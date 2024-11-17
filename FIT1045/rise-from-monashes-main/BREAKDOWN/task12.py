BERYL_MAZE = [
  [300, -13, 189, -15, -12, 203, -23, 587, -78, 321, -46],
  [300, -11, -13, -24, 365, 198, -34, -21, 789, -81, -53],
  [300, -12, 112, -46, -76, -11, -23, -59, 321, 204, -32],
  [300, -23, 235, -12, -89, -62, -34, 212, -56, -67, -89],
  [300, 376, -23, -77, 227, -99, 134, 289, -12, 476, -51]
]

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
        

    elif direction == "down":
        for index in range(row+1, len(nestedList)):  # looping through each row of the same column, downwards.
            if str(dollarIndicator) not in str(nestedList[index][column]):
                coordinates.append( (index, column) )
                indicators.append( nestedList[index][column] )
            
            else:
                coordinates.append( (index, column) )
                indicators.append( nestedList[index][column] )
                foundDigit = True
                print(f"Found digit at location { (index, column)}!\n")
                return coordinates, indicators
  
        if not foundDigit:
            print(f"Entered restricted area!\n")
            return [],[]

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
if __name__ == "__main__":
    visited_position_list = [(2, 2), (2, 3), (2, 4), (2, 5)]
    dollar_indicator_list = [112, -46, -76, -11]
    funds = [8, 2, 3]
    position, funds = navigating_maze(visited_position_list, dollar_indicator_list, funds, 20, 10)
    print(position)
    print(funds)
