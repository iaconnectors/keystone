# SeaDream Prompt Playground Backend

FastAPI service that wraps the CHROMA Synthetica pipeline to generate SeaDream prompts
without depender da interface CLI.

## Endpoints

| Method | Path | Descrição |
| ------ | ---- | --------- |
| `POST` | `/generate` | Executa o pipeline e grava a sessão no histórico. |
| `GET` | `/history` | Lista sessões (mais recentes primeiro). |
| `POST` | `/history/{id}/like` | Marca ou desmarca uma sessão como referência. |
| `GET` | `/references` | Retorna todas as sessões curtidas. |

### Payload de geração

```json
{
  "brief": "Hero shot para serum sustentável...",
  "theme": "cinematografico",
  "model": "models/gemini-2.5-pro",
  "case_id": "marketing_product_consistency",
  "tags": ["campanha", "produto"]
}
```

Resposta (`GenerateResponse`) inclui blueprint formatado, prompts por modelo e o registro
persistido no histórico (`PromptSession`).

## Execução

```bash
python -m pip install -r requirements.txt
uvicorn playground_backend.main:app --reload
```

Defina a chave do Gemini via `GEMINI_API_KEY` (ou `config/gemini_api_key.txt` já utilizado
pelas ferramentas atuais).

O histórico é salvo em `playground_backend/data/prompt_history.json`. Sessões curtidas (`liked: true`)
poderão alimentar novos presets ou a KB após revisão manual.

## Roadmap

- Expor endpoint para reaproveitar referências como presets (`GET /cases`), mesclando favoritos
  ao catálogo existente em `playgrounds/seedream_cases.json`.
- Permitir atualização/remoção de sessões no histórico.
- Adicionar camadas de autenticação e limite de requisições por usuário.
