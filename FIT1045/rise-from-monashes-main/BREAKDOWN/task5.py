"""
The program assigns the names to the spawned characters manually or appropriately.
"""

# list of character names that the program will automatically assign.
DEFAULT_CHARACTER_LIST = ['HOMELANDER', 'IMAN', 'TERMINATOR', 'LELO MUSK', 'MR. MONASH', 
'FYP STUDENT 2', 'HERMIONE GRANGER', 'SUPERMARIO', 'SUNFLOWER', 'THANOS',
'LUIGI', 'CHATGPT5', 'PATRICK STAR', 'GARY THE SNAIL', 'MICHONNE',
'VENOM','SPONGEBOB', 'DORAEMON', 'WOLVERINE', 'DORAEMON', 'BUMBLEBEE']

# asks the user to input the number of characters.
number_of_characters = int(input("How many characters do you want?\n")) 

def find_consonants(word):
    """
    Takes in the parameter word and returns how many consonants does it have.
    
    Parameters:
    word: str - The word to check for the number of consonants.
    
    Returns:
    count: int - The number of consonants present in a given word.
    """
    
    count = 0
    not_consonants = ['A', 'E', 'I', 'O', 'U', ' ', '.']
    for ch in word:
        if ch not in not_consonants and not ch.isdigit():
            count += 1
    return count

# asks the user whether they want to enter the names manually or automatically.
setNameMode = input("Do you wish to choose the character names manually or automatically (M or A)?\n")

names = [] # names list to store the names.

# assigns name for every character manually
for i in range(number_of_characters):
    if (setNameMode == "M"):
        nameToAppend = input("Set character {0} name:\n".format(i+1)).upper() # converts the string all to uppercase.
        while (nameToAppend.upper() in names): # repeatedly reprompts the user to enter unique names only.
            print("{0} is a duplicate, try again!".format(nameToAppend))
            nameToAppend = input("Set character {0} name:\n".format(i+1)).upper()

        names.append(nameToAppend) # adding the name to the list.
        
        if len(names) == number_of_characters: # if the list length equals the number of characters, break the loop.
            break 

if (setNameMode == "A"):
    # asks the user to choose a number from 1-6.
    divisible_by = int(input("Pick a number between 1-6 (inclusive):\n"))
    
    # reprompts the user to enter the correct value within the range 1-6.    
    while(divisible_by < 1 or divisible_by > 6):
        print("You may choose a number between 1-6 (inclusive) only!")
        divisible_by = int(input("Pick a number between 1-6 (inclusive):\n"))
            
    """
    The code below loops through every element of the default character list and chooses the first unique element 
    such that the number of consonants in that word is divisible by the number chosen initially by the user, and if the 
    name is not in the list.
    """
    
    for i in range(len(DEFAULT_CHARACTER_LIST)):
        if find_consonants(DEFAULT_CHARACTER_LIST[i]) % divisible_by == 0 and DEFAULT_CHARACTER_LIST[i] not in names:
            names.append(DEFAULT_CHARACTER_LIST[i])
                
        if len(names) == number_of_characters: # breaks the loop if the length of the list equals the number of characters.
            break
        
# final output of the list.        
print(names)
