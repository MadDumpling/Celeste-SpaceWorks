"""Compatibility layer for spacecraft provenance metadata.

This module re-exports the canonical provenance definitions used by the domain
models so imports like ``from spacecraft.provenance import DataProvenance`` keep
working without pulling in UI or OpenGL dependencies.
"""

from engineering.readiness.provenance import (
    QUALITIES,
    TRACEABLE_QUALITIES,
    DataProvenance,
    MissingDataError,
)

__all__ = [
    "QUALITIES",
    "TRACEABLE_QUALITIES",
    "DataProvenance",
    "MissingDataError",
]
