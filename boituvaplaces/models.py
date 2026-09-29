from django.db import models


class Rota(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class ParadaOnibus(models.Model):
    endereco = models.CharField(max_length=200, unique=True)
    rotas = models.ManyToManyField(Rota, related_name="pontos")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Parada de Ônibus"
        verbose_name_plural = "Paradas de Ônibus"

    def __str__(self):
        return self.endereco


class CategoriaMarco(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Categoria de Marco"
        verbose_name_plural = "Categorias de Marco"

    def __str__(self):
        return self.nome


class Local(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=300)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    e_marco = models.BooleanField(default=False, db_index=True)
    tipo_marco = models.ManyToManyField(CategoriaMarco, blank=True, related_name="locais")
    tipo_local = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"
        indexes = [models.Index(fields=["e_marco"])]
        constraints = [models.UniqueConstraint(fields=["nome", "endereco"], name="local_nome_endereco_unique")]

    def __str__(self):
        return f"{self.nome} ({'Marco' if self.e_marco else 'Comum'})"
