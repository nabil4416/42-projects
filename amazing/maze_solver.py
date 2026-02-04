#!/usr/bin/env python3
"""
Shortest path solver for A-Maze-ing.

This module finds a valid shortest path from ENTRY to EXIT using BFS.
The path is returned as a string of letters: N, E, S, W.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, Final, Tuple

from maze_generator import Maze
from maze_types import WALL_E, WALL_N, WALL_S, WALL_W, Point


# Directions are defined as:
# (dx, dy, wall_bit_in_current_cell, letter)
_DIRS: Final[Tuple[Tuple[int, int, int, str], ...]] = (
    (0, -1, WALL_N, "N"),
    (1, 0, WALL_E, "E"),
    (0, 1, WALL_S, "S"),
    (-1, 0, WALL_W, "W"),
)


class MazeSolveError(Exception):
    """Raised when no valid path can be found or inputs are invalid."""


@dataclass(frozen=True)
class _Prev:
    """Store predecessor and move letter used to reach a cell."""
    prev: Tuple[int, int]
    move: str


def solve_shortest_path(maze: Maze, entry: Point, exit_: Point) -> str:
    """
    Compute a shortest valid path from entry to exit using BFS.

    Args:
        maze: The Maze structure (wall bits per cell).
        entry: Start position.
        exit_: Goal position.

    Returns:
        A string composed of 'N', 'E', 'S', 'W'.

    Raises:
        MazeSolveError: If entry/exit are invalid or no path exists.
    """
    if not maze.in_bounds(entry):
        raise MazeSolveError("ENTRY is out of maze bounds.")
    if not maze.in_bounds(exit_):
        raise MazeSolveError("EXIT is out of maze bounds.")
    if entry == exit_:
        return ""

    start = (entry.x, entry.y)
    goal = (exit_.x, exit_.y)

    q: Deque[Tuple[int, int]] = deque()
    q.append(start)

    seen: set[Tuple[int, int]] = set()
    seen.add(start)

    prev: Dict[Tuple[int, int], _Prev] = {}

    while q:
        cx, cy = q.popleft()

        if (cx, cy) == goal:
            break

        cur_point = Point(cx, cy)
        cur_bits = maze.get(cur_point)

        for dx, dy, wall_bit, letter in _DIRS:
            nx = cx + dx
            ny = cy + dy
            nxt = (nx, ny)

            if nx < 0 or ny < 0 or nx >= maze.width or ny >= maze.height:
                continue
            if nxt in seen:
                continue

            # If the wall in the current cell is OPEN, we can move.
            if (cur_bits & wall_bit) == 0:
                seen.add(nxt)
                prev[nxt] = _Prev(prev=(cx, cy), move=letter)
                q.append(nxt)

    if goal not in prev:
        raise MazeSolveError("No path found from ENTRY to EXIT.")

    return _reconstruct_path(prev, start, goal)


def _reconstruct_path(
    prev: Dict[Tuple[int, int], _Prev],
    start: Tuple[int, int],
    goal: Tuple[int, int],
) -> str:
    """Rebuild the path string from predecessor links."""
    moves: list[str] = []
    cur = goal

    while cur != start:
        step = prev.get(cur)
        if step is None:
            raise MazeSolveError("Path reconstruction failed.")
        moves.append(step.move)
        cur = step.prev

    moves.reverse()
    return "".join(moves)
