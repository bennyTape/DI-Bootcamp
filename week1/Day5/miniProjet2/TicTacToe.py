"""
Tic Tac Toe — Two-player terminal game
Concepts: conditionals, loops, functions
"""

def display_board(board):
    """Display the 3x3 Tic Tac Toe board."""
    print("\nTIC TAC TOE")
    print("*" * 17)
    for i, row in enumerate(board):
        print(f"*  {row[0]} | {row[1]} | {row[2]}  *")
        if i < 2:
            print("*  ---|---|---  *")
    print("*" * 17)
    print()


def player_input(board, player):
    """
    Ask the current player for a valid row and column.
    Returns (row, col) as zero-based indices.
    """
    while True:
        try:
            row = int(input(f"Player {player}'s turn — Enter row (1-3): ")) - 1
            col = int(input(f"Player {player}'s turn — Enter column (1-3): ")) - 1

            if row not in range(3) or col not in range(3):
                print("⚠  Please enter numbers between 1 and 3.\n")
            elif board[row][col] != " ":
                print("⚠  That square is already taken. Choose another.\n")
            else:
                return row, col

        except ValueError:
            print("⚠  Invalid input. Please enter a number.\n")


def check_win(board, player):
    """
    Return True if `player` has three marks in a row
    (horizontally, vertically, or diagonally).
    """
    mark = player

    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == mark for j in range(3)):   # row
            return True
        if all(board[j][i] == mark for j in range(3)):   # column
            return True

    # Check diagonals
    if all(board[i][i] == mark for i in range(3)):        # top-left → bottom-right
        return True
    if all(board[i][2 - i] == mark for i in range(3)):   # top-right → bottom-left
        return True

    return False


def check_tie(board):
    """Return True when every square is filled (and no winner was found)."""
    return all(board[r][c] != " " for r in range(3) for c in range(3))


def play():
    """Main game loop — sets up the board and alternates turns until win/tie."""
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    turn = 0

    print("\nWelcome to TIC TAC TOE!")
    print("Rows and columns are numbered 1–3 from top-left.")

    while True:
        player = players[turn % 2]
        display_board(board)

        row, col = player_input(board, player)
        board[row][col] = player

        if check_win(board, player):
            display_board(board)
            print(f"🎉  Player {player} wins! Congratulations!\n")
            break

        if check_tie(board):
            display_board(board)
            print("🤝  It's a tie! Well played by both!\n")
            break

        turn += 1

    again = input("Play again? (y/n): ").strip().lower()
    if again == "y":
        play()
    else:
        print("Thanks for playing! 👋\n")


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    play()