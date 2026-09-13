# AGENTS.md

Rules an AI agent (or a new contributor) follows in this repo. Added by `action-platform install`; keep it current.

[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/): `type(scope)!: description` — `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. One commit per concern; stage files explicitly — never `git add .`. Enforced by git hooks (`action-platform install`) and CI.

Git-flow: work on `<kind>/<code>[-slug]` started with `action-platform branch <kind> <code>`. Kinds: `feature bugfix hotfix release support chore docs refactor test ci perf`. Never commit on `main`, `master` or `develop`; `feature`/`bugfix` merge into `develop`, `release`/`hotfix` into `main` and `develop`.

`platform.toml` declares the project; `action-platform release` cuts versions from `LAST_VERSION`; `action-platform gitflow` audits a branch before a pull request.
