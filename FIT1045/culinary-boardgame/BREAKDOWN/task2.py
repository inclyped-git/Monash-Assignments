def retrieve_restaurant_details(data: list, delimiter: str, board_size: int) -> dict:
    """
    Description:
    This function extracts data from csv format to give each position in the game board with
    appropriate restaurant details.
    
    Parameters:
    @param list[] data: The csv data that contains details of restaurants.
    @param str delimiter: The character that separates the information of each detail.
    @param int board_size: The dimension size.
    
    Returns:
    @return dict: A dictionary with postions as keys and restaurant details as values.
    """
    
    # extracting the titles' postions inside the csv data.
    titles = data[0].split(delimiter)
    
    # getting the indexes of each title
    restaurantNameIndex = titles.index('Restaurant Name')
    restaurantTypeIndex = titles.index('Type')
    restaurantPriceIndex = titles.index('Price')
    restaurantPositionIndex = titles.index('Board Position')
    
    finalDictionary = {} # used to store the extracted details from the csv data.
    
    bigData = data[1:] # excluding the titles from the details.
    
    offset = 0 # required to shift the iterator to avoid diagonal indexes.
    
    for index in range(len(bigData)):
        # getting the restaurant data
        restaurantData = bigData[index].split(delimiter)
        
        # getting the list to store in the dictionary with the key as the position of the restaurant.
        valueToStore = [restaurantData[restaurantNameIndex], restaurantData[restaurantTypeIndex], restaurantData[restaurantPriceIndex]]
        keyToStore = int( restaurantData[restaurantPositionIndex] ) + offset
        
        # if the diagonal index has been encountered, it skips to the next index and stores the list.
        if keyToStore % ( board_size - 1 ) == 0 and keyToStore > 0 and keyToStore < board_size**2 - 1:
            finalDictionary[keyToStore + 1] = valueToStore
            offset += 1
        
        # if it is not a diagonal index
        else:
            finalDictionary[keyToStore] = valueToStore
    
    return finalDictionary
