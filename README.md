# python-template

A [Copier](https://copier.readthedocs.io) template for production-ready Python projects. Every generated project is linted, typed, tested, scanned and containerised from its first commit, and it can pull in later template improvements with one command.

```sh
uvx copier copy --trust gh:Qualixto/python-template my-project
```

`--trust` lets Copier run the post-generation tasks: `git init` and `uv lock`.

---

## What you get

| Area | Tooling | Why |
|---|---|---|
| Environments | [uv](https://docs.astral.sh/uv/), `.python-version`, `uv.lock` | One fast tool for Python, dependencies and lockfiles |
| Lint and format | [ruff](https://docs.astral.sh/ruff/), including bandit-style `S` rules | One tool instead of four, with security linting built in |
| Types | mypy `--strict` over `src`, `tests` and `tasks.py` | Type errors fail the build, not production |
| Tests | pytest with branch coverage, failing under 90% | Coverage is a gate, not a report nobody reads |
| Tasks | [invoke](https://www.pyinvoke.org) `tasks.py` | CI runs the same tasks as you do locally, so they can't drift |
| Git hooks | pre-commit: hygiene, gitleaks, ruff, mypy, conventional commits; tests on push | Problems are caught before they reach a pull request |
| Security | gitleaks, `uv audit`, Dependabot for uv, Actions and Docker | Secrets and vulnerable dependencies are caught automatically |
| Container | uv base image, cached dependency layer, non-root user, smoke test | The image is tested, not just built |
| CI | GitHub Actions: lint, test, audit, secrets, smoke | Fails by default; nothing merges red |
| Ways of working | `DEFINITION_OF_DONE.md`, ADRs in `docs/adr/`, `CLAUDE.md` | Shared standards for people and AI agents alike |

### Optional: API service

Answer **yes** to the API question to add a FastAPI service that wraps an upstream HTTP API:

- `create_app` takes the upstream client as an argument, so tests inject a fake via `httpx2.MockTransport`.
- Upstream failures, timeouts and malformed payloads map to deliberate status codes and are covered by tests.
- A fake upstream in `tests/` lets you run the whole stack locally with `invoke serve`.
- A [Bruno](https://www.usebruno.com) collection doubles as API documentation and as end-to-end tests (`invoke api-test`), run in CI.

## Questions

| Question | Default |
|---|---|
| `project_name` | required |
| `project_slug` | derived from the name, e.g. `my-project` |
| `package_name` | derived from the slug, e.g. `my_project` |
| `description` | empty |
| `author_name`, `author_email` | required |
| `python_version` | `3.13` (3.12 to 3.14) |
| `api` | `false` |
| `license` | `Apache-2.0` (or `MIT`, `Proprietary`) |

## Keeping projects up to date

Generated projects record their answers in `.copier-answers.yml`. To apply later template changes:

```sh
uvx copier update --trust
```

Copier merges the changes, and anything that conflicts with your edits shows up as a normal git conflict.

## Developing the template

```sh
uv sync
uv run pre-commit install
uv run invoke lint     # the template's own tooling
uv run invoke test     # renders every variant and runs its lint and test tasks
uv run invoke render --dest /tmp/demo --api
```

CI also builds and smoke-tests the Docker image and runs the Bruno suite for each generated variant.

## Licence

[Apache-2.0](LICENSE). Maintained by [Qualixto](https://qualixto.com).
