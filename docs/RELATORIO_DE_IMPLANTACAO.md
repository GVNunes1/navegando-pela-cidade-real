# Relatório de implantação e validação

**Projeto:** Navegando pela Cidade Real  
**Data:** 29/09/2026  
**Ambiente:** Vercel (aplicação Django) e Supabase (PostgreSQL)

## Ocorrência

O primeiro acesso à página inicial publicada funcionou, mas a busca por “Centro Nacional” retornou HTTP 500. A inspeção do Supabase mostrou que o esquema `public` não continha tabelas da aplicação. A página inicial não consulta o banco; a busca consulta o modelo `Local`, por isso somente a segunda requisição falhava.

## Correção aplicada

Foi gerado o esquema PostgreSQL correspondente aos modelos Django e aplicado ao projeto Supabase “Navegando pela Cidade Real”. O registro das migrações iniciais foi transferido do ambiente local. Em seguida foram importados os registros dos JSON versionados, preservando IDs e relacionamentos. As sequências de IDs foram ajustadas ao maior valor importado.

Todas as tabelas criadas em `public` receberam Row Level Security (RLS) sem políticas para os papéis públicos da API Supabase. O aplicativo Django acessa o banco pelo usuário PostgreSQL configurado em `DATABASE_URL`. O PostGIS permanece ativado no esquema `extensions`, mas a versão atual calcula distâncias em Python.

| Conjunto | Registros verificados no Supabase |
|---|---:|
| Rotas | 11 |
| Paradas | 368 |
| Locais | 1.331 |
| Relações entre paradas e rotas | 814 |
| Migrações registradas | 20 |

## Testes no site público

- `/`: página de busca exibida.
- `/?q=Centro+Nacional`: dois destinos correspondentes exibidos, sem erro.
- Seleção do destino “Centro Nacional De Paraquedismo”: marco “Passeio De Balão Boituva” a aproximadamente 1.218 m; parada “Rua Domingos Waldemar Bellucci, 136” a aproximadamente 373 m; linha “012 - Solaris”.
- `/admin/`: página de login do Django exibida.

**Resultado:** o fluxo principal de busca está funcional na URL pública `https://navegando-pela-cidade-real-boituva.vercel.app/`.

## Observações para versões futuras

O banco foi inicializado por SQL gerado dos modelos Django porque a senha de conexão não foi compartilhada com o agente. As próximas alterações de esquema devem seguir o fluxo normal de migrações Django usando `DATABASE_URL` em um ambiente administrativo. Não reaplique o esquema inicial manualmente em um banco que já contenha essas tabelas. A autenticação do painel admin não foi testada, pois não foi criado um superusuário.
