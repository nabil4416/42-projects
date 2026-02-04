#!/usr/bin/env python3
"""
Parse and validate the KEY=VALUE configuration file for A-Maze-ing.

Rules:
- One KEY=VALUE per line
- Lines starting with '#' are comments and must be ignored
- Mandatory keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from maze_types import MazeConfig, Point


class ConfigError(Exception):
    """Raised when the configuration file is missing or invalid."""


def _parse_bool(text: str) -> bool:
    """Parse a boolean from a string like 'True' or 'False'."""
    t = text.strip().lower()
    if t in ("true", "1", "yes"):
        return True
    if t in ("false", "0", "no"):
        return False
    raise ConfigError(f"Invalid boolean value: {text!r}")


def _parse_int(text: str) -> int:
    """Parse an integer from a string."""
    try:
        return int(text.strip())
    except ValueError as exc:
        raise ConfigError(f"Invalid integer value: {text!r}") from exc


def _parse_point(text: str) -> Point:
    """Parse 'x,y' into a Point."""
    raw = text.strip()
    parts = raw.split(",")
    if len(parts) != 2:
        msg = "Invalid coordinate format (expected x,y): "
        raise ConfigError(msg + repr(text))
    x = _parse_int(parts[0])
    y = _parse_int(parts[1])
    return Point(x=x, y=y)


def _validate_bounds(cfg: MazeConfig) -> None:
    """Validate entry/exit bounds and basic consistency."""
    if cfg.width <= 0 or cfg.height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be positive integers.")

    def inside(p: Point) -> bool:
        return 0 <= p.x < cfg.width and 0 <= p.y < cfg.height

    if not inside(cfg.entry):
        raise ConfigError("ENTRY is out of maze bounds.")
    if not inside(cfg.exit):
        raise ConfigError("EXIT is out of maze bounds.")
    if cfg.entry == cfg.exit:
        raise ConfigError("ENTRY and EXIT must be different.")


def parse_config_file(path: str) -> MazeConfig:
    """
    Read and validate the config file.

    Returns:
        MazeConfig: validated configuration.

    Raises:
        ConfigError: for any invalid config or missing file.
    """
    p = Path(path)

    if not p.exists():
        raise ConfigError(f"Config file not found: {path}")
    if not p.is_file():
        raise ConfigError(f"Config path is not a file: {path}")

    raw_map: Dict[str, str] = {}

    try:
        with p.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                if "=" not in stripped:
                    bad = line.rstrip()
                    raise ConfigError(
                        f"Bad syntax at line {line_no}: {bad!r}"
                    )
                key, value = stripped.split("=", 1)
                key = key.strip().upper()
                value = value.strip()
                if not key:
                    raise ConfigError(f"Empty key at line {line_no}.")
                raw_map[key] = value
    except OSError as exc:
        raise ConfigError(f"Cannot read config file: {path}") from exc

    mandatory = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")
    for k in mandatory:
        if k not in raw_map:
            raise ConfigError(f"Missing mandatory key: {k}")

    width = _parse_int(raw_map["WIDTH"])
    height = _parse_int(raw_map["HEIGHT"])
    entry = _parse_point(raw_map["ENTRY"])
    exit_ = _parse_point(raw_map["EXIT"])

    output_file = raw_map["OUTPUT_FILE"].strip()
    if not output_file:
        raise ConfigError("OUTPUT_FILE must not be empty.")

    perfect = _parse_bool(raw_map["PERFECT"])

    seed: Optional[int] = None
    if "SEED" in raw_map:
        seed = _parse_int(raw_map["SEED"])

    cfg = MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
    _validate_bounds(cfg)
    return cfg
