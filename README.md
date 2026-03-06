# 1980_Style_Adventure-Game

"Kingdom's Peril" — a text adventure game with a shared engine and two frontends. Written in Python.

Built for CS 3620 Server-Side Web Architecture. Grade: A.

I wrote this code myself. AI was used for concept research, not code generation.

## What it does

You play a character navigating a fantasy kingdom. There are multiple paths — hidden stairs, a grand hall, catacombs, a mystic pond, a druid circle. You collect items (horn, sword, medallion), solve riddles with limited retries and progressive hints, and your choices determine the outcome.

Two ways to play:
- **CLI** (`adventure_game.py`) — terminal-based, classic text adventure style
- **GUI** (`adventure_gui.py`) — Tkinter window with retro terminal visual effects

Both frontends use the same game engine. That separation was intentional.

## Architecture

```
game_engine.py      - Shared engine (~14KB), scene graph, game state
adventure_game.py   - CLI frontend
adventure_gui.py    - Tkinter GUI frontend
retro_monitor.py    - Visual effects for the GUI
```

The engine uses a scene graph architecture. Scenes and options are defined as dataclasses. The engine handles state, inventory, branching, and player name templating throughout story text. Frontends just handle input and display.

## Honesty

This is my code. The scene graph, the inventory system, the riddle mechanics, the engine/frontend separation — all mine. AI helped me research concepts around text adventure design, not write the implementation.
