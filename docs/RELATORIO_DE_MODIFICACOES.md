# Relatório de modificações para versionamento

**Projeto:** Navegando pela Cidade Real — Rotas de ônibus por marcos urbanos  
**Origem:** repositório de Marcos Silveira, importado com histórico Git  
**Versão documentada:** 0.2.0  
**Data:** 29/09/2026  
**Objetivo:** permitir hospedagem do aplicativo Django na Vercel com persistência no PostgreSQL do Supabase.

## 1. Situação inicial

A versão importada usava GeoDjango, MariaDB local e caminhos de arquivo dependentes do diretório de execução. O `docker-compose.yml` incluía apenas o banco, embora o README descrevesse também um contêiner da aplicação. A configuração `ALLOWED_HOSTS=[]` impedia o atendimento em domínio público. A importação de dados era acionada por URLs HTTP públicas, que podiam modificar o banco sem autenticação.

## 2. Alterações realizadas

| Área | Antes | Depois | Justificativa |
|---|---|---|---|
| Persistência | MariaDB em `127.0.0.1` | PostgreSQL por `DATABASE_URL`; SQLite local | Permitir banco gerenciado Supabase e desenvolvimento simples |
| Coordenadas | `PointField` GeoDjango | `latitude` e `longitude` numéricos | Evitar dependências nativas GEOS/GDAL na Vercel |
| Proximidade | Operações espaciais e conversão Web Mercator | Fórmula de Haversine em metros | Calcular distância geodésica sem distorção da projeção Mercator |
| Importação | Views GET públicas | Comando `manage.py seed_data` | Restringir alterações de dados à administração |
| Arquivos JSON | Caminho relativo ao processo | Caminho baseado no arquivo do comando | Funcionar em diferentes diretórios |
| Segurança web | Hosts vazios e sem configuração de proxy | Hosts, origem CSRF, cookies seguros e HTTPS por proxy | Atender domínio da Vercel com proteção básica |
| Arquivos estáticos | Configuração incompleta | WhiteNoise e `STATIC_ROOT` | Servir recursos do Django Admin |
| Navegação | Busca apenas em `/boituvaplaces/buscar/` | Busca também na raiz `/` | Abrir diretamente a página principal após deploy |

O PostGIS está ativado no Supabase, mas esta versão não o usa nas consultas. Essa escolha preserva a funcionalidade de busca no runtime da Vercel e permite avaliar consultas espaciais no banco em versão futura.

## 3. Arquivos modificados

- `piplaces/settings.py` e `requirements.txt`: ambiente, banco e dependências.
- `boituvaplaces/models.py` e `migrations/0001_initial.py`: novo esquema de coordenadas.
- `boituvaplaces/views.py` e `urls.py`: busca, distâncias e remoção de importações públicas.
- `boituvaplaces/management/commands/seed_data.py`: carga reproduzível.
- `piplaces/urls.py`: rota inicial.
- `boituvaplaces/tests.py`: testes automatizados.
- `README.md`, `.env.example` e `CHANGELOG.md`: operação e versionamento.

O antigo `docker-compose.yml` e o importador por caminho relativo foram removidos.

## 4. Verificação

Em desenvolvimento local, com Python 3.11 e as dependências de `requirements.txt`:

1. `python manage.py check`: nenhum problema identificado.
2. `python manage.py makemigrations --check --dry-run`: nenhuma migração pendente.
3. `python manage.py migrate`: migrações aplicadas em SQLite local.
4. `python manage.py seed_data`, executado duas vezes: 11 rotas, 368 paradas e 1331 locais nas duas execuções.
5. `python manage.py test`: 2 testes aprovados.
6. Busca HTTP local por um identificador de destino: resposta 200 com destino, parada e linhas.
7. `python manage.py collectstatic --noinput`: arquivos estáticos gerados.

## 5. Limites e próximos passos

O banco Supabase foi criado e o PostGIS está ativo, mas as migrações e a carga de dados ainda exigem a URI PostgreSQL com senha; ela deve ficar apenas no ambiente local e nas variáveis da Vercel. O deploy na Vercel será criado pelo responsável pela conta, que poderá importar o repositório. Até a execução das migrações no Supabase e um teste na URL pública, o funcionamento em produção permanece não verificado.

A migração inicial foi reescrita porque o banco Supabase deste projeto foi criado vazio. Bancos que já tenham aplicado a migração original com `PointField` exigem uma migração de dados específica antes de atualizar.
