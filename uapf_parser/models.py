"""Dataclass models for common UAPF concepts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Role:
    id: str
    description: Optional[str] = None


@dataclass
class CapabilityBinding:
    taskId: str
    agent: str
    mode: str
    dmnDecisionRef: Optional[str] = None


@dataclass
class CapabilitySet:
    agent: str
    capabilities: List[str]
