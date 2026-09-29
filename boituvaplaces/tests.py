import os
from unittest.mock import patch

from django.test import TestCase

from .models import Local, ParadaOnibus, Rota
from .views import distancia_metros


class BuscaProximidadesTests(TestCase):
    def setUp(self):
        self.destino = Local.objects.create(nome="Praça Central", endereco="Centro", latitude=-23.28, longitude=-47.67)
        Local.objects.create(nome="Marco distante", endereco="Rua B", latitude=-23.30, longitude=-47.70, e_marco=True)
        Local.objects.create(nome="Marco próximo", endereco="Rua A", latitude=-23.2801, longitude=-47.6701, e_marco=True)
        self.parada = ParadaOnibus.objects.create(endereco="Parada A", latitude=-23.2802, longitude=-47.6702)
        rota = Rota.objects.create(codigo="001", nome="Centro")
        self.parada.rotas.add(rota)
        ParadaOnibus.objects.create(endereco="Sem coordenadas")

    def test_busca_retorna_marco_parada_e_linha(self):
        response = self.client.get("/buscar/", {"local_id": self.destino.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Marco próximo")
        self.assertContains(response, "Parada A")
        self.assertContains(response, "001 - Centro")
        self.assertNotContains(response, "Sem coordenadas")

    def test_distancia_em_metros_e_nao_em_graus(self):
        self.assertAlmostEqual(distancia_metros(-23.28, -47.67, -23.28, -47.67), 0)
        self.assertGreater(distancia_metros(-23.28, -47.67, -23.281, -47.67), 100)

    def test_deploy_sem_variaveis_retorna_configuracao_pendente(self):
        with patch.dict(os.environ, {"VERCEL": "1", "SECRET_KEY": "", "DATABASE_URL": ""}):
            response = self.client.get("/")
        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "SECRET_KEY", status_code=503)
        self.assertContains(response, "DATABASE_URL", status_code=503)
