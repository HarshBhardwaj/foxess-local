# Release checklist

Semantic versioning; conventional commits; CI green on all supported Python
versions before tagging.

## Pre-release

- [ ] `ruff check src tests` clean
- [ ] `mypy` clean
- [ ] `pytest -q` green (no hardware required)
- [ ] `python -m build` produces wheel + sdist
- [ ] `docker build -f docker/Dockerfile .` succeeds
- [ ] CHANGELOG updated (Keep a Changelog format)
- [ ] Version bumped in `pyproject.toml` and `foxess/__init__.py`
- [ ] Docs reviewed; verified/experimental status of decoders is accurate
- [ ] Register map (`fox_model_defs.json`) unchanged, or migration noted

## Verification against hardware (optional, HIL)

- [ ] `fox scan "$FOX_HOST" 2` matches the supported-model matrix
- [ ] `fox read "$FOX_HOST" 2 1` returns correct identity
- [ ] Spot-check a scaled measurement against the FoxCloud dashboard
- [ ] (If touching writes) `write_field(..., dry_run=True)` frame reviewed by a
      second person before any real write

## Tag & publish

- [ ] `git tag vX.Y.Z` (annotated) and push
- [ ] GitHub Release with notes; CI publishes artifacts
- [ ] `twine upload dist/*` (or trusted-publisher workflow) to PyPI
- [ ] Container image tagged `foxess-local:X.Y.Z` and `:latest`

## Post-release

- [ ] Verify `pip install foxess-local==X.Y.Z` in a clean venv
- [ ] Announce; open a milestone for the next version
