#!/usr/bin/env python3
"""
Shared types and constants for the A-Maze-ing project.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


# Wall bit mapping (must match the subject):
# bit 0: North, bit 1: East, bit 2: South, bit 3: West
WALL_N: Final[int] = 1 << 0
WALL_E: Final[int] = 1 << 1
WALL_S: Final[int] = 1 << 2
WALL_W: Final[int] = 1 << 3


@dataclass(frozen=True)
class Point:
    """Simple 2D point (x, y) used for ENTRY and EXIT coordinates."""
    x: int
    y: int


@dataclass(frozen=True)
class MazeConfig:
    """Validated configuration read from the config file."""
    width: int
    height: int
    entry: Point
    exit: Point
    output_file: str
    perfect: bool
    seed: int | None = None
