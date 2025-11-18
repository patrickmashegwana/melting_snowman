import random
import shutil
from ascii_art import STAGES

# ANSI Color Constants
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# List of secret words
WORDS = ["python", "git", "github", "snowman", "meltdown"]

width = shutil.get_terminal_size().columns

def get_random_word():
    """Selects a random word from the list."""
    return random.choice(WORDS)


def format_message(text, color=RESET):
    """Wraps the given text in ANSI color codes."""
    return f"{color}{text}{RESET}"


def print_dotted_box(message, padding=1, center=False):
    """
    Prints a message inside a dotted box.

    Args:
        message (str): The message to display (can be multiline).
        padding (int): Padding around the text.
        center (bool): Whether to center the text inside the box.
    """
    lines = message.strip().split('\n')
    max_len = max(len(line.strip()) for line in lines)
    total_width = max_len + padding * 2 + 2  # borders + padding

    border = '.' * total_width
    print(border)
    for line in lines:
        line = line.strip()
        line = line.center(max_len) if center else line.ljust(max_len)
        print(f".{' ' * padding}{line}{' ' * padding}.")
    print(border)


def display_game_state(mistakes, secret_word, guessed_letters):
    """Displays current snowman stage and the guessed word so far."""
    print(CYAN + STAGES[mistakes] + RESET)

    display_word = ""
    for letter in secret_word:
        if letter in guessed_letters:
            display_word += GREEN + letter + RESET + " "
        else:
            display_word += "_ "

    print(f"{BOLD}Word:{RESET}  {display_word.strip()}  ({len(secret_word)} letters)\n")
    print(f"{BOLD}Guessed letters:{RESET} {' '.join(sorted(guessed_letters))}\n")
    print("*" * width, "\n")


def play_game():
    """
    Handles the main gameplay loop:
    - Gets a random secret word
    - Tracks user guesses and mistakes
    - Displays the game state after each guess
    - Ends the game when the player wins or loses
    """
    secret_word = get_random_word()
    guessed_letters = []
    mistakes = 0
    max_mistakes = len(STAGES) - 1

    # Welcome Message
    print_dotted_box(CYAN + "Welcome to Snowman Meltdown!\nGuess the word before the snowman melts!" + RESET, center=True)

    while True:
        display_game_state(mistakes, secret_word, guessed_letters)

        if all(letter in guessed_letters for letter in secret_word):
            print_dotted_box(format_message("Congratulations! You saved the snowman!", GREEN))
            print_dotted_box(format_message(f"The word was: {secret_word}", CYAN))
            break

        if mistakes >= max_mistakes:
            print_dotted_box(format_message(" Game Over! The snowman melted!", RED))
            print_dotted_box(format_message(f"The word was: {secret_word}", CYAN))
            break

        guess = input("Guess a letter: ").lower()

        # Input validation
        if not guess.isalpha() or len(guess) != 1:
            print_dotted_box(format_message(" Please enter a single valid letter.", YELLOW))
            continue

        if guess in guessed_letters:
            if guess in secret_word:
                print_dotted_box(format_message("✔ You already guessed that letter correctly.", YELLOW))
            else:
                mistakes += 1
                print_dotted_box(format_message(f" You already guessed '{guess}' and it's still wrong.", RED))
                print_dotted_box(format_message(f"You have {max_mistakes - mistakes} chances left.", RED))
            continue

        guessed_letters.append(guess)

        if guess in secret_word:
            print_dotted_box(format_message(" Good guess!", GREEN))
        else:
            mistakes += 1
            print_dotted_box(format_message(f" Wrong guess! You have {max_mistakes - mistakes} chances left.", RED))