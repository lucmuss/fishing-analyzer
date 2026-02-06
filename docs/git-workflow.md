# Git Workflow

## Branching
- `main`: protected production branch.
- `feature/<topic>`: new features.
- `fix/<topic>`: bug fixes.
- `chore/<topic>`: maintenance work.

## Development Flow
1. Create a branch from `main`.
2. Run `just format` and `just check` before each push.
3. Commit with clear scoped messages.
4. Open a pull request to `main`.
5. Wait for `CI` (`lint -> typecheck -> tests -> build`) to pass.
6. Merge via squash or rebase.

## Release Flow
1. Update version and release notes.
2. Tag `main` with `vX.Y.Z`.
3. Push tag to trigger publishing and binary workflows.

## Commit Message Style
Use concise imperative messages, for example:
- `feat: add docker compose healthchecks`
- `fix: correct precipitation parser`
- `chore: migrate package layout to src/`
