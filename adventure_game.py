def intro():
    print("Welcome change name!")
    print("You're standing at the edge of a dark forest.")
    print("There are two paths ahead of you.")
    print("Do you want to go left or right?")

def left_path():
    print("\nYou took the left path.")
    print("You encounter a friendly elf who gives you a magical potion.")
    print("You win!")

def right_path():
    print("\nYou took the right path.")
    print("Oh no! You fell into a trap.")
    print("Game over!")

def main():
    intro()
    choice = input("Type 'left' or 'right': ").lower()

    if choice == "left":
        left_path()
    elif choice == "right":
        right_path()
    else:
        print("\nInvalid choice. Please restart the game and type 'left' or 'right'.")

if __name__ == "__main__":
    main()