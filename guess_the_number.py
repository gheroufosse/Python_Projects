from random import randint

def guess(x):

    random_number = randint(1,x)
    guess = 0
    while guess != random_number:
        guess = int(input(f"Guess a number between 1 and {x}: "))
        if guess > random_number:
            print(f"The number is less dans {guess}")
        elif guess < random_number:
            print(f"The number is more than {guess}")


    print(f"Great! {random_number} was truely the answer.")


def computer_guess(x):

    low = 1
    high = x
    feedback = ''
    while feedback != 'y':
        guess = randint(low,high)
        feedback = input(f"Is {guess} the correct answer ? 'y' or 'n' " )
        if feedback != 'y':
            clue = input(f"Is it lower or upper than {guess} ? 'up' or 'down' ")
            if clue == 'up':
                low = guess - 1
            elif clue == 'down':
                high = guess + 1


    print("Yeee I won stupid player")



def main():

    Max_number = int(input("Choose a maximal number: "))
    guess(Max_number)
    print("Ok so now it's the computer's turn! \t Choose a number.")

    computer_guess_max_number = int(input("And now choose a maximal number for the computer to guess your number:"))
    computer_guess(computer_guess_max_number)

main()


