# Environment setup

## Session logs

session logs are timestamped to Singapore timezone in reverse chronological order, with latest entries at the top, and earlier entries at the bottom.

### Design [Codex] 2025-07-13 <HH>:<MM>


### Design [Developer] Codex prompt 2025-07-13 19:16
for context, refer to assignment main page `docs/01_assignment.md`

this project implements a number of Gen AI Developer features, organized into tasks, one of which is LangChain as well as RAG features.
Setting up the environment for these packages which have many dependencies can be tricky to correctly specify the environment and packages with correct versions, avoid conflicts etc..

your task
- scope: tasks 1-3. 
  - Do NOT worry about task 4 yet, that would be a whole new set of requirements for a small stand alone app

- consider the design, functional requirements, how you would implement these tasks, which frameworks and python packages you would use

- 01 document your design in each of the respective pages for each task 01-03

  - 01.01 `docs/tasks/0301_custom_agent.md`
  - 01.02 `docs/tasks/0302_rag.md`
  - 01.03 `docs/tasks/0303_integration.md`

- 02 from this design, for tasks 01 and 02, extract the list of python packages needed, such as LangChain
  - from this list of packages, update `requirements.txt` to correctly specify and format the python package requirements
  - write out the bash steps to setup the env in `setup.sh` it can be a simple as `pip install -r requirements.txt`, if you need some custom setup steps, document them here in the `setup.sh`

- 03 from the design, for tasks 01 and 02, consider for the build, secrets, other files that might be used or generated at runtime that do NOT belong in the repository
  - update `.gitignore` for the additional files and directories that might be generated which should NOT belong in the repository

- document and timestamp your activity in the release doc `dev/001_env_setup.md` in section ## Session Log subsection ### Design [Codex] 2025-07-13 <HH>:<MM>

- create a PR with changes
  - design pages 01-03
  - `.gitignore`
  - `requirements.txt`
  - `setup.sh`
  - your session log

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