"""Schema loading and validation helpers for UAPF packages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from jsonschema import Draft202012Validator

SCHEMA_FILES: Dict[str, str] = {
    "manifest": "uapf-manifest.schema.json",
    "roles": "uapf-roles.schema.json",
    "capabilities": "uapf-capabilities.schema.json",
    "bindings": "uapf-bindings.schema.json",
    "mcp_tools": "uapf-mcp-tools.schema.json",
    "a2a_schemas": "uapf-a2a-schemas.schema.json",
}

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"


def _schema_path(name: str) -> Path:
    try:
        filename = SCHEMA_FILES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown schema: {name}") from exc

    path = SCHEMAS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {path}")
    return path


def load_schema(name: str) -> dict:
    """Load a JSON schema by friendly name."""

    path = _schema_path(name)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_validator(name: str) -> Draft202012Validator:
    """Create a Draft202012Validator for the requested schema."""

    schema = load_schema(name)
    return Draft202012Validator(schema)


def validate_manifest(data: dict) -> None:
    get_validator("manifest").validate(data)


def validate_roles(data: dict) -> None:
    get_validator("roles").validate(data)


def validate_capabilities(data: dict) -> None:
    get_validator("capabilities").validate(data)


def validate_bindings(data: dict) -> None:
    get_validator("bindings").validate(data)


def validate_mcp_tools(data: dict) -> None:
    get_validator("mcp_tools").validate(data)


def validate_a2a_schemas(data: dict) -> None:
    get_validator("a2a_schemas").validate(data)
