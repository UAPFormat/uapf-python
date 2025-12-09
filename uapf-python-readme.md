# uapf-python

Official **Python parser & validator** for [UAPF](https://github.com/UAPFormat/UAPF-spec) packages.

This library loads `.uapf` archives, validates them against the official JSON Schemas, and exposes a Pythonic API for working with workflows, decisions, agents, and integration metadata.

> Status: Early draft – API may change before UAPF v1.0.

---

## Installation

Until a package is published to PyPI, install from source:

```bash
git clone https://github.com/UAPFormat/uapf-python.git
cd uapf-python
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -e .
```

---

## Quick example

```python
from uapf_parser import UAPFPackage

# Load from a .uapf file (zip archive)
pkg = UAPFPackage.from_file("examples/acme-docflow.uapf")

# Validate against the official JSON Schemas
pkg.validate()  # raises UAPFValidationError on failure

# Access core sections
print(pkg.manifest.id, pkg.manifest.version)
print(pkg.agents.roles)
print(pkg.integration.mcp_tools)
```

(Adapt names to the actual classes/functions you expose.)

---

## Features

- **Package handling**
  - Open `.uapf` archives from disk or file-like objects.
  - Inspect raw contents (manifest, BPMN/DMN/CMMN XML, JSON sections).

- **Schema validation**
  - Validates against schemas from [`UAPF-spec`](https://github.com/UAPFormat/UAPF-spec).
  - Clear error reporting with JSON-pointer-like paths.

- **Convenience accessors**
  - Typed access to `manifest`, `agents`, `decisions`, `integration`, `metadata`.
  - Helpers for listing agent roles, capabilities, and tool bindings.

---

## Roadmap

Planned enhancements:

- CLI: `uapf-validate path/to/package.uapf`
- Rich error types and human-friendly messages.
- Helpers for building `.uapf` packages programmatically.
- Integration with `uapf-conformance` fixtures.

---

## Development

```bash
git clone https://github.com/UAPFormat/uapf-python.git
cd uapf-python
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Contributions are welcome:

- Better error messages and typing.
- Additional helpers for agent/orchestrator frameworks.
- Documentation and examples.

---

## License

MIT – see [`LICENSE`](LICENSE).
