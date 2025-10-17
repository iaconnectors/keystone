# SeaDream Prompt Playground (Front-end)

Interface web simples que consome o backend FastAPI (`playground_backend`) para gerar,
curtir e reutilizar prompts SeaDream.

## Estrutura

- `index.html`: layout principal com painel de presets, formulário e histórico.
- `styles.css`: tema escuro inspirado no console CHROMA.
- `app.js`: lógica da SPA (fetch de casos, histórico, geração e likes).

## Execução

1. Inicie o backend:
   ```bash
   uvicorn playground_backend.main:app --reload
   ```
2. Em outro terminal, sirva os arquivos estáticos (ex.: `python -m http.server` na raiz do repo) e abra `http://localhost:8000/index.html` conforme a porta utilizada.

O front comunica-se com o backend em `http://localhost:8000`; ajuste `API_BASE` em `app.js`
se publicar em outra porta.

## Funcionalidades

- Seleção rápida de presets (cases + referencias curtidas) com um clique.
- Formulário para editar briefing, tema, modelo Gemini e tags.
- Exibição do blueprint e prompts por modelo com botões de cópia.
- Histórico lateral com filtro “Todos” / “Curtidos” e ação “Usar como base”.
- Botão “Curtir referência” transforma a sessão atual em referência reutilizável.

## Roadmap

- Sincronizar automaticamente referências com o catálogo de cases.
- Adicionar busca e filtros avançados (tags, data, modelo).
- Exportar sessões em formatos (`.json`, `.md`) diretamente da UI.
- Autenticação e multiusuário (quando necessário).
