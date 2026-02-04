#!/usr/bin/env python3
"""
Output writer for A-Maze-ing.

Writes:
- the maze grid as hex digits (1 per cell), row by row
- an empty line
- entry coordinates on one line
- exit coordinates on one line
- shortest path as N/E/S/W on one line
"""

from __future__ import annotations

from pathlib import Path

from maze_generator import Maze
from maze_types import Point


class MazeOutputError(Exception):
    """Raised when the maze output cannot be written or is invalid."""


def write_maze_output(
    output_file: str,
    maze: Maze,
    entry: Point,
    exit_: Point,
    path: str,
) -> None:
    """
    Write the maze output file in the required format.

    Args:
        output_file: destination filename.
        maze: maze structure (wall bits per cell).
        entry: entry coordinates.
        exit_: exit coordinates.
        path: shortest path string using N/E/S/W.

    Raises:
        MazeOutputError: on invalid inputs or file write errors.
    """
    if maze.width <= 0 or maze.height <= 0:
        raise MazeOutputError("Maze dimensions must be positive.")
    if not maze.in_bounds(entry):
        raise MazeOutputError("ENTRY is out of maze bounds.")
    if not maze.in_bounds(exit_):
        raise MazeOutputError("EXIT is out of maze bounds.")

    _validate_path_letters(path)

    lines: list[str] = []
    lines.extend(_maze_to_hex_lines(maze))
    lines.append("")  # empty line
    lines.append(_format_point(entry))
    lines.append(_format_point(exit_))
    lines.append(path)

    data = "\n".join(lines) + "\n"
    _write_text_file(output_file, data)


def _maze_to_hex_lines(maze: Maze) -> list[str]:
    """Convert the maze grid to a list of hex strings, one row per line."""
    out: list[str] = []
    for y in range(maze.height):
        row_cells = maze.cells[y]
        if len(row_cells) != maze.width:
            raise MazeOutputError("Maze row length mismatch.")
        row = "".join(_cell_to_hex_digit(v) for v in row_cells)
        out.append(row)
    return out


def _cell_to_hex_digit(value: int) -> str:
    """Convert a cell wall-bit value (0..15) into an uppercase hex digit."""
    if value < 0 or value > 15:
        raise MazeOutputError("Cell value must be between 0 and 15.")
    return format(value, "X")


def _format_point(p: Point) -> str:
    """Format a Point as 'x,y'."""
    return f"{p.x},{p.y}"


def _validate_path_letters(path: str) -> None:
    """Ensure the path contains only N/E/S/W letters."""
    allowed = {"N", "E", "S", "W"}
    for ch in path:
        if ch not in allowed:
            raise MazeOutputError("Path contains invalid direction letters.")


def _write_text_file(filename: str, data: str) -> None:
    """Write UTF-8 text to filename safely."""
    p = Path(filename)
    try:
        with p.open("w", encoding="utf-8") as f:
            f.write(data)
    except OSError as exc:
        raise MazeOutputError(f"Cannot write output file: {filename}") from exc
