import random

def hangman():
    word_list = ["python", "java", "hangman", "computer", "keyboard", "laptop", "headphones", "monitor"]
    random_word = random.choice(word_list)
    guessed_letters = []
    attempts = 6
    score = 0

    stages = [
        """
           -----
           |   |
               |
               |
               |
               |
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        """
    ]

    print("Let's play Hangman!")
    print("_ " * len(random_word))

    while attempts > 0:
        print(stages[6 - attempts])  # print the hangman doll

        guess = input("\nPlease guess a letter: ").lower()

        if not guess.isalpha():
            print("Invalid input. Please enter a letter.")
        elif len(guess) != 1:
            print("Please enter only one letter.")
        elif guess in guessed_letters:
            print("You have already guessed that letter.")
        elif guess not in random_word:
            print("Sorry, that letter is not in the word.")
            attempts -= 1
            score -= 1
        else:
            print("Good job, that letter is in the word!")
            guessed_letters.append(guess)
            score += 1

        word_so_far = ""
        for letter in random_word:
            if letter in guessed_letters:
                word_so_far += letter + " "
            else:
                word_so_far += "_ "

        print(word_so_far)
        print("Your current score is: ", score)

        if "_" not in word_so_far:
            print("Congratulations, you won!")
            print("Your final score is: ", score)
            update_leaderboard(score)
            return

    print(stages[-1])  # print the final stage of the hangman doll
    print("Sorry, you ran out of attempts. The word was " + random_word + ".")
    print("Your final score is: ", score)
    update_leaderboard(score)

def update_leaderboard(score):
    try:
        with open("leaderboard.txt", "r") as file:
            scores = file.readlines()
            scores = [int(i.strip()) for i in scores]

    except FileNotFoundError:
        scores = []

    scores.append(score)
    scores.sort(reverse=True)

    with open("leaderboard.txt", "w") as file:
        for score in scores:
            file.write(str(score) + "\n")

    print("Updated leaderboard:")
    for i, score in enumerate(scores, start=1):
        print(f"{i}. {score}")

if __name__ == "__main__":
    hangman()