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
- In the CLI, type the option keys as shown (e.g., `1`, `left`, `a`).
- Outcomes are appended to `adventure_outcomes.txt`. You can view them from the CLI menu or the GUI’s “View Past Outcomes.”

Troubleshooting
- PowerShell execution policy blocks venv activation:
	```powershell
	Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
	.\.venv\Scripts\Activate.ps1
	```
- On Linux, if the GUI fails to start due to Tk missing, install system packages (e.g., `sudo apt-get install python3-tk`).

Development
- The story graph lives in `game_engine.py` (see the `Engine._build_scenes()` method). To add scenes or options, edit that graph once and both the CLI and GUI respect the changes.

Enjoy the quest!
