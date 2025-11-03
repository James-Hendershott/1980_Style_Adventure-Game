# Kingdom's Peril — Adventure Game (CLI + GUI)

Kingdom's Peril is a retro, choose‑your‑own‑adventure game. It now uses a shared game engine so both the console (CLI) and the Tkinter GUI read from the same story.

What's included
- `game_engine.py` — shared story/scene graph, outcomes logging.
- `adventure_game.py` — console (CLI) front‑end.
- `adventure_gui.py` — simple Tkinter GUI front‑end.
- `adventure_outcomes.txt` — outcomes log (auto‑appended).

Highlights
- Multiple new paths and outcomes (in addition to the original flow):
	- Hidden stairs from the library leading to an observation tower and signal horn
	- Grand hall banquet detour (watch out for the poisoned feast!)
	- Catacombs with a skeletal sentry and a riddle
	- Mystic Pond branch with three boons
	- Druid circle riddle and more throne room approaches
- Player name templating — your chosen name appears in the story text.
- Inventory system — pick up items along the way (e.g., horn, sword, medallion).
- Riddle retries with hints — a couple of input scenes allow limited retries with progressive hints before failure.

Requirements
- Python 3.9+ (tested with 3.13 on Windows)
- Tkinter is bundled with most Python Windows installers. On Linux, you may need to install `python3-tk` from your package manager.

Quick start (Windows PowerShell)

1) Create and activate a virtual environment (recommended)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Run the console version (CLI)
```powershell
python .\adventure_game.py
```

3) Run the GUI (Tkinter)
```powershell
python .\adventure_gui.py
```

Gameplay notes
- Enter your knightly name when prompted (CLI) or when the GUI opens.
- In the CLI, type the option keys as shown (e.g., `1`, `left`, `a`). Type `i` to view your inventory at any choice prompt.
- Outcomes are appended to `adventure_outcomes.txt`. You can view them from the CLI menu or the GUI’s “View Past Outcomes.”
- In the GUI, there’s an “Inventory” button on choice screens to review your items.

Troubleshooting
- PowerShell execution policy blocks venv activation:
	```powershell
	Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
	.\.venv\Scripts\Activate.ps1
	```
- On Linux, if the GUI fails to start due to Tk missing, install system packages (e.g., `sudo apt-get install python3-tk`).

Development
- The story graph lives in `game_engine.py` (see the `Engine._build_scenes()` method). To add scenes or options, edit that graph once and both the CLI and GUI respect the changes.
- The engine exposes a `Session` with per‑run state (name, inventory, riddle attempts). Front‑ends use `ENGINE.new_session(name)` to play. Choice options can award items via `Option(item_gain="...")`. Input scenes can set `input_retries` and `input_hints` for guided puzzles.

Enjoy the quest!
