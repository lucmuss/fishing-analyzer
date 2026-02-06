# Release Workflow

## Versioning
Use semantic versioning with tags in the format `vX.Y.Z`.

## Checklist
1. Run `just ci` locally.
2. Update changelog and docs.
3. Create and push a tag:
```bash
git tag v0.2.0
git push origin v0.2.0
```
4. `publish-to-pypi.yml` publishes to PyPI on tag.
5. `build-binaries.yml` builds binaries and attaches them to a GitHub release.

## TestPyPI
Trigger `publish-to-pypi.yml` manually with `target=testpypi`.
