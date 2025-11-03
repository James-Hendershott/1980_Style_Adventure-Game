"""Console (CLI) front-end for Kingdom's Peril using the shared game engine.

Run with:
    python .\adventure_game.py
"""

from game_engine import ENGINE, read_outcomes


player_name = ""


def get_player_name():
    global player_name
    player_name = input("Enter your knightly name: ").strip()
    if not player_name:
        player_name = "Sir indecisive"
    print(f"\nWelcome, {player_name}!")


def play_adventure():
    print("\nWelcome to the Kingdom's Peril Adventure!")
    scene_id = ENGINE.start_id

    while True:
        scene = ENGINE.get_scene(scene_id)
        print("\n" + scene.text)

        if scene.type == "choice":
            # show options
            for opt in scene.options:
                print(f" - {opt.key}: {opt.label}")
            sel = input("Choose: ").strip()
            try:
                next_id, outcome, is_fatal, is_end = ENGINE.apply_choice(scene_id, sel)
            except ValueError as e:
                print(e)
                continue
        elif scene.type == "input":
            ans = input("Enter your answer: ")
            next_id, outcome, is_fatal, is_end = ENGINE.apply_input(scene_id, ans)
        else:
            # end scenes (shouldn't be reached directly in this engine)
            is_fatal, is_end, next_id, outcome = False, True, None, None

        if outcome:
            print(f"Outcome recorded: {outcome}")

        if is_end:
            if is_fatal:
                print("\nAlas, your quest has ended in tragedy!")
            else:
                print("\nVictory! Your quest concludes gloriously.")
            break

        scene_id = next_id


def main():
    get_player_name()
    while True:
        print("\n=== Kingdom's Peril ===")
        print("1. Start New Adventure")
        print("2. View Past Outcomes")
        print("3. Quit")
        choice = input("Choose (1/2/3): ").strip()
        if choice == "1":
            play_adventure()
        elif choice == "2":
            print("\n" + read_outcomes())
        elif choice == "3":
            print("Farewell, brave knight!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()