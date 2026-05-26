import random

# ─────────────────────────────────────────
# Exercise 1: Birthday Look-up
# ─────────────────────────────────────────
birthdays = {
    "Ada Lovelace":    "1815/12/10",
    "Alan Turing":     "1912/06/23",
    "Grace Hopper":    "1906/12/09",
    "Linus Torvalds":  "1969/12/28",
    "Guido van Rossum":"1956/01/31",
}

print("Welcome! You can look up the birthdays of the people in the list!")
name = input("Enter a person's name: ")
birthday = birthdays[name]
print(f"{name}'s birthday is {birthday}.")


# ─────────────────────────────────────────
# Exercise 2: Birthdays Advanced
# ─────────────────────────────────────────
print("\nWelcome! You can look up the birthdays of the people in the list!")
print("People in the dictionary:")
for person in birthdays:
    print(f"  - {person}")

name = input("\nEnter a person's name: ")
if name in birthdays:
    print(f"{name}'s birthday is {birthdays[name]}.")
else:
    print(f"Sorry, we don't have the birthday information for {name}.")


# ─────────────────────────────────────────
# Exercise 3: Check the Index
# ─────────────────────────────────────────
names = ['Samus', 'Cortana', 'V', 'Link', 'Mario', 'Cortana', 'Samus']

name = input("\nEnter your name: ")
if name in names:
    print(f"The first occurrence of '{name}' is at index {names.index(name)}.")
else:
    print(f"'{name}' is not in the list.")


# ─────────────────────────────────────────
# Exercise 4: Double Dice
# ─────────────────────────────────────────
def throw_dice():
    """Return a random integer between 1 and 6 (inclusive)."""
    return random.randint(1, 6)


def throw_until_doubles():
    """
    Keep rolling two dice until both show the same number.
    Returns the total number of throws made.
    """
    throws = 0
    while True:
        die1, die2 = throw_dice(), throw_dice()
        throws += 1
        if die1 == die2:
            return throws


def main():
    results = [throw_until_doubles() for _ in range(100)]

    total = sum(results)
    average = total / len(results)

    print(f"\nTotal throws: {total}")
    print(f"Average throws to reach doubles: {average:.2f}.")


main()