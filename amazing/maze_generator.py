#!/usr/bin/env python3
"""
Maze generation logic for A-Maze-ing.

This module focuses on the *data* and *generation* only:
- no config parsing
- no file writing
- no rendering

It produces a grid of cells, each cell storing wall bits:
bit0=N, bit1=E, bit2=S, bit3=W
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Final, List, Set, Tuple

from maze_types import WALL_E, WALL_N, WALL_S, WALL_W, Point


_DIRS: Final[List[Tuple[int, int, int, int]]] = [
    # (dx, dy, wall_bit_in_current, wall_bit_in_neighbor)
    (0, -1, WALL_N, WALL_S),
    (1, 0, WALL_E, WALL_W),
    (0, 1, WALL_S, WALL_N),
    (-1, 0, WALL_W, WALL_E),
]


@dataclass
class Maze:
    """
    Maze grid storing wall bits per cell.

    A wall bit set to 1 means the wall is CLOSED.
    A bit set to 0 means the wall is OPEN.
    """
    width: int
    height: int
    cells: List[List[int]]

    def in_bounds(self, p: Point) -> bool:
        """Return True if point is inside the maze bounds."""
        return 0 <= p.x < self.width and 0 <= p.y < self.height

    def get(self, p: Point) -> int:
        """Get wall bits for a cell."""
        return self.cells[p.y][p.x]

    def set(self, p: Point, value: int) -> None:
        """Set wall bits for a cell."""
        self.cells[p.y][p.x] = value


class MazeGenerationError(Exception):
    """Raised when maze generation cannot meet constraints."""


class MazeGenerator:
    """
    Generate a coherent maze.

    This first version focuses on:
    - randomness + reproducibility via seed
    - wall coherence between neighboring cells
    - full connectivity (no isolated cells)
    """

    def __init__(self, width: int, height: int, seed: int | None = None) -> None:
        if width <= 0 or height <= 0:
            raise MazeGenerationError("width and height must be > 0")
        self._width = width
        self._height = height
        self._rng = random.Random(seed)

    def generate(self) -> Maze:
        """
        Generate a maze.

        Returns:
            Maze: a coherent, fully connected maze.
        """
        maze = self._init_full_walls()

        # Use a simple randomized DFS "recursive backtracker" style,
        # implemented iteratively to keep control and readability.
        start = Point(0, 0)
        visited: Set[Tuple[int, int]] = set()
        stack: List[Point] = [start]
        visited.add((start.x, start.y))

        while stack:
            current = stack[-1]
            neighbors = self._unvisited_neighbors(current, visited)

            if not neighbors:
                stack.pop()
                continue

            nx, ny, w_cur, w_nbr = self._rng.choice(neighbors)
            neighbor = Point(nx, ny)

            self._open_wall_both(maze, current, neighbor, w_cur, w_nbr)
            visited.add((neighbor.x, neighbor.y))
            stack.append(neighbor)

        # Safety: ensure full connectivity (should already be true)
        if not self._is_fully_connected(maze, start):
            raise MazeGenerationError("generated maze is not fully connected")

        return maze

    def _init_full_walls(self) -> Maze:
        """Create a maze with all walls closed in every cell."""
        full = WALL_N | WALL_E | WALL_S | WALL_W
        cells = [[full for _ in range(self._width)] for _ in range(self._height)]
        return Maze(width=self._width, height=self._height, cells=cells)

    def _unvisited_neighbors(
        self,
        p: Point,
        visited: Set[Tuple[int, int]],
    ) -> List[Tuple[int, int, int, int]]:
        """
        Return a list of unvisited neighbors with wall-bit pairing info.

        Each item: (nx, ny, wall_bit_current, wall_bit_neighbor)
        """
        out: List[Tuple[int, int, int, int]] = []
        for dx, dy, w_cur, w_nbr in _DIRS:
            nx = p.x + dx
            ny = p.y + dy
            if 0 <= nx < self._width and 0 <= ny < self._height:
                if (nx, ny) not in visited:
                    out.append((nx, ny, w_cur, w_nbr))
        return out

    def _open_wall_both(
        self,
        maze: Maze,
        a: Point,
        b: Point,
        wall_a: int,
        wall_b: int,
    ) -> None:
        """
        Open the wall between a and b in BOTH cells (coherence guarantee).
        """
        maze.set(a, maze.get(a) & ~wall_a)
        maze.set(b, maze.get(b) & ~wall_b)

    def _is_fully_connected(self, maze: Maze, start: Point) -> bool:
        """Check all cells are reachable from start using BFS on openings."""
        seen: Set[Tuple[int, int]] = set()
        q: List[Point] = [start]
        seen.add((start.x, start.y))

        while q:
            cur = q.pop(0)
            cur_bits = maze.get(cur)

            for dx, dy, w_cur, _w_nbr in _DIRS:
                nx = cur.x + dx
                ny = cur.y + dy
                if nx < 0 or ny < 0 or nx >= maze.width or ny >= maze.height:
                    continue

                # If wall is open, we can move.
                if (cur_bits & w_cur) == 0:
                    key = (nx, ny)
                    if key not in seen:
                        seen.add(key)
                        q.append(Point(nx, ny))

        return len(seen) == maze.width * maze.height
