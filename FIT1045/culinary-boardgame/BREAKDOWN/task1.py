def print_game_board(dimension: int, values: dict):
    """
    Description:
    This function prints the game board with given dimensions and values.
    
    Parameters:
    @param int dimension: Dimension of the board.
    @param dict values: Dictionary of values that contains values to be printed.
    """
    # extracting the values from the dictionary, and storing them in a list.
    valuesOfRows = []
    stringToAppend = "" # this string will store the row with values that will be printed inside the boxes.
    
    for index in range( dimension**2 ):
        
        # if the key does not exist, we just have to print an empty box.
        if index not in values:
            stringToAppend += "|" + "     "
        
        # if the key does exist
        else:
            
            valuesToPrint = values[index]
            
            if len(valuesToPrint) == 0: # if the key contains an empty list.
                stringToAppend += "|" + "     "
            
            elif len(valuesToPrint) == 1: # if the key contains one element inside the list.
                stringToAppend += "|" + f"  {valuesToPrint[0]}  "
            
            elif len(valuesToPrint) == 2: # if the key contains two elements inside the list.
                stringToAppend += "|" + f"{valuesToPrint[0]} {valuesToPrint[1]}  "
                
            else: # if the key contains three elements inside the list.
                stringToAppend += "|" + f"{valuesToPrint[0]} {valuesToPrint[1]} {valuesToPrint[2]}"
        
        # values[] will store the rows with values once the end of the row has been met.              
        if (index + 1) % dimension == 0:
            valuesOfRows.append(stringToAppend + "|")
            stringToAppend = "" # resetting the string to default to store values for another row.
            
        
    # printing the top row.
    print(" _____" * dimension)
    
    index = 0 # keeping track of which row with values to print.
    
    # printing the game board.
    for line in range(dimension * 3):
        
        # printing a row of box closing for every third line
        if (line + 1) % 3 == 0:
            print("_____".join(['|'] * (dimension + 1)))
            
        # printing a row with values for every second line
        elif (line + 2) % 3 == 0:
            print(valuesOfRows[index])
            index += 1 # iterates over the next row.
        
        # printing a row with empty spaces for first line
        else:
            print("     ".join(['|'] * (dimension + 1)))
