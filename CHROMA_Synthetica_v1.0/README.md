# CHROMA Synthetica v1.1 — Guia Rápido

## Execução
- `python main.py` roda as duas demos padrão (Kinnari Solarpunk e Centaur Chiaroscuro) usando a KB unificada v1.1.
- Para exercícios personalizados, importe `ChromaSyntheticaOrchestrator` e chame `run_workflow` com seu `AbstractCreativeObject` e pipeline de operadores.
- Todos os testes unitários passam com `python -m pytest` (requer `pytest>=8.4` instalado).

## Configuração da KB
- Arquivo padrão: `kb/synthetica_kb_v1.1.json`.
- Pode ser substituído em tempo de execução via `SYNTHETICA_KB_PATH=/caminho/para/sua_kb.json`.
- Caso a KB v1.1 ainda não exista, execute `python scripts/migrate_kb.py` para fundir os artefatos legados.

## Clientes LLM
- A CLI do SeaDream (`interactive_assistant.py` / `interactive_chat.py`) usa a factory de `llm_client`.
- Ambiente local sem chave: defina `SYNTHETICA_LLM_PROVIDER=stub` para ativar o `StubLLMClient` (sem chamadas externas).
- Produção Gemini: forneça `GEMINI_API_KEY` via ambiente ou `config/gemini_api_key.txt`.

## Conectores Externos
- `ExternalKnowledgeHub` usa Wikipedia + Wikidata com timeout configurável (`SYNTHETICA_HTTP_TIMEOUT`, padrão 5s).
- As respostas são cacheadas em memória durante a execução para evitar requisições redundantes.

## Antropofagia Sintética
- A diretiva `Operator_CulturalCannibalize` gera combinações dinâmicas: a síntese mistura até 3 keywords da cultura que devora e 2 do elemento devorado, adicionando uma nota contextual conforme o modo (`Aesthetic`, `Narrative`, `Symbolic`).
- Exemplos prontos:
  - Solarpunk + Iris van Herpen (modo `Aesthetic`) na demo oficial.
  - Yoruba + Brutalism (modo `Symbolic`) — ver exemplo de prompt gerado com `Seedream_4_0` no registro de execução recente.
