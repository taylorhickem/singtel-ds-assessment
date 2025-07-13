# Environment setup

## Session logs

session logs are timestamped to Singapore timezone in reverse chronological order, with latest entries at the top, and earlier entries at the bottom.

### Environment setup [Developer] 2025-07-13 18:55

- repository config
- setup local virtual env
- create docs

repository config

- create github repository: [singtel-ds-assessment](https://github.com/taylorhickem/singtel-ds-assessment)
- OpenAI Codex configuration
  - create `AGENTS.md` for use with AI Coding agent OpenAI Codex
  - grant repository access 

setup local virtual env `env`

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
```

create docs

- using `mkdocs` package
- create documentation outline with pages for each task
- page for guidelines and project information
- publish to [Github page: Singtel Data Science Assessment](https://taylorhickem.github.io/singtel-ds-assessment/)