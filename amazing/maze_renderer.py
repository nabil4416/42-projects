#!/usr/bin/env python3
"""
Terminal ASCII renderer for A-Maze-ing.

Features:
- Display walls, entry, exit
- Optional show/hide shortest path
- Change wall colors
- Regenerate support is handled by the main loop (a_maze_ing.py)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from maze_generator import Maze
from maze_types import Point, WALL_E, WALL_N, WALL_S, WALL_W


_RESET: Final[str] = "\033[0m"

_WALL_COLORS: Final[list[str]] = [
    "\033[97m",  # white
    "\033[92m",  # green
    "\033[93m",  # yellow
    "\033[94m",  # blue
    "\033[95m",  # magenta
    "\033[96m",  # cyan
]


@dataclass
class RenderState:
    """Rendering options for the terminal view."""
    show_path: bool = False
    color_index: int = 0

    def next_color(self) -> None:
        """Cycle to the next wall color."""
        self.color_index = (self.color_index + 1) % len(_WALL_COLORS)

    def wall_color(self) -> str:
        """Return ANSI color code for walls."""
        return _WALL_COLORS[self.color_index]


def render_maze(
    maze: Maze,
    entry: Point,
    exit_: Point,
    path: str,
    state: RenderState,
) -> str:
    """
    Render the maze as ASCII.

    Returns:
        A string representing the maze to print.
    """
    path_cells = _path_to_cells(entry, path) if state.show_path else set()
    color = state.wall_color()

    lines: list[str] = []
    lines.append(_top_border(maze, color))

    for y in range(maze.height):
        lines.extend(_render_row(maze, y, entry, exit_, path_cells, color))

    lines.append(_help_line(state))
    return "\n".join(lines)


def _top_border(maze: Maze, color: str) -> str:
    """Render the top border based on North walls of first row."""
    parts = [color, "+"]
    for x in range(maze.width):
        cell = maze.cells[0][x]
        if (cell & WALL_N) != 0:
            parts.append("---+")
        else:
            parts.append("   +")
    parts.append(_RESET)
    return "".join(parts)


def _render_row(
    maze: Maze,
    y: int,
    entry: Point,
    exit_: Point,
    path_cells: set[tuple[int, int]],
    color: str,
) -> list[str]:
    """Render a row as two lines: vertical walls + bottom walls."""
    line_cells = [color]
    line_bottom = [color, "+"]

    for x in range(maze.width):
        p = Point(x, y)
        bits = maze.get(p)

        # West wall
        if x == 0:
            if (bits & WALL_W) != 0:
                line_cells.append("|")
            else:
                line_cells.append(" ")

        # Cell content (3 chars)
        line_cells.append(_cell_content(p, entry, exit_, path_cells))

        # East wall
        if (bits & WALL_E) != 0:
            line_cells.append("|")
        else:
            line_cells.append(" ")

        # Bottom border for this cell
        if (bits & WALL_S) != 0:
            line_bottom.append("---+")
        else:
            line_bottom.append("   +")

    line_cells.append(_RESET)
    line_bottom.append(_RESET)

    return ["".join(line_cells), "".join(line_bottom)]


def _cell_content(
    p: Point,
    entry: Point,
    exit_: Point,
    path_cells: set[tuple[int, int]],
) -> str:
    """Choose what to display inside the cell."""
    if p == entry:
        return " E "
    if p == exit_:
        return " X "
    if (p.x, p.y) in path_cells:
        return " . "
    return "   "


def _path_to_cells(entry: Point, path: str) -> set[tuple[int, int]]:
    """Convert a path string (NESW) into
    the set of visited cell coordinates."""
    x = entry.x
    y = entry.y
    visited: set[tuple[int, int]] = set()
    visited.add((x, y))

    for ch in path:
        if ch == "N":
            y -= 1
        elif ch == "E":
            x += 1
        elif ch == "S":
            y += 1
        elif ch == "W":
            x -= 1
        visited.add((x, y))

    return visited


def _help_line(state: RenderState) -> str:
    """Render a small help / status line."""
    on_off = "ON" if state.show_path else "OFF"
    return f"[r]egenerate  [p]ath:{on_off}  [c]olor  [q]uit"
