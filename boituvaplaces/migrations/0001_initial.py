from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="CategoriaMarco",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Rota",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=10, unique=True)),
                ("nome", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="ParadaOnibus",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("endereco", models.CharField(max_length=200, unique=True)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("rotas", models.ManyToManyField(related_name="pontos", to="boituvaplaces.rota")),
            ],
        ),
        migrations.CreateModel(
            name="Local",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=200)),
                ("endereco", models.CharField(max_length=300)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("e_marco", models.BooleanField(db_index=True, default=False)),
                ("tipo_marco", models.ManyToManyField(blank=True, related_name="locais", to="boituvaplaces.categoriamarco")),
            ],
            options={
                "verbose_name": "Local",
                "verbose_name_plural": "Locais",
                "indexes": [models.Index(fields=["e_marco"], name="boituvaplac_e_marco_ed69da_idx")],
                "constraints": [models.UniqueConstraint(fields=("nome", "endereco"), name="local_nome_endereco_unique")],
            },
        ),
    ]
