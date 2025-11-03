# Kingdom's Peril — Text Adventure

This is a standalone, text-based adventure game implemented in `adventure_game.py`.

What changed
- The accidental `retro_adventure_game/` Django app was removed from the repo (core files removed). If you need any files recovered, let me know before pushing.
- The console game script (`adventure_game.py`) was extended with an additional story branch (the "Mystic Pond").

Quick start (Windows PowerShell)

1. Open PowerShell in the project root (where `adventure_game.py` lives).

2. (Recommended) create and activate a venv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Run the game:

```powershell
python .\adventure_game.py
```

Gameplay notes
- Enter a knightly name when prompted.
- Choose options exactly as shown (e.g., `1`, `castle`, `A`, `a`).
- Outcomes are appended to `adventure_outcomes.txt` in the repo root.

If you want me to remove every leftover empty directory for `retro_adventure_game/` or to fully purge it from git history, I can do that next (I can also create a small README in its place if you prefer to keep a note). 

Enjoy the quest!
