# Environment setup

## Session logs

session logs are timestamped to Singapore timezone in reverse chronological order, with latest entries at the top, and earlier entries at the bottom.

### Environment setup [Developer] 2025-07-13 18:30

- create github repository: [singtel-ds-assessment](https://github.com/taylorhickem/singtel-ds-assessment)
- OpenAI Codex configuration
  - create `AGENTS.md` for use with AI Coding agent OpenAI Codex
  - grant repository access 

- setup local virtual env `env`

```bash
$ python -m venv env
```

```bash
$ python -m pip install --upgrade pip
```

```bash
$ pip install -r requirements.txt
```

requirements.txt

```
mkdocs
mkdocs-material
mkdocs-material[mermaid]
```