import os

from django.http import HttpResponse


class DeploymentConfigurationMiddleware:
    """Deixa o build importar Django, mas impede requisições sem configuração."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if os.getenv("VERCEL"):
            ausentes = [name for name in ("SECRET_KEY", "DATABASE_URL") if not os.getenv(name)]
            if ausentes:
                return HttpResponse(
                    "Implantação pendente: configure " + ", ".join(ausentes) + " na Vercel.",
                    status=503,
                    content_type="text/plain; charset=utf-8",
                )
        return self.get_response(request)
