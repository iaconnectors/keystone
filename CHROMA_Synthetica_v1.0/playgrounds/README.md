# Seedream Case Library

The `seedream_cases.json` file contains curated presets for the interactive chat CLI.

Each entry provides:

- `title`: short description of the creative context.
- `theme`: recommended SeaDream theme (must exist in `THEME_LIST`).
- `brief`: default briefing passed to the assistant.
- `notes`: post-generation reminders or follow-up actions.

## Using the Cases in the CLI

```bash
python interactive_chat.py --theme cinematografico
```

Inside the prompt loop use:

- `/case marketing_product_consistency`
- `/case tipografia_evento`
- `/case storyboard_exploracao`
- `/case arquitetura_pavilhao_lux`
- `/case stand_imersivo_tech`

The CLI prints the suggested theme, the briefing, and any additional notes before executing the full Seedream pipeline with `run_interaction`.
