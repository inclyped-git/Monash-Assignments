DEFAULT_CHARACTER_LIST = ['HOMELANDER', 'IMAN', 'TERMINATOR', 'LELO MUSK', 'MR. MONASH', 
'FYP STUDENT 2', 'HERMIONE GRANGER', 'SUPERMARIO', 'SUNFLOWER', 'THANOS',
'LUIGI', 'CHATGPT5', 'PATRICK STAR', 'GARY THE SNAIL', 'MICHONNE',
'VENOM','SPONGEBOB', 'DORAEMON', 'WOLVERINE', 'DORAEMON 2.0', 'BUMBLEBEE']

def set_character_number() -> int:
    """
    Description:
        The function will ask for how many characters the user wants, and then printing an introduction to
        the players. The function will also return the number of characters in the game.
        
    Returns:
        @return int: The number of characters deployed in BERYL world.
    """
    numOfCharacters = int(input( "How many characters do you want?\n" ))
     
    # We will only want 1-5 characters; incorrect input will result in the user being reprompted to enter
    while ( numOfCharacters < 1 or numOfCharacters > 5 ):
        numOfCharacters = int(input( "You may choose 1-5 characters only!\nHow many characters do you want?\n" ))
    
    # Need to print x Characters if x > 1, else print x Character
    hasMultipleCharacters = "character" if numOfCharacters == 1 else "characters"
    
    print(f"There will be {numOfCharacters} {hasMultipleCharacters} attempting to Rise from the (Mon)Ashes!")
    return numOfCharacters

def set_names_manual( numberOfCharacters: int ) -> list[str]:
    """
    Description:
        The function will return a list of manually entered names for the characters that enter
        the BERYL world.
    
    Parameter:
        @param int numberOfCharacters: The number of characters that enter the BERYL world.
        
    Returns:
        @return list[str]: A list of names that are given to the characters.
    """
    
    names = [] # A list to store the names of the characters
    
    for i in range(numberOfCharacters):
        nameToAppend = input(f"Set character {i+1} name:\n").upper() # Converts all of the string name to uppercase
        
        # If a name repeats the program will reprompt to enter an unique name for every character
        while (nameToAppend in names):
            print(f"{nameToAppend} is a duplicate, try again!")
            nameToAppend = input(f"Set character {i+1} name:\n").upper()
        
        names.append(nameToAppend)
        
    return names

def set_divided_by_integer() -> int:
    """
    Description:
        The function asks the user to enter an integer between 1 to 6 (inclusive), and returns that integer neeeded
        for automatic naming. 
    
    Returns:
        @return int: An integer that is used for automatic naming system.
    """
    
    divisible_by = int( input( "Pick a number between 1-6 (inclusive):\n" ) )
    
    # Reprompts the user to enter again if the integer is out of the range [1,6]
    while( divisible_by < 1 or divisible_by > 6 ):
        print("You may choose a number between 1-6 (inclusive) only!")
        divisible_by = int( input( "Pick a number between 1-6 (inclusive):\n" ) )
    
    return divisible_by

def set_names_automatic( characterList: list[str], numberOfCharacters: int, divisibleBy: int ) -> list[str]:
    """
    Description:
        Automatically names all of the characters that enter the BERYL world
        
    Parameters:
        @param list[str] characterList: A list of predefined names that can be used to name each character
        @param int numberOfCharacters: The number of characters that enter the BERYL world
        @param int divisibleBy: The number that will be used to determine the names for each character
    
    Returns:
        @return list[str]: A list of character names.
    """
    
    names = [] # A list to store the names
    
    for i in range(len(characterList)):
        
        # Finding the number of consonants in each name
        numOfConsonants = 0
        vowels = ['A', 'E', 'I', 'O', 'U']
        for character in characterList[i]:
            if character >= 'A' and character <= 'Z' and character not in vowels: # Only considers ASCII values between A-Z
                   numOfConsonants += 1
        
        # If the divisibleBy divides the number of consonants for each name, append that name to the list until
        # you reach the character limit
        if (numOfConsonants % divisibleBy == 0) and (characterList[i] not in names):
            names.append(characterList[i]) # We will append unique names only
        
        if len(names) == numberOfCharacters:
            break
        
    return names
            

def return_welcome_message(names: list[str]) -> str:
    """
    Description:
        Returns a welcome message for the characters entering the BERYL world.
        
    Parameters:
        @param list[str] names: A list of character names entering the BERYL world.
        
    Returns:
        @return: A welcome message for the characters.
    """
    
    if len(names) == 1:
        return f"It is the year 3045. Sentient Artificial Intelligence Bots have now taken over.\n{names[0]} must rise from the (Mon)ashes!\nThey are BERYL's only hope!"
    else:
        return "It is the year 3045. Sentient Artificial Intelligence Bots have now taken over.\n{0} and {1} must rise from the (Mon)ashes!\nOnly one character may survive!".format(", ".join(names[:-1]), names[-1])
