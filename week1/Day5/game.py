import random


class Game:
    ITEMS = ["rock", "paper", "scissors"]

    # Winning combinations: key beats value
    WINS_AGAINST = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock",
    }

    def get_user_item(self):
        """Ask the user to pick rock, paper, or scissors. Loops until valid input."""
        while True:
            choice = input("Your move (rock / paper / scissors): ").strip().lower()
            if choice in self.ITEMS:
                return choice
            print(f"  Invalid choice '{choice}'. Please type rock, paper, or scissors.")

    def get_computer_item(self):
        """Pick a random item for the computer."""
        return random.choice(self.ITEMS)

    def get_game_result(self, user_item, computer_item):
        """
        Compare the two items and return:
          'win'  – user wins
          'loss' – user loses
          'draw' – tie
        """
        if user_item == computer_item:
            return "draw"
        if self.WINS_AGAINST[user_item] == computer_item:
            return "win"
        return "loss"

    def play(self):
        """
        Run one full round:
          1. Get user item
          2. Get computer item
          3. Determine & print result
          4. Return result string ('win' | 'loss' | 'draw')
        """
        user_item = self.get_user_item()
        computer_item = self.get_computer_item()
        result = self.get_game_result(user_item, computer_item)

        # Pretty result message
        if result == "win":
            outcome_msg = "You win! "
        elif result == "loss":
            outcome_msg = "You lose! "
        else:
            outcome_msg = "It's a draw! "

        print(f"\n  You selected: {user_item}")
        print(f"  Computer selected: {computer_item}")
        print(f"  {outcome_msg}\n")

        return result