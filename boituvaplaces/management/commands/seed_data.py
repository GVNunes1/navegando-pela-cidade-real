"""Importa os JSON versionados no projeto. Pode ser executado repetidas vezes."""

import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from boituvaplaces.models import CategoriaMarco, Local, ParadaOnibus, Rota

DATA_DIR = Path(__file__).resolve().parents[2]


def ler_json(nome):
    with (DATA_DIR / nome).open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


class Command(BaseCommand):
    help = "Carrega rotas, paradas, locais e marcos dos JSON do repositório."

    @transaction.atomic
    def handle(self, *args, **options):
        for codigo, nome in ler_json("rotas_limpo.json").items():
            Rota.objects.update_or_create(codigo=codigo, defaults={"nome": nome})

        for endereco, dados in ler_json("pontos_onibus.json").items():
            endereco = endereco.strip('", ')
            if dados and isinstance(dados[0], list):
                codigos = dados[0]
                latitude = dados[1].get("latitude")
                longitude = dados[2].get("longitude")
            else:
                codigos = dados if isinstance(dados, list) else [dados]
                latitude = longitude = None
            parada, _ = ParadaOnibus.objects.update_or_create(
                endereco=endereco,
                defaults={"latitude": latitude, "longitude": longitude},
            )
            parada.rotas.set(Rota.objects.filter(codigo__in=codigos))

        for item in ler_json("lista_de_locais_1.json"):
            tipos = item.get("tipo", "")
            if isinstance(tipos, list):
                tipos = ", ".join(tipos)
            Local.objects.update_or_create(
                nome=item["nome"],
                endereco=item["endereco"],
                defaults={
                    "latitude": item.get("lat"),
                    "longitude": item.get("lng"),
                    "tipo_local": tipos[:200],
                },
            )

        categoria, _ = CategoriaMarco.objects.get_or_create(nome="Turístico")
        for item in ler_json("pontos_turisticos.json"):
            nome = item.get("Ponto Turístico") or item.get("nome")
            endereco = item.get("Endereço") or item.get("endereco", "")
            if not nome:
                continue
            local, _ = Local.objects.update_or_create(
                nome=nome,
                endereco=endereco,
                defaults={
                    "latitude": item.get("lat"),
                    "longitude": item.get("lon"),
                    "e_marco": True,
                },
            )
            local.tipo_marco.add(categoria)

        self.stdout.write(self.style.SUCCESS(
            f"Dados carregados: {Rota.objects.count()} rotas, "
            f"{ParadaOnibus.objects.count()} paradas, {Local.objects.count()} locais."
        ))
