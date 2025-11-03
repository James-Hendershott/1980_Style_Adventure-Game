"""Shared game engine for Kingdom's Peril.

Defines a simple scene graph and helpers to navigate the adventure.
Front-ends (CLI and GUI) should render scenes and call `apply_choice`
or `apply_input` to advance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Literal
import os


OUTCOMES_FILE = os.path.join(os.path.dirname(__file__), "adventure_outcomes.txt")


def save_outcome(text: str) -> None:
    with open(OUTCOMES_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def read_outcomes() -> str:
    if not os.path.exists(OUTCOMES_FILE):
        return "No outcomes recorded yet."
    with open(OUTCOMES_FILE, "r", encoding="utf-8") as f:
        contents = f.read().strip()
        return contents if contents else "No outcomes recorded yet."


SceneType = Literal["choice", "input", "end", "fatal"]


@dataclass
class Option:
    key: str
    label: str
    next_id: Optional[str] = None
    outcome: Optional[str] = None
    fatal: bool = False


@dataclass
class Scene:
    id: str
    text: str
    type: SceneType = "choice"
    options: List[Option] = field(default_factory=list)
    # For type == "input": map of lowercase accepted answers to (next_id, outcome)
    input_correct: Dict[str, Tuple[str, Optional[str]]] = field(default_factory=dict)
    # When wrong input leads to fatal outcome
    input_fatal_outcome: Optional[str] = None


class Engine:
    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self.start_id = "castle_or_forest"
        self._build_scenes()

    # --- Public helpers ---
    def get_scene(self, scene_id: str) -> Scene:
        return self.scenes[scene_id]

    def apply_choice(self, scene_id: str, key: str) -> Tuple[str, Optional[str], bool, bool]:
        """Apply a choice for a 'choice' scene.

        Returns: (next_scene_id, outcome_saved, is_fatal_end, is_end)
        """
        scene = self.get_scene(scene_id)
        key_low = key.strip().lower()
        for opt in scene.options:
            if opt.key.lower() == key_low:
                if opt.outcome:
                    save_outcome(opt.outcome)
                if opt.fatal:
                    return ("end_fatal", opt.outcome, True, True)
                if opt.next_id is None:
                    return ("end", opt.outcome, False, True)
                return (opt.next_id, opt.outcome, False, False)
        raise ValueError(f"Invalid choice '{key}' for scene '{scene_id}'")

    def apply_input(self, scene_id: str, value: str) -> Tuple[str, Optional[str], bool, bool]:
        """Apply text input for an 'input' scene."""
        scene = self.get_scene(scene_id)
        ans = value.strip().lower()
        if ans in scene.input_correct:
            next_id, outcome = scene.input_correct[ans]
            if outcome:
                save_outcome(outcome)
            return (next_id, outcome, False, False)
        # wrong -> fatal
        if scene.input_fatal_outcome:
            save_outcome(scene.input_fatal_outcome)
        return ("end_fatal", scene.input_fatal_outcome, True, True)

    # --- Scene graph ---
    def _build_scenes(self):
        add = self._add

        # Start choice: castle vs forest
        add(Scene(
            id="castle_or_forest",
            text=(
                "You are on a quest to rescue Princess Elara. Legend says she's held in the "
                "ancient Crimson Castle. Dark forests surround the castle grounds.\n\n"
                "Where do you go?"
            ),
            options=[
                Option("castle", "Head to the castle gates", next_id="castle_entrance"),
                Option("forest", "Take the dangerous forest path", next_id="forest_path"),
            ],
        ))

        # Castle entrance
        add(Scene(
            id="castle_entrance",
            text=(
                "You stand before massive gates. In the courtyard you see:\n"
                "1) A guarded main entrance\n2) A suspiciously quiet side entrance"
            ),
            options=[
                Option("1", "Guarded main entrance", next_id="main_entrance"),
                Option("2", "Quiet side entrance", next_id="side_entrance_riddle"),
            ],
        ))

        # Main entrance
        add(Scene(
            id="main_entrance",
            text="Guards spot you! Choose: A) Fight  B) Diplomacy  C) Distraction",
            options=[
                Option("a", "Fight your way through", fatal=True, outcome="Fell in main entrance combat"),
                Option("b", "Attempt diplomacy", next_id="grand_hall", outcome="Heroically gained entry"),
                Option("c", "Create a distraction", next_id="grand_hall", outcome="Slipped past guards"),
            ],
        ))

        # Side entrance riddle (input)
        add(Scene(
            id="side_entrance_riddle",
            type="input",
            text=(
                "A magical barrier asks: What comes once in a minute, twice in a moment, "
                "but never in a thousand years? (enter a single letter)"
            ),
            input_correct={"m": ("secret_library", "Solved side entrance riddle")},
            input_fatal_outcome="Failed side entrance riddle",
        ))

        # Secret library
        add(Scene(
            id="secret_library",
            text=(
                "In an ancient library you see:\n"
                "1) A glowing crystal orb\n2) A dusty tome bound in chains\n3) A hidden lever behind an atlas"
            ),
            options=[
                Option("1", "Study the orb", next_id="dungeon_path"),
                Option("2", "Open the tome", fatal=True, outcome="Driven mad by ancient tome"),
                Option("3", "Pull the lever", next_id="hidden_stairs", outcome="Found secret stairs from the library"),
            ],
        ))

        add(Scene(
            id="hidden_stairs",
            text=(
                "The lever opens hidden stairs up to a quiet observation tower. A signal horn rests on a ledge."
            ),
            options=[
                Option("signal", "Blow the horn to call allies", next_id="throne_room", outcome="Allies rallied to your cause"),
                Option("sneak", "Sneak back down toward the throne room", next_id="throne_room"),
            ],
        ))

        # Grand hall
        add(Scene(
            id="grand_hall",
            text=(
                "You enter the grand hall. Paths branch:\n"
                "left) Balcony noises\nright) Singing below\ncenter) Banquet tables"
            ),
            options=[
                Option("left", "Go to the balcony", next_id="balcony_path"),
                Option("right", "Descend to the dungeons", next_id="dungeons"),
                Option("center", "Inspect the banquet tables", next_id="banquet"),
            ],
        ))

        add(Scene(
            id="banquet",
            text=(
                "A feast lies abandoned. The food looks tempting."
            ),
            options=[
                Option("feast", "Eat to regain strength", fatal=True, outcome="Fell to poisoned feast"),
                Option("sneak", "Hide beneath the table and sneak onward", next_id="throne_room", outcome="Snuck past the guards from the banquet"),
            ],
        ))

        # Balcony
        add(Scene(
            id="balcony_path",
            text="Princess Elara is chained on the balcony. The Dark Vizier appears. Fight or Rescue?",
            options=[
                Option("fight", "Fight the Vizier", fatal=True, outcome="Defeated by Dark Vizier"),
                Option("rescue", "Rescue the princess", next_id=None, outcome="Heroically rescued princess"),
            ],
        ))

        # Dungeons
        add(Scene(
            id="dungeons",
            text=(
                "Dark stairs lead to dungeons. Choose:\n1) Metallic clanging left\n2) Moaning ahead\n3) Flickering light right"
            ),
            options=[
                Option("1", "Go left to clanging", next_id="throne_room", outcome="Armed at armory"),
                Option("2", "Go straight toward moaning", fatal=True, outcome="Fell to dungeon zombies"),
                Option("3", "Follow flickering light", next_id="catacombs", outcome="Found a secret candle-lit passage"),
            ],
        ))

        add(Scene(
            id="catacombs",
            text=(
                "You enter ancient catacombs beneath the castle. A skeletal sentry blocks a narrow archway."
            ),
            options=[
                Option("challenge", "Challenge the sentry to a riddle", next_id="catacomb_riddle"),
                Option("dash", "Dash past while it's distracted", next_id="throne_room", outcome="Slipped through the catacombs"),
            ],
        ))

        add(Scene(
            id="catacomb_riddle",
            type="input",
            text=(
                "The sentry rasps: 'I speak without a mouth and hear without ears. I have nobody, but I come alive with wind. What am I?'\n"
                "(enter a single word)"
            ),
            input_correct={"echo": ("throne_room", "Answered the catacomb riddle")},
            input_fatal_outcome="Failed catacomb riddle",
        ))

        # Throne room (end)
        add(Scene(
            id="throne_room",
            text="You burst into the throne room. The False King laughs. Charge or Trick?",
            options=[
                Option("charge", "Charge the False King", fatal=True, outcome="Fell in throne room"),
                Option("trick", "Expose the illusion", next_id=None, outcome="Saw through throne room illusion"),
            ],
        ))

        # Forest
        add(Scene(
            id="forest_path",
            text=(
                "A mystical stag blocks your way. Choose:\n1) Calm it\n2) Shoot it\n3) Follow it\n4) Approach a shining pond"
            ),
            options=[
                Option("1", "Attempt to calm the stag", next_id="secret_library", outcome="Led to secret entrance"),
                Option("2", "Shoot the stag", fatal=True, outcome="Swarmed by forest spirits"),
                Option("3", "Follow the stag to a druid circle", next_id="druid_riddle"),
                Option("4", "Approach the mystic pond", next_id="mystic_pond"),
            ],
        ))

        add(Scene(
            id="druid_riddle",
            type="input",
            text=(
                "Druids ask: What occurs once in June, twice in August, but never in October? (single letter)"
            ),
            input_correct={"e": ("throne_room", "Druids' amulet granted")},
            input_fatal_outcome="Failed druid riddle",
        ))

        add(Scene(
            id="mystic_pond",
            text="At the mystic pond choose: A) Drink  B) Search banks  C) Vow",
            options=[
                Option("a", "Drink from the pond", next_id="throne_room", outcome="Healed by mystic pond and found hidden tunnel"),
                Option("b", "Search the banks", next_id="secret_library", outcome="Found medallion at mystic pond"),
                Option("c", "Make a knightly vow", next_id="throne_room", outcome="Boon of the pond guardian"),
            ],
        ))

    def _add(self, scene: Scene) -> None:
        self.scenes[scene.id] = scene


# Singleton engine for convenience
ENGINE = Engine()
