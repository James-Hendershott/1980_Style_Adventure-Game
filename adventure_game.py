"""
Adventure Game Project - CS3620_Project1

Requirements:
- Create a text-based console adventure game where the player chooses their own adventure.
- The game should include an entertaining story with a minimum of 10 decision points and at least 20 narrative passages.
- Use various Python types including strings, integers, and booleans.
- Use input() to accept user input and convert it to the appropriate type when needed.
- Utilize control structures such as if, elif, and else for branching the story.
- Incorporate loops (for or while) to manage repeated actions or validations.
- Organize the code into functions (e.g., start_adventure(), castle_entrance(), secret_library(), etc.) to encapsulate different parts of the adventure.
- Use file handling to save the outcome of the adventure to a file named "adventure_outcomes.txt".
- Include a function read_outcomes() to read and display past adventure outcomes.
- Provide nods to Monty Python and the Holy Grail as well as The Princess Bride films.
- Allow the user to choose their own knightly name.
- I am also learning and utilizing docstrings (triple-quoted strings) for function documentation for the very first time.
"""

import os

# Global variable to store player's name
player_name = ""

def get_player_name():
    """Prompts the user to enter their knightly name."""
    global player_name
    player_name = input("Enter your knightly name: ").strip()
    if not player_name:
        player_name = "Sir indecisive"  # Default name if none provided
    print(f"\nWelcome, Sir {player_name}!")
    print("May your quest be as daring as a Monty Python adventure and as legendary as The Princess Bride.\n")

def save_outcome(outcome):
    """Appends the game outcome to adventure_outcomes.txt."""
    with open("adventure_outcomes.txt", "a") as file:
        file.write(outcome + "\n")

def fatal_end(outcome):
    """Prints a generic fatal message and saves the fatal outcome."""
    print("\nAlas, your quest has ended in tragedy!")
    save_outcome(outcome)

def read_outcomes():
    """Reads and prints all saved outcomes from the file."""
    try:
        with open("adventure_outcomes.txt", "r") as file:
            outcomes = file.readlines()
            if outcomes:
                print("\nPast Adventure Outcomes:")
                for i, outcome in enumerate(outcomes, 1):
                    print(f"{i}. {outcome.strip()}")
            else:
                print("No outcomes recorded yet.")
    except FileNotFoundError:
        print("No outcomes file found - starting fresh!")

def get_choice(options, prompt):
    """Handles user input validation with retry logic."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in options:
            return user_input
        print(f"Invalid choice. Please enter one of {options}.")

def start_adventure():
    """Main entry point for the adventure game."""
    print("\nWelcome to the Kingdom's Peril Adventure!")
    print(f"You are Sir {player_name}, a valiant knight on a quest to rescue Princess Elara.")
    print("Legend says she's held in the ancient Crimson Castle...")
    print("But beware - dark forests surround the castle grounds, and surprises await, as absurd as in Monty Python's sketches.\n")
    
    choice = get_choice(["castle", "forest"], "Go to (castle/forest): ")
    if choice == "castle":
        castle_entrance()
    else:
        forest_path()

def castle_entrance():
    """First decision point at the castle entrance."""
    print("\nYou stand before the massive castle gates, reminiscent of Camelot itself.")
    print("They creak open ominously, and you recall the absurdity of knights shouting 'Ni!' in Monty Python.")
    print("In the courtyard you see:")
    print("1. A guarded main entrance")
    print("2. A suspiciously quiet side entrance")
    
    choice = get_choice(["1", "2"], "Choose entrance (1/2): ")
    if choice == "1":
        main_entrance()
    else:
        side_entrance()

def main_entrance():
    """Main castle entrance scenario."""
    print("\nGuards spot you! They offer parley:")
    print("A) Fight your way through")
    print("B) Attempt diplomacy (channeling the wit of Westley from The Princess Bride)")
    print("C) Create distraction (perhaps shout 'Inconceivable!' at the enemy)")
    
    choice = get_choice(["a", "b", "c"], "Choose (A/B/C): ").lower()
    if choice == "a":
        print("\nYour bold attack fails against superior numbers! 'Inconceivable!' you mutter.")
        print("Your vision begins to fade as you feel the sharp pain of a blade enter your side.")
        print("The guards laugh as they walk over your corpse.")
        fatal_end("Fell in main entrance combat")
    elif choice == "b":
        print("\nYour silver tongue wins safe passage!")
        grand_hall()
    else:
        print("\nYour distraction works! You slip by like a cunning rogue.")
        grand_hall()

def side_entrance():
    """Side entrance scenario with a puzzle."""
    print("\nThe quiet entrance leads to a stone corridor.")
    print("A magical barrier blocks your path with this riddle reminiscent of absurd quests:")
    print("What comes once in a minute, twice in a moment, but never in a thousand years?")
    
    attempts = 3
    for attempt in range(1, attempts+1):
        answer = input(f"Attempt {attempt}/{attempts}: ").lower()
        if answer == "m":
            print("\nThe barrier dissolves! You proceed, feeling a bit like a brave knight from Monty Python.")
            secret_library()
            return
        else:
            if attempt < attempts:
                print(f"\nThe barrier murmurs ominously... (Attempt {attempt} failed)")
    print("\nYou hear the distant laughter of an old man.")
    print("The barrier radiates and emits an overwhelming glow!")
    print("You feel the air electrified before the deafening blast that ends your life!")
    fatal_end("Failed side entrance riddle")

def secret_library():
    """Library path after solving the riddle."""
    print("\nYou find an ancient library with two strange artifacts:")
    print("1. A glowing crystal orb")
    print("2. A dusty tome bound in chains")
    
    choice = get_choice(["1", "2"], "Investigate (1/2): ")
    if choice == "1":
        print("\nThe orb shows you a secret passage network! It almost feels like the surreal archives of Monty Python.")
        dungeon_path()
    else:
        print("\nThe tome curses you with forbidden knowledge!")
        print("As you open its brittle pages, eldritch whispers invade your mind, and visions of doomed heroes flood your senses.")
        print("The dark magic of the tome consumes your very soul, leaving you lost in a maddening cacophony of voices.")
        fatal_end("Driven mad by ancient tome")

def grand_hall():
    """Central castle hall scenario."""
    print("\nYou enter the grand hall. Two paths branch:")
    print("Left: Strange noises echo from above the balcony")
    print("Right: Faint singing from below, as if whispering 'As you wish' in honor of epic quests.")
    
    choice = get_choice(["left", "right"], "Go (left/right): ")
    if choice == "left":
        balcony_path()
    else:
        dungeons()

def balcony_path():
    """Balcony scenario with combat."""
    print("\nYou find Princess Elara chained on a high balcony!")
    print("A shadowy figure emerges - the Dark Vizier!")
    
    choice = get_choice(["fight", "rescue"], "Focus on (fight/rescue): ")
    if choice == "fight":
        print("\nWith a defiant cry, you charge at the Dark Vizier!")
        print("But his magic defenses manifest as a swirling vortex of shadow and flame.")
        print("The Vizier's dark spells leave you utterly defenseless, and you are engulfed in a torrent of mystical fire.")
        print("Your armor liquefies under the searing heat, and you are reduced to nothing but a pile of ashes.")
        fatal_end("Defeated by Dark Vizier")
    else:
        print("\nYou free the princess while dodging attacks, reminiscent of a daring rescue in The Princess Bride!")
        print("Together you escape as the balcony collapses!")
        save_outcome("Heroically rescued princess")

def dungeons():
    """Dungeon path with multiple challenges."""
    print("\nDark stairs lead to dungeons. You hear:")
    print("1. Metallic clanging from the left")
    print("2. Moaning from straight ahead")
    print("3. Flickering light to the right")
    
    choice = get_choice(["1", "2", "3"], "Investigate (1/2/3): ")
    if choice == "1":
        print("\nYou find an armory! Better equipment helps your quest, as if blessed by the absurd spirit of Monty Python.")
        throne_room()
    elif choice == "2":
        print("\nAs you proceed, a ghastly moan fills the air—a chilling sound from the depths of despair.")
        print("Before you can react, zombie prisoners emerge from the darkness, their decaying forms advancing with sinister intent.")
        print("Their rotting hands reach out, grabbing and clawing at you with relentless hunger.")
        print("In a desperate struggle, you try to fend them off, but the undead swarm you with overwhelming force.")
        print("Their foul stench and cold grip leave you paralyzed, and in a final, brutal moment, you realize you have become their last meal.")
        print("Your brave resistance fades as you succumb to the merciless grasp of the undead.")
        fatal_end("Fell to dungeon zombies")
    else:
        print("\nA torch reveals a secret passage upward!")
        throne_room()

def throne_room():
    """Final throne room scenario."""
    print("\nYou burst into the throne room!")
    print("The False King laughs: 'You're too late!' His tone is as absurd as a Monty Python sketch.")
    
    choice = get_choice(["charge", "trick"], "Respond with (charge/trick): ")
    if choice == "charge":
        print("\nWith a defiant roar, you launch your charge toward the False King!")
        print("But as you surge forward, a dazzling shield of arcane fire erupts around him.")
        print("In an instant, the magic defenses ignite, unleashing a torrent of searing flames.")
        print("Your armor begins to melt like wax in a blaze, and the inferno consumes your very being.")
        print("The scorching heat overwhelms you, leaving only the charred echo of your once valiant charge.")
        fatal_end("Fell in throne room")
    else:
        print("\nYour clever trick exposes him as an illusion!")
        print("The real princess was hidden in the dungeon! 'Inconceivable!' you exclaim in triumph.")
        save_outcome("Saw through throne room illusion")

def mystic_pond():
    """A new optional story branch: the mystic pond with choices and consequences."""
    print("\nYou approach a serene pond whose surface shimmers like polished silver.")
    print("Ripples form even though there's no wind, and you feel a calm ancient presence.")
    print("A) Drink from the pond")
    print("B) Search the banks for a hidden token")
    print("C) Close your eyes and make a knightly vow")

    choice = get_choice(["a", "b", "c"], "Choose (A/B/C): ").lower()
    if choice == "a":
        print("\nThe water heals a deep wound and fills you with clarity. You gain insight into the castle's secret passages.")
        print("As you stand, a small ripple shows the location of a hidden tunnel leading toward the throne room.")
        save_outcome("Healed by mystic pond and found hidden tunnel")
        throne_room()
    elif choice == "b":
        print("\nYou discover a tarnished medallion bearing an old family crest. It hums faintly in your hand.")
        print("The medallion repels lesser magic. Feeling emboldened, you press toward the castle, heart steady.")
        save_outcome("Found medallion at mystic pond")
        secret_library()
    else:
        print("\nYour vow calls forth a guardian spirit who tests your resolve in combat.")
        print("You fight bravely, and the spirit, satisfied, grants you a boon: a single decisive blow in the final battle.")
        save_outcome("Boon of the pond guardian")
        throne_room()

def forest_path():
    """Alternative forest path scenario."""
    print("\nYou take the dangerous forest path.")
    print("A mystical stag blocks your way, as enigmatic as the knights of Camelot.")
    print("1. Attempt to calm it")
    print("2. Shoot it with your bow")
    print("3. Follow it")
    
    print("4. Approach a shining pond nearby")

    choice = get_choice(["1", "2", "3", "4"], "Choose action (1/2/3/4): ")
    if choice == "1":
        print("\nThe stag leads you to a secret castle entrance!")
        secret_library()
    elif choice == "2":
        print("\nYou take careful aim and let fly your arrow!")
        print("But as it whistles past its mark, the arrow disturbs the ancient magic of the forest.")
        print("A chorus of eerie voices rises—the forest spirits begin to chant in unison, 'Ni! Ni! Ni!'")
        print("Their ghostly forms materialize from the mist, closing in around you.")
        print("Overwhelmed and disoriented, you feel your strength slipping away as you are drawn into their spectral ranks.")
        print("You have been swarmed by forest spirits, your fate sealed by the very magic you dared to disturb.")
        fatal_end("Swarmed by forest spirits")
    else:
        print("\nFollowing the stag leads you to an ancient druid circle.")
        druid_quest()

    if choice == "4":
        mystic_pond()

def druid_quest():
    """Druid circle scenario with a time loop challenge."""
    print("\nDruids challenge you to solve their puzzle:")
    print("What occurs once in June, twice in August, but never in October?")
    attempts = 3
    for attempt in range(1, attempts + 1):
        answer = input(f"Attempt {attempt}/{attempts}: ").lower()
        if answer == "e":
            print("\nThe druids smile knowingly and bestow upon you a shimmering amulet of protection!")
            print("Empowered by their gift, you feel ready to face the next challenge.")
            throne_room()
            return
        else:
            if attempt == 1:
                print("\nA hushed whisper echoes: 'E... perhaps the answer lies in energy itself.'")
            elif attempt == 2:
                print("\nA stern warning from the druids: 'This is your second chance—focus! The answer is as simple as the first letter of 'energy'.'")
    print("\nThe druids' eyes flare with ancient power as their curse takes hold.")
    print("A blinding light envelops you, and the very air trembles with the force of their retribution.")
    print("Your life is extinguished by the overwhelming magic of the barrier!")
    fatal_end("Failed druid riddle")


def dungeon_path():
    """Secret dungeon path from the library."""
    print("\nThe secret passage leads to cells. You find:")
    print("A) Princess Elara in a cell!")
    print("B) A suspiciously empty cell with an open door")
    
    choice = get_choice(["a", "b"], "Investigate (A/B): ").lower()
    if choice == "a":
        print("\nApproaching the cell, you notice something off about its appearance...")
        print("Without warning, the cell wall shudders and transforms—a monstrous mimic reveals itself!")
        print("With a terrifying roar, the creature lunges, its gaping maw snapping shut around you.")
        print("In a matter of seconds, you are consumed whole, your heroic quest silenced by the beast.")
        fatal_end("Fell to dungeon mimic")
    else:
        print("\nYou find an escape tunnel leading to the princess!")
        print("The true Elara was hidden in plain sight!")
        save_outcome("Found true princess through intuition")


def main():
    """Main game loop and flow control."""
    # Get the player's knightly name at the start of the game.
    get_player_name()
    
    while True:
        print("\n=== Kingdom's Peril ===")
        print("1. Start New Adventure")
        print("2. View Past Outcomes")
        print("3. Quit")
        choice = input("Choose (1/2/3): ").strip()
        
        if choice == "1":
            start_adventure()
        elif choice == "2":
            read_outcomes()
        elif choice == "3":
            print("Farewell, brave knight!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()