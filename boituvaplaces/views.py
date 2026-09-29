from math import asin, cos, radians, sin, sqrt

from django.shortcuts import render

from .models import Local, ParadaOnibus


def distancia_metros(lat1, lon1, lat2, lon2):
    """Distância geodésica aproximada entre dois pontos (fórmula de Haversine)."""
    raio_terra = 6371000
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * raio_terra * asin(sqrt(min(1, max(0, a))))


def mais_proximo(candidatos, origem):
    if origem.latitude is None or origem.longitude is None:
        return None
    validos = (item for item in candidatos if item.latitude is not None and item.longitude is not None)
    def distancia(item):
        return distancia_metros(origem.latitude, origem.longitude, item.latitude, item.longitude)
    escolhido = min(validos, key=distancia, default=None)
    if escolhido:
        escolhido.distancia_em_metros = distancia(escolhido)
    return escolhido


def buscar_proximidades(request):
    query = request.GET.get("q", "").strip()
    local_id = request.GET.get("local_id", "").strip()
    context = {"query": query}

    local_pesquisado = None
    if local_id.isdecimal():
        local_pesquisado = Local.objects.filter(pk=int(local_id)).first()
    elif query:
        encontrados = Local.objects.filter(nome__icontains=query).order_by("nome", "endereco")
        quantidade = encontrados.count()
        if quantidade == 1:
            local_pesquisado = encontrados.first()
        elif quantidade > 1:
            context["locais_multiplos"] = encontrados[:50]
        else:
            context["erro"] = "Nenhum local encontrado no banco de dados."

    if local_pesquisado:
        context["local_pesquisado"] = local_pesquisado
        context["marco_proximo"] = mais_proximo(
            Local.objects.filter(e_marco=True).exclude(pk=local_pesquisado.pk), local_pesquisado
        )
        context["ponto_proximo"] = mais_proximo(
            ParadaOnibus.objects.prefetch_related("rotas").all(), local_pesquisado
        )
    return render(request, "boituvaplaces/busca_local.html", context)
