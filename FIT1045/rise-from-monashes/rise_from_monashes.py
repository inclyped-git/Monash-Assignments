__author__ = 'inclyped'

# List of names provided to the automicatic naming algorithm
DEFAULT_CHARACTER_LIST = ['HOMELANDER', 'IMAN', 'TERMINATOR', 'LELO MUSK', 'MR. MONASH', 
'FYP STUDENT 2', 'HERMIONE GRANGER', 'SUPERMARIO', 'SUNFLOWER', 'THANOS',
'LUIGI', 'CHATGPT5', 'PATRICK STAR', 'GARY THE SNAIL', 'MICHONNE',
'VENOM','SPONGEBOB', 'DORAEMON', 'WOLVERINE', 'DORAEMON', 'BUMBLEBEE']

# The maze the character is going to escape from
BERYL_MAZE = [
  [300, -13, 189, -15, -12, 203, -23, 587, -78, 321, -46],
  [300, -11, -13, -24, 365, 198, -34, -21, 789, -81, -53],
  [300, -12, 112, -46, -76, -11, -23, -59, 321, 204, -32],
  [300, -23, 235, -12, -89, -62, -34, 212, -56, -67, -89],
  [300, 376, -23, -77, 227, -99, 134, 289, -12, 476, -51]
]


"""Checkpoint 1 Tasks"""

def get_funds_string( listOfBerylDollars: list[int] ) -> str:
    """
    Description:
        The function will return a string format of the number of Dorabies, Doubloons, and Dusts the character has 
        from a given list of Dorabies, Doubloons, and Dusts.
    
    Parameter:
        @param list[int] listOfBerylDollars: A list of Dorabies, Doubloons, and Dusts.
    
    Returns:
        @return str: A string that represents how many Dorabies, Doubloons, and Dusts the character has.
    """
    
    # Extracting Dorabies, Doubloons, and Dusts from a list of [Dorabies, Doubloons, Dusts]
    numOfDorabies = listOfBerylDollars[0]; numOfDoubloons = listOfBerylDollars[1]; numOfDusts = listOfBerylDollars[2]
    
    # Need to print x Dorabies if numOfDorabies == 0 or numOfDorabies > 1, otherwise print 1 Dorabie
    hasMultipleDorabies = "Dorabie" if ( numOfDorabies == 1 ) else "Dorabies"
    
    # Same concept applied to Doubloons and Dusts
    hasMultipleDoubloons = "Doubloon" if ( numOfDoubloons == 1 ) else "Doubloons"
    hasMultipleDusts = "Dust" if ( numOfDusts == 1 ) else "Dusts"
    
    return f"{numOfDorabies} {hasMultipleDorabies}, {numOfDoubloons} {hasMultipleDoubloons} and {numOfDusts} {hasMultipleDusts}"

def beryl_dollar_conversion( amountOfDusts: int, dustToDoubloonRate: int, doubloonToDorabieRate: int ) -> list[int]:
    """
    Description:
        The function will return a list of Dorabies, Doubloons, and Dusts after converting all of the Dusts using
        the exchange rates used in BERYL world.
        
    Parameters:
        @param int amountOfDusts: The number of Dusts the character will have to convert to corresponding Dorabies, 
                                Doubloons, and remaining Dusts.
        @param int dustToDoubloonRate: The conversion rate of converting x Dusts to 1 Doubloon.
        @param int doubloonToDorabieRate: The conversion rate of converting x Doubloons to 1 Dorabie.
    
    Returns:
        @return list[int]: A list that contains the converted Dorabies, Doubloons and remaining Dusts from the initial
                    pack of Dusts alone.
    """
    
    # Directly using the two exchange rates to directly convert x Dusts to y Dorabies
    dustToDorabieRate = dustToDoubloonRate * doubloonToDorabieRate
    
    # Converting all of the dusts into Dorabies, Doubloons, and Dusts
    convertedDorabies = int ( amountOfDusts / dustToDorabieRate )
    remainingDusts = amountOfDusts - convertedDorabies * dustToDorabieRate # Remaining Dusts after converting some to Dorabies
    
    convertedDoubloons = int ( remainingDusts / dustToDoubloonRate )
    
    convertedDusts = remainingDusts - convertedDoubloons * dustToDoubloonRate # Remaining dusts will be equal to converted Dusts
                                                                            # The others are converted to Doubloons
    
    return [convertedDorabies, convertedDoubloons, convertedDusts]
    

def beryl_dollar_indicator( dollarIndicator: int, startingFundsList: list[int], dustToDoubloonRate: int, doubloonToDorabieRate: int ) -> list[int]:
    """
    Description:
        The function will return a list of remaining Dorabies, Doubloons, and Dusts after the character
        encounters with the Dollar Indicator.
        
    Parameters:
        @param int dollarIndicator: The Dollar Indicator that will be encountered by the character.
        @param list[int] startingFundsList: The starting Dorabies, Doubloons, and Dusts before encountering the
                                        Dollar Indicator.
        @param int dustToDoubloonRate: The rate of conversion from x Dusts to 1 Doubloon.
        @param int doubloonToDorabieRate: The rate of conversion from x Doubloons to 1 Dorabie.
        
    Returns:
        @return list[int]: A list of remaining Dorabies, Doubloons, and Dusts after encountering the Dollar Indicator.
    """
    
    # Converting the starting funds all into Dusts
    # Directly converting from Dorabies to Dusts using the two exchange rates
    dustToDorabieRate = dustToDoubloonRate * doubloonToDorabieRate
    
    startingFundsInDust = startingFundsList[0] * dustToDorabieRate
    startingFundsInDust += startingFundsList[1] * dustToDoubloonRate
    startingFundsInDust += startingFundsList[2]
    
    # converting the Dollar Indicator into Dusts
    dollarIndicatorInDust = 0
    if ( dollarIndicator > 0 ): # if the Dollar Indicator is positive
        
        # First digit of the indicator implies the Dorabie amount is added to the funds
        dollarIndicatorDorabies = int ( dollarIndicator / 100 )
        remainingDollarIndicator = dollarIndicator - ( dollarIndicatorDorabies * 100 )
        
        # Second digit of the indicator implies the Doubloon amount is added to the funds
        dollarIndicatorDoubloons= int ( remainingDollarIndicator / 10 )
        
        # The remainder is the third digit of the indicator, implying that the Dust amount is added to the funds
        dollarIndicatorDusts = remainingDollarIndicator - ( dollarIndicatorDoubloons * 10 )
        
        dollarIndicatorInDust = dollarIndicatorDusts + dollarIndicatorDoubloons * dustToDoubloonRate + dollarIndicatorDorabies * dustToDorabieRate
    
    elif ( dollarIndicator < 0 ): # if the Dollar Indicator is negative
        
        # First digit of the indicator implies the Dorabie amount is subtracted from the funds
        dollarIndicatorDorabies = int ( dollarIndicator / 10 )
        
        # The remainder is the second digit of the indicator, implying the Doubloon amount is subtracted from the funds
        dollarIndicatorDoubloons = dollarIndicator - ( dollarIndicatorDorabies * 10 )
        
        dollarIndicatorInDust = dollarIndicatorDorabies * dustToDorabieRate + dollarIndicatorDoubloons * dustToDoubloonRate
    
    finalFundsInDust = startingFundsInDust + dollarIndicatorInDust
    
    # Converting the final Dusts into Dorabies, Doubloons, and remaining Dusts
    # If any of the dollar units are less than zero, they are automatically defined to zero
    finalDorabies = int ( finalFundsInDust / dustToDorabieRate ) if int ( finalFundsInDust / dustToDorabieRate ) > 0 else 0
    remainingFinalDusts = finalFundsInDust - finalDorabies * dustToDorabieRate
    
    finalDoubloons = int ( remainingFinalDusts / dustToDoubloonRate ) if int ( remainingFinalDusts / dustToDoubloonRate ) > 0 else 0
    
    finalDusts = remainingFinalDusts - finalDoubloons * dustToDoubloonRate if remainingFinalDusts - finalDoubloons * dustToDoubloonRate > 0 else 0
    
    
    return [finalDorabies, finalDoubloons, finalDusts]

"""Checkpoint 2 Tasks"""

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
    
    
    
    
"""Checkpoint 3 Tasks"""

def check_valid_maze_location( desiredPosition: tuple[int] ) -> bool:
    """
    Description:
        Returns whether the entered location is within the range or not.
        
    Parameter:
        @param tuple[int] desiredPosition: The current row and column index the character is currently in.
    
    Returns:
        @return: A boolean value indicating if the location is within the BERYL_MAZE range or not.
    """
    
    if (desiredPosition[0] < 0 or desiredPosition[1]< 0 or desiredPosition[0] >= len(BERYL_MAZE) or desiredPosition[1] >= len(BERYL_MAZE[0])):
        return False
    return True

def visualise_maze(nestedList: list[list[int]], characterName: str, desiredPosition: tuple[int]) -> str:
    """
    Description:
        The function takes in a maze, the character and the starting position, and returns a string
        version of the maze with the postion of where the character is at that moment.
        
    Parameters:
        @param list[list[int]] nestedList: The maze that the character is going to escape from.
        @param str characterName: The character name.
        @param tuple[int] desiredPosition: The position that the character is currently going to be in.
    
    Returns:
        @return: A string version of the maze that shows where the character is at that moment.
    """
    
    finalStringOfMaze = ""
    
    for row in range( len(nestedList) ):
        for column in range( len(nestedList[0]) ):
            if desiredPosition[0] == row and desiredPosition[1] == column:
                finalStringOfMaze += "<" + characterName.upper()[0] + ">   " # Putting the character if the desiredPosition index is found
            else:
                finalStringOfMaze += str(nestedList[row][column]) + "   "
        if (row < len(nestedList) - 1):
            finalStringOfMaze += "\n" # Creates a new row after the end of one list
    
    print(finalStringOfMaze)


def deploy_drone(nestedList: list[list[int]], currentLocation: tuple[int], direction: str, dollarIndicator: int) -> (list[tuple[int]], list[int]) :
    """
    Description:
        The function will return whether a character has found a Dollar Indicator inside of the nested list maze, with their
        drone. It will return the coordinates that the drone had passed by, and the dollar Indicators it encountered with
        before finding the desired Dollar Indicator. If the digit is not found, the program will return empty lists of coordinates
        and indicators.
        
    Parameters:
        @param list[list[int]] nestedList: The list that the character deploy their drone in.
        @param tuple[int] currentLocation: The location that the character will deploy their drone from.
        @param str direction: The direction the drone is going to be deployed to.
        @param int dollarIndicator: The digit that the drone is going to find.
        
    Returns:
        @return: A coordinates list and indicators list.
    """
    
    row = currentLocation[0]; column = currentLocation[1]
    
    coordinates = []; indicators = []
    foundDigit = False # Sentinel value to determine if the digit has been found or not
    
    if direction == "right":
        for index in range( column + 1, len(nestedList[row]) ):
                coordinates.append( (row, index) )
                indicators.append( nestedList[row][index] )
                
                # If the Dollar Indicator has been found
                if str(dollarIndicator) in str( nestedList[row][index] ):
                    foundDigit = True
                    print(f"Found digit at location { (row, index) }!\n")
                    return coordinates, indicators
        
    elif direction == "up":
        for index in range( row-1, -1, -1 ):
            coordinates.append( (index, column) )
            indicators.append( (nestedList[index][column]) )

            # If the Dollar Indicator has been found
            if str(dollarIndicator) in str(nestedList[index][column]):
                foundDigit = True
                print(f"Found digit at location { (index, column) }!\n")
                return coordinates, indicators

    
    elif direction == "down":
        for index in range( row+1, len(nestedList) ):
            coordinates.append( (index, column) )
            indicators.append( nestedList[index][column] )
            
            # If the Dollar Indicator has been found
            if str(dollarIndicator) in str(nestedList[index][column]):
                foundDigit = True
                print(f"Found digit at location { (index, column)}!\n")
                return coordinates, indicators
                
     # If the Dollar Indicator has not been found
    if not foundDigit:
        print("Entered restricted area!\n")
        return [], []    
    
def navigating_maze(visitedList: list[int], dollarIndicatorList: list[int], funds: list[int], dustToDoubloonRate: int, doubloonToDorabieRate: int) -> (tuple[int], list[int]):
    """
    Description:
        The function will simulate the movement of the character as they lose or collect BERYL dollars in the maze. 
        The character will stop moving if the total Dusts they have is less than or equal to zero. 
        
    Parameters:
        @param list[int] visitedList: The list that contains a list of coordinates that the character will travel to.
        @param list[int] dollarIndicatorList: The list that contains a list of Dollar Indicators that the character will encounter.
        @param list[int] funds: A list of Dorabies, Doubloons, and Dusts the character has.
        @param int dustToDoubloonRate: The exchange rate of x Dusts to 1 Doubloon.
        @param int doubloonToDorabieRate: The exchange rate of x Dorabies to 1 Dorabie.
        
    Returns:
        @return: A tuple that contains a list of coordinates and a list of indicators that the character has encounted with.
    """
    
    dustToDorabieRate = dustToDoubloonRate * doubloonToDorabieRate # Converting Dusts to Dorabies
    
    def convertDollarIndicatorToDust(indicator: int) -> int:
        """
        Description:
            The function will return all of the Dusts converted from the Dollar Indicator.
            
        Paramter:
            @param int indicator: The Dollar Indicator.
        
        Returns:
            @return: All of the Dusts converted from the Dollar Indicator.
        """
        
        # If the Dollar Indicator is positive
        if indicator > 0:
            convertedDorabies = int(indicator / 100)
            remainingIndicator = indicator - convertedDorabies * 100
            
            convertedDoubloons = int(remainingIndicator / 10)
            remainingIndicator = remainingIndicator - convertedDoubloons * 10
            
            return remainingIndicator + convertedDoubloons * dustToDoubloonRate + convertedDorabies * dustToDorabieRate

        # If the Dollar Indicator is negative
        elif indicator < 0:
            indicator = -1 * indicator
            convertedDorabies = int ( indicator / 10 )
            remainingIndicator = indicator - convertedDorabies * 10
            
            return -1 * ( convertedDorabies * dustToDorabieRate + remainingIndicator * dustToDoubloonRate )

        # If the Dollar Indicator is zero
        return 0    
    
    index = 0 
    currentCoordinate = None
    
    finalDorabies = funds[0]; finalDoubloons = funds[1]; finalDusts = funds[2] 
    
    totalDusts = finalDorabies * dustToDorabieRate + finalDoubloons * dustToDoubloonRate + finalDusts
    
    while index < len(visitedList):
        # Finding the total dusts after adding the Dollar Indicator
        totalDusts += convertDollarIndicatorToDust(dollarIndicatorList[index])
        
        if totalDusts < 0 and index == 0: # Breaking the loop if there is no enough funds for the character
            break
        
        finalDorabies = int( totalDusts / dustToDorabieRate ) if int( totalDusts / dustToDorabieRate ) > 0 else 0
        remainingDusts = totalDusts - finalDorabies * dustToDorabieRate
            
        finalDoubloons = int( remainingDusts / dustToDoubloonRate ) if  int( remainingDusts / dustToDoubloonRate ) > 0 else 0
        remainingDusts = remainingDusts - finalDoubloons * dustToDoubloonRate
            
        finalDusts = remainingDusts if remainingDusts > 0 else 0
        currentCoordinate = visitedList[index]
        
        if totalDusts < 0:
            break
        
        index += 1
    
    return currentCoordinate, [finalDorabies, finalDoubloons, finalDusts]


"""Start Rising From the Mon(Ashes)"""


def run():
    """
    Description:
        Simulates the game of Rise from the (Mon)Ashes! 
    """
    
    print("""Welcome to Rising from the (Mon)Ashes, a fictional universe set in a planet 
named BERYL where Sentient Artificial Intelligence Bots have taken over.\n""")

    print("SETTING UP UNIVERSE...\n")

    #ADD YOUR CODE TO RUN ALL THE FUNCTIONS ABOVE
    
    # Getting the exchange rates inside the BERYL world.
    dustToDoubloonRate = int(input("Enter the Dusts-To-Doubloons exchange rate:\n"))
    doubloonToDorabieRate = int(input("Enter the Doubloons-to-Dorabies exchange rate:\n"))
    
    numOfCharacters = set_character_number() # Getting the number of characters the player wants.
    
    setNameMode = input("Do you wish to choose the character names manually or automatically (M or A)?\n") # Names input mode.
    
    listOfNames = [] # Storing names of the characters.
    
    if setNameMode == "M":
        listOfNames = set_names_manual(numberOfCharacters=numOfCharacters)
        print()
    else:
        divisibleBy = set_divided_by_integer()
        listOfNames = set_names_automatic(characterList=DEFAULT_CHARACTER_LIST, numberOfCharacters=numOfCharacters, divisibleBy=divisibleBy)
        print()
    
    print("NAVIGATING MAZE...\n")
    
    print(return_welcome_message(names=listOfNames))
    
    def start_game(currentCharacter: str):
        """
        Description:
            Allow to deploy the drone, and navigate to the maze accordingly.
            
        Parameter:
            @param str currentCharacter: Name of the character.
        """
        currentCoordinate = (0,0); currentFunds = [3,0,0]; lastCoordinate = (0,0); reachedEnd = False
        
        print(f"{currentCharacter} starts at position {currentCoordinate} with a BERYL funds list of {currentFunds}")
    
        while not reachedEnd:

            # Printing the maze for the player
            visualise_maze(nestedList=BERYL_MAZE, characterName=currentCharacter, desiredPosition=currentCoordinate)
            print()
            
            desiredDirection = input("Choose a direction:\n")
            dollarIndicator = int(input("Choose a Dollar Indicator digit to find:\n"))
            
            # Deploying the drone to check if the desired Dollar Indicator is present in a specific direction
            visitedCoordinates, visitedIndicators = deploy_drone(nestedList=BERYL_MAZE, currentLocation=currentCoordinate, direction=desiredDirection, dollarIndicator=dollarIndicator)
            
            # If the visitedCoordinates and visitedIndicators are not empty, we then store the funds list to check if there is enough funds for the character or not
            if visitedCoordinates != [] and visitedIndicators != []:
                listOfBerylDollars = beryl_dollar_indicator(visitedIndicators[0], dustToDoubloonRate=dustToDoubloonRate, startingFundsList=currentFunds, doubloonToDorabieRate=doubloonToDorabieRate)
                
                # If the user does not have money, they cannot move further and therefore they will get kicked out of the game.
                if listOfBerylDollars == [0,0,0]:
                    print("Not enough funds!")
                    print(f"{currentCharacter} doesn't have enough money!\n\n{currentCharacter} has no money to move anymore.\n\nMISSION FAILED!\n\n")
                    break
                
            else: # If the user cannot move anywhere, they have reached the restricted area and they will get caught by AI
                print(f"{currentCharacter} has entered a restricted area!\n\n{currentCharacter} tried to act smart and instead got shot down by AI bots.\n\nMISSION FAILED!\n\n")
                break
            
            # Gets the current coordinate the character is in, and the funds they have after they travelled
            currentCoordinate, currentFunds = navigating_maze(visitedList=visitedCoordinates, dollarIndicatorList=visitedIndicators, funds=currentFunds, dustToDoubloonRate=dustToDoubloonRate, doubloonToDorabieRate=doubloonToDorabieRate)
            
            print(f"Reached position {currentCoordinate} with", get_funds_string(currentFunds) + "!")
            
            # If they reach the end of the maze, they have won the game.
            if (currentCoordinate[1] == 10):
                print(f"{currentCharacter} has successfully escaped the maze!\n\nAI BOTS SUCCESSFULLY DEFEATED!\n\n")
                reachedEnd = True
            print()
            
    for name in listOfNames:
        start_game(name)
        
        if len(listOfNames) > 1:
            print("Time for a new game!!\n\n")
        
if __name__ == "__main__":
    run()
