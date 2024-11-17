"""
The program asks the user for the number of characters they want to spawn
in the world.
"""

# asking the number of characters they want.
numOfCharacters = int(input("How many characters do you want?\n"))

# code repeats until the user enters the number of characters between 1 to 5 (inclusive) only.
while(numOfCharacters < 1 or numOfCharacters > 5):
    # reprompts the user to enter the appropriate number again.
    numOfCharacters = int(input("You may choose 1-5 characters only!\nHow many characters do you want?\n"))

# manipulates the string if there are multiple characters.
isMultipleCharacters = "characters" if numOfCharacters > 1 else "character"

# final output.
print("There will be {0} {1} attempting to Rise from the (Mon)Ashes!".format(numOfCharacters, isMultipleCharacters))
