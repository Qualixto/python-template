# CLAUDE.md

Guidance for AI coding agents working on this Copier template.

## Layout

- `copier.yml`: questions, validators and post-generation tasks.
- `template/`: the generated project. Files ending in `.jinja` are rendered; everything else is copied verbatim. Conditional files and folders use names like `{% if api %}api.py{% endif %}.jinja`.
- `tests/test_template.py`: renders variants with Copier and runs each one's own `invoke lint` and `invoke test`.
- `tasks.py`: tasks for the template repo itself. CI runs the same tasks.

## Commands

```sh
uv run invoke lint                          # ruff and mypy on tasks.py and tests
uv run invoke test                          # render every variant and check it
uv run invoke render --dest /tmp/demo --api # inspect a rendered project
```

After changing anything under `template/`, run `invoke test`. For changes touching Docker, Bruno or `invoke smoke`/`api-test`, also render a project and run those tasks inside it.

## Rules

- **Generated projects must pass their own CI.** Every change to `template/` keeps `lint`, `test`, `audit`, `smoke` and (for the API variant) `api-test` green.
- **Jinja and GitHub Actions both use `{{ }}`.** Wrap Actions expressions in rendered files in `{% raw %}...{% endraw %}`. Bruno `.bru` files aren't rendered, so their `{{baseUrl}}` needs no escaping.
- **Keep the CLI and API variants in step.** Shared behaviour belongs outside the `{% if api %}` blocks.
- Keep example code small and obviously replaceable; the template is a starting point, not a framework.
- Keep the generated `CLAUDE.md` in step with the generated project's tooling.

## Conventions

- Branch as `<type>/<issue>-<short-description>`; start from an issue.
- Commits are `<type>: <description>` with types `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`. CI and tooling changes are `chore`.
- Never add AI attribution (`Co-Authored-By` trailers or "Generated with" footers) to commits, pull requests, issues or comments.
- Comments explain *why*, not *what*.
