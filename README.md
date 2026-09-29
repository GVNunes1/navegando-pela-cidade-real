# Navegando pela Cidade Real

Aplicação Django para buscar locais de Boituva e identificar o marco urbano e a parada de ônibus mais próximos, incluindo as linhas disponíveis na parada.

## Origem

Este repositório foi importado do [projeto de Marcos Silveira](https://github.com/marcosilveira2/Navegando-pela-Cidade-Real-Rotas-de-nibus-por-Marcos-Urbanos). A adaptação para hospedagem e o histórico de mudanças estão em [CHANGELOG.md](CHANGELOG.md) e [docs/RELATORIO_DE_MODIFICACOES.md](docs/RELATORIO_DE_MODIFICACOES.md).

## Desenvolvimento local

Requer Python 3.11 ou superior. No Windows:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py seed_data
.venv\Scripts\python manage.py runserver
```

Sem `DATABASE_URL`, o projeto usa SQLite local. A aplicação fica em `http://127.0.0.1:8000/`. Para testar: `.venv\Scripts\python manage.py test`.

## Supabase

O projeto Supabase **Navegando pela Cidade Real** está na organização **Projetos Integradores**. O PostGIS foi ativado no esquema `extensions`; a versão hospedada usa as colunas `latitude`/`longitude` e calcula distâncias em Python para evitar a dependência de GEOS/GDAL no runtime da Vercel.

No painel do Supabase, abra **Connect** e copie a URI PostgreSQL do **Transaction pooler** (porta 6543), adequado a aplicações serverless. Use essa URI como `DATABASE_URL` em um `.env` local, execute uma vez `python manage.py migrate` e `python manage.py seed_data`. Essas operações criam as tabelas do Django e importam os JSON. O comando de importação pode ser repetido sem duplicar registros. O Psycopg está configurado sem prepared statements para ser compatível com esse pooler. Não coloque a URI ou senha no Git.

## Vercel

1. Importe este repositório na Vercel com a pasta raiz do projeto como **Root Directory**. A Vercel detecta o `manage.py` e o aplicativo Django.
2. Configure as variáveis de ambiente **antes do primeiro deploy**:
   - `DATABASE_URL`: URI PostgreSQL do pooler Supabase, com a senha.
   - `SECRET_KEY`: chave aleatória longa gerada para esta implantação.
   - `DEBUG=False`.
   - `ALLOWED_HOSTS`: opcional para domínio próprio; `.vercel.app` já está permitido.
   - `CSRF_TRUSTED_ORIGINS`: URL HTTPS do domínio próprio, se houver.
3. Execute as migrações e a carga de dados no Supabase antes de testar a busca publicada. É possível usar o mesmo `DATABASE_URL` em uma máquina local para esses comandos.
4. Abra a URL publicada, busque um local e confira o marco, a parada e as linhas. O painel `/admin/` exige um superusuário criado com `python manage.py createsuperuser`.

O deploy não executa migrações automaticamente. Isso evita que uma requisição web modifique a estrutura do banco. Os arquivos estáticos do admin são gerados com `collectstatic` no build da Vercel.

## Dados

- `boituvaplaces/rotas_limpo.json`: linhas de ônibus.
- `boituvaplaces/pontos_onibus.json`: paradas e coordenadas disponíveis.
- `boituvaplaces/lista_de_locais_1.json`: locais pesquisáveis.
- `boituvaplaces/pontos_turisticos.json`: marcos turísticos.

Paradas sem coordenadas são preservadas no banco, mas não entram no cálculo de proximidade. Distâncias são aproximações geodésicas em metros pela fórmula de Haversine.
