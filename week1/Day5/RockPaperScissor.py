from game import Game


def get_user_menu_choice():
    """
    Display the main menu and return the user's choice.
    Valid choices: '1' (play), '2' (scores), 'q' (quit).
    No looping – just reads one input and returns it.
    """
    print("=" * 40)
    print("       ROCK  PAPER  SCISSORS")
    print("=" * 40)
    print("  1 – Play a new game")
    print("  2 – Show scores")
    print("  q – Quit")
    print("-" * 40)

    choice = input("Your choice: ").strip().lower()
    return choice


def print_results(results):
    """
    Print a summary of all games played.
    results: dict with keys 'win', 'loss', 'draw' and int values.
    """
    total = results["win"] + results["loss"] + results["draw"]

    print("\n" + "=" * 40)
    print("         GAME SUMMARY")
    print("=" * 40)
    print(f"  Total games played : {total}")
    print(f"  Wins               : {results['win']}")
    print(f"  Losses             : {results['loss']}")
    print(f"  Draws              : {results['draw']}")
    print("=" * 40)

    if total == 0:
        print("  You didn't play any games.")
    elif results["win"] > results["loss"]:
        print("  Great job – you came out ahead! ")
    elif results["loss"] > results["win"]:
        print("  Better luck next time! ")
    else:
        print("  Perfectly balanced. ")

    print("\n  Thanks for playing! See you next time.\n")


def main():
    results = {"win": 0, "loss": 0, "draw": 0}
    valid_choices = {"1", "2", "q"}

    while True:
        choice = get_user_menu_choice()

        if choice not in valid_choices:
            print(f"\n  ⚠  Invalid option '{choice}'. Please enter 1, 2, or q.\n")
            continue

        if choice == "1":
            game = Game()
            result = game.play()          # 'win' | 'loss' | 'draw'
            results[result] += 1

        elif choice == "2":
            total = results["win"] + results["loss"] + results["draw"]
            if total == 0:
                print("\n  No games played yet.\n")
            else:
                print(f"\n  Wins: {results['win']}  |  "
                      f"Losses: {results['loss']}  |  "
                      f"Draws: {results['draw']}\n")

        elif choice == "q":
            print_results(results)
            break


if __name__ == "__main__":
    main()