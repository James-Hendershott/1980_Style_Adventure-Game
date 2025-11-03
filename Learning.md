# Learning Notes — Kingdom's Peril (Living Doc)

This document explains what we changed and why, with concise rationale and practical tips for extending the game. We’ll keep updating it alongside changes.

Last updated: 2025-11-03

## 1) Starting point and goals
- Initial repo: single-file CLI adventure `adventure_game.py`.
- Goals:
  - Make it easy to launch.
  - Expand the story.
  - (Later) Add a GUI.
  - Avoid duplicated story logic between CLI and GUI.

## 2) Cleanup and documentation
- Removed an accidental Django project folder to simplify the repo.
- Wrote/updated `README.md` with clear Windows PowerShell run steps and quick troubleshooting.
- Rationale: Lower friction to run and contribute.

## 3) GUI addition (Tkinter)
- Added `adventure_gui.py` using Tkinter (standard library on Windows) to offer a simple window with buttons for choices.
- Rationale: Provide a friendly front-end while keeping the CLI for quick testing.

## 4) Shared game engine
- Created `game_engine.py` containing:
  - Scene graph (choice scenes + input/riddle scenes).
  - Transition helpers for choices and inputs.
  - Outcome logging to `adventure_outcomes.txt`.
- Refactored CLI and GUI to depend on the engine.
- Rationale: Single source of truth for story and logic, easier to expand safely.

## 5) Story expansion highlights
- Added branches: secret library + hidden stairs; grand hall/banquet detour; catacombs w/ riddle; mystic pond; druid riddle.
- Rationale: More replayability and classic adventure variety.

## 6) Stateful play: name templating, inventory, riddle hints
- Introduced a `Session` in the engine for per-run state:
  - Player name (applied in text via `{name}` templating).
  - Inventory (items gained via `Option(item_gain="...")`).
  - Limited riddle retries with progressive hints (`input_retries`, `input_hints`).
- Wired both front-ends to use `ENGINE.new_session(name)`:
  - CLI: type `i` at choice prompts to view inventory.
  - GUI: “Inventory” button on choice screens.
- Rationale: More immersion without complicating content editing.

## 7) How to add/modify story
- In `Engine._build_scenes()`:
  - Choice scene:
    ```py
    Scene(
      id="some_room",
      text="Welcome {name}...",
      options=[
        Option("1", "Go north", next_id="north" , outcome="Found the northern path", item_gain="map"),
        Option("2", "Open chest", fatal=True, outcome="Poisoned by trap"),
      ],
    )
    ```
  - Input scene (riddle):
    ```py
    Scene(
      id="riddle_gate",
      type="input",
      text="Speak the secret word",
      input_correct={"echo": ("next_scene", "Solved the riddle")},
      input_fatal_outcome="Failed the riddle",
      input_retries=2,
      input_hints=["It repeats.", "Canyons make it louder."],
    )
    ```
- Use `{name}` inside scene text to personalize.
- Use `item_gain` if a choice should award an item.

## 8) Next improvement ideas
- Item-gated options (e.g., only blow horn if you actually have it) and alternate endings based on inventory.
- Simple saves (JSON) + load/resume.
- Unit tests for engine transitions and input handling.

## 9) Quick run reference (Windows PowerShell)
- CLI:
  ```powershell
  python .\adventure_game.py
  ```
- GUI (Tkinter):
  ```powershell
  python .\adventure_gui.py
  ```

## 10) Troubleshooting checklist
- Ensure you’re in the repo folder before running.
- Verify Python version: `python --version` (3.9+ recommended).
- Virtual env: `python -m venv .venv; .\.venv\Scripts\Activate.ps1`.
- Tkinter errors on Windows are rare. If you see one, share the exact error text.

---
We’ll keep this Learning.md updated as we change the codebase. If you want to add design notes or TODOs here, feel free to append a section at the end.
