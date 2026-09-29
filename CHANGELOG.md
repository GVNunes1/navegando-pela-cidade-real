# Histórico de versões

## 0.2.1 — 29/09/2026 — Correção do build na Vercel

- Removida a exceção de importação de `settings.py` quando as variáveis de produção ainda não foram informadas.
- Adicionada resposta HTTP 503 com os nomes das variáveis ausentes. Nenhuma consulta ao banco é feita nessa condição.
- Adicionado teste de regressão para o deploy sem variáveis.

## 0.2.0 — 29/09/2026 — Preparação para Supabase e Vercel

- Substituído o banco MariaDB local por conexão PostgreSQL via `DATABASE_URL`, com SQLite para desenvolvimento.
- Desativados prepared statements do Psycopg para o pooler transacional do Supabase.
- Removida a dependência de GEOS/GDAL e convertido o armazenamento de coordenadas para latitude/longitude.
- Corrigido o cálculo de proximidade para distância em metros por Haversine.
- Criado comando `seed_data` idempotente para importar os quatro conjuntos JSON.
- Removidas rotas HTTP públicas que alteravam o banco; a carga agora é um comando administrativo.
- Configurados host, CSRF, cookies seguros e arquivos estáticos para a Vercel.
- Adicionados testes da busca e documentação de implantação.

## 0.1.0 — versão original importada

- Aplicação Django de busca por marcos urbanos, paradas e linhas de ônibus de Boituva.
- Projeto original de Marcos Silveira, preservado no histórico Git importado.

Detalhes, justificativas e evidências estão em [docs/RELATORIO_DE_MODIFICACOES.md](docs/RELATORIO_DE_MODIFICACOES.md).
