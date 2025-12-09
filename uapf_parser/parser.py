"""UAPF package loader and validator."""

from __future__ import annotations

import json
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable

from . import validators


@dataclass
class UAPFPackage:
    manifest: Dict[str, Any]
    roles: Dict[str, Any]
    capabilities: Dict[str, Any]
    bindings: Dict[str, Any]
    mcp_tools: Dict[str, Any]
    a2a_schemas: Dict[str, Any]
    raw_files: Dict[str, bytes]


def _read_json(zf: zipfile.ZipFile, path: str) -> Dict[str, Any]:
    try:
        with zf.open(path) as handle:
            return json.load(handle)
    except KeyError as exc:
        raise FileNotFoundError(f"Missing required file in archive: {path}") from exc


def _find_component(components: Iterable[str], filename: str) -> str:
    for path in components:
        if path.endswith(filename):
            return path
    raise ValueError(f"manifest.json components must include {filename}")


def load_uapf(path: str, validate: bool = True) -> UAPFPackage:
    """Load a .uapf archive and optionally validate its JSON payloads."""

    archive_path = Path(path)
    if not archive_path.exists():
        raise FileNotFoundError(f"UAPF archive not found: {path}")

    with zipfile.ZipFile(archive_path, "r") as zf:
        manifest = _read_json(zf, "manifest.json")

        if validate:
            validators.validate_manifest(manifest)

        components = manifest.get("components") or {}
        agents = components.get("agents") or []
        integration = components.get("integration") or []

        roles_path = _find_component(agents, "roles.json")
        capabilities_path = _find_component(agents, "capabilities.json")
        bindings_path = _find_component(agents, "bindings.json")
        mcp_tools_path = _find_component(integration, "mcp-tools.json")
        a2a_schemas_path = _find_component(integration, "a2a-schemas.json")

        roles = _read_json(zf, roles_path)
        capabilities = _read_json(zf, capabilities_path)
        bindings = _read_json(zf, bindings_path)
        mcp_tools = _read_json(zf, mcp_tools_path)
        a2a_schemas = _read_json(zf, a2a_schemas_path)

        if validate:
            validators.validate_roles(roles)
            validators.validate_capabilities(capabilities)
            validators.validate_bindings(bindings)
            validators.validate_mcp_tools(mcp_tools)
            validators.validate_a2a_schemas(a2a_schemas)

        raw_files: Dict[str, bytes] = {}
        for info in zf.infolist():
            raw_files[info.filename] = zf.read(info.filename)

    return UAPFPackage(
        manifest=manifest,
        roles=roles,
        capabilities=capabilities,
        bindings=bindings,
        mcp_tools=mcp_tools,
        a2a_schemas=a2a_schemas,
        raw_files=raw_files,
    )


def validate_uapf(path: str) -> None:
    """Validate a UAPF archive against all schemas."""

    load_uapf(path, validate=True)
