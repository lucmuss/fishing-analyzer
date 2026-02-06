# Release Workflow

## Versioning
Use semantic versioning with tags in the format `vX.Y.Z`.

## Checklist
1. If dependencies changed, run `uv lock` and commit `uv.lock`.
2. Run `just ci` locally.
3. Update changelog and docs.
4. Create and push a tag:
```bash
git tag v0.2.0
git push origin v0.2.0
```
5. `publish-to-pypi.yml` publishes to PyPI on tag.
6. `build-binaries.yml` builds binaries and attaches them to a GitHub release.

## TestPyPI
Trigger `publish-to-pypi.yml` manually with `target=testpypi`.
