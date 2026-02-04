#!/usr/bin/env python3
"""
A-Maze-ing main entrypoint.

Usage:
    python3 a_maze_ing.py config.txt
"""

from __future__ import annotations

import sys

from config_parser import ConfigError, parse_config_file
from maze_generator import MazeGenerator
from maze_renderer import RenderState, render_maze
from maze_solver import MazeSolveError, solve_shortest_path
from maze_writer import MazeOutputError, write_maze_output


def main(argv: list[str]) -> int:
    """Program entrypoint. Returns an exit code."""
    if len(argv) != 2:
        print("Error: expected exactly one argument:")
        print("  config file path")
        print("Usage: python3 a_maze_ing.py config.txt")
        return 2

    config_path = argv[1]

    try:
        cfg = parse_config_file(config_path)
    except ConfigError as exc:
        print(f"Error: {exc}")
        return 1

    state = RenderState(show_path=False, color_index=0)

    seed = cfg.seed

    while True:
        try:
            gen = MazeGenerator(cfg.width, cfg.height, seed)
            maze = gen.generate()
            path = solve_shortest_path(maze, cfg.entry, cfg.exit)
            write_maze_output(cfg.output_file, maze, cfg.entry, cfg.exit, path)
        except (MazeOutputError, MazeSolveError, Exception) as exc:
            print(f"Error: {exc}")
            return 1

        print(render_maze(maze, cfg.entry, cfg.exit, path, state))
        print(f"OK: wrote output to {cfg.output_file}")

        cmd = input("Command (r/p/c/q): ").strip().lower()

        if cmd == "q":
            break
        if cmd == "p":
            state.show_path = not state.show_path
            continue
        if cmd == "c":
            state.next_color()
            continue
        if cmd == "r":
            if seed is not None:
                seed += 1
            continue

        print("Unknown command. Use r, p, c, q.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
