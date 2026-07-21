# Contributing

Thanks for helping build the local FoxESS SDK.

## Principles

- **Evidence-first.** Every register/decoder change must be backed by captured
  bytes, a UI value, the SunSpec spec, or the frontend decoder. Mark unverified
  mappings clearly; never guess.
- **No hardware in tests.** The suite runs against captured fixtures. HIL checks
  are optional and separate.
- **Safety.** Writes stay disabled by default and behind explicit confirmation.

## Workflow

1. `pip install -e ".[dev,api,mqtt,prometheus]"` and `pre-commit install`.
2. Make changes with full type hints and docstrings on public APIs.
3. `ruff check src tests`, `mypy`, and `pytest -q` must pass.
4. Conventional-commit messages; open a PR. CI runs the full matrix.

## Secrets & personal data (public repo)

This is a public repository. **Never commit device-identifying or secret data:**
serial numbers, LAN/device IP addresses, credentials, tokens, or private keys.
Use placeholders instead (`FOX_HOST`, `<your-device-ip>`, `docker/.env` — which is
git-ignored).

A [gitleaks](https://github.com/gitleaks/gitleaks) scan enforces this in two places:

- **Locally** via the `gitleaks` pre-commit hook (`pre-commit install` enables it).
- **In CI** via the required `secret-scan` job on every push and PR.

Rules and allowlisted placeholders live in `.gitleaks.toml`. Run it yourself:

```bash
gitleaks detect --source . --no-git --config .gitleaks.toml --redact -v
```

If it flags a legitimate value (e.g. a new documented placeholder), add a narrow
entry to the `.gitleaks.toml` allowlist rather than disabling the rule.

## Adding a device / model

Prefer adding a model definition to the registry over changing core logic; the
architecture is designed to extend by data, not code.
