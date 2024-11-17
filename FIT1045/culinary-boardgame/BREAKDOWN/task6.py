from abc import ABC, abstractmethod
import random

class RestaurantManager:
    """
    Description: RestaurantManager is a class that contains the attributes of a manager -
    their name, their symbol, their bitecoins, the number of restaurants managed, and 
    what positions they currently own.
    """
    INITIAL_CAPITAL = 1000
    
    def __init__(self, name: str):
        """
        Description: Constructor for the RestaurantManager class.
        
        Parameters:
        @param str name: String that is the name of the restaurant manager.
        """
        self.name = name
        self.symbol = self.name.upper()[0]
        self.bitecoins = RestaurantManager.INITIAL_CAPITAL
        self.restaurants_managed = []
        self.manager_positions = []
        
    # set of getters.
    def get_name(self) -> str:
        """
        Description: Getter method for the instance variable "name".

        Returns:
        @return str: The name of the manager.
        """
        return self.name

    def get_symbol(self) -> str:
        """
        Description: Getter method for the instance variable "symbol".

        Returns:
        @return str: The starting character of the manager's name.
        """
        return self.symbol
    
    def get_bitecoins(self) -> int:
        """
        Description: Getter method for the instance variable "bitecoins".
        
        Returns:
        @return int: The number of bitecoins the manager currently has.
        """
        return self.bitecoins

    
    def get_restaurants_managed(self) -> list:
        """
        Description: Getter method for the instance variable "restaurants_managed"

        Returns:
        @return list: A list of restaurants the manager manages.
        """
        return self.restaurants_managed

    def get_manager_positions(self) -> list:
        """
        Description: Getter method for the instance variable "manager_positions"

        Returns:
        @return list: A list of positions the manager owns.
        """
        return self.manager_positions

    
    # set of updators and retrievers
    def update_bitecoins(self, coins: int):
        """
        Description: Updates the bitecoins the manager has.

        Parameters:
        @param int coins: The number of coins lost or gained by the manager.
        """
        self.bitecoins = self.get_bitecoins() + coins
        
    
    def update_position(self, pos: int):
        """
        Description: Appends the latest position the manager owns.

        Parameters:
        @param int pos: The new position the manager has occupied.
        """
        self.get_manager_positions().append(pos)
    
    def get_current_position(self) -> int:
        """
        Description: Returns the current position of the manager.

        Returns:
        @return int: The position of the manager.
        """
        return self.get_manager_positions()[-1]
    
    
    def undo_position(self) -> int:
        """
        Description: 

        Returns:
        @return int: The previous position the manager was in.
        """
        self.manager_positions = self.get_manager_positions()[:-1]
        return self.get_manager_positions()[-1]
    
    def update_restaurants_managed(self, restaurant: object):
        """
        Description: Appends the restaurant the manager owns.

        Parameters:
        @param Restaurant restaurant: The restaurant object that the manager owns.
        """
        if restaurant not in self.get_restaurants_managed():
            self.get_restaurants_managed().append(restaurant)
    
    # string rep functions
    def __str__(self) -> str:
        """
        Description: A function that represents the details of the restaurant manager object.

        Returns:
        @return str: A string that contains details of the RestaurantManager object.
        """
        return f"{self.get_name()} has {self.get_bitecoins()} BiteCoins and manages {len(self.get_restaurants_managed())} restaurant(s)"
    
    def __repr__(self) -> object:
        """
        Description: __repr__() function calls the __str__() function.

        Returns:
        @return str: A string that is returned by __str__() function.
        """
        return self.__str__()

    def buy_restaurant(self, restaurantsDictionary: dict, boardPosition: int) -> str:
        """
        Description: Behaviour to allow the manager to buy shares of available restaurants.

        Parameters:
        @param dict restaurantsDictionary: Contains details of the restaurants, which could either be a list or a Restaurant object.
        @param int boardPosition: The board position of the restaurant the manager wants to buy in.

        Returns:
        @return str: A string that indicates whether the manager was able to purchase the restaurant.
        """
        restaurantDetails = restaurantsDictionary[boardPosition] # gets the details from a specific position.
        
        # checking if the details is a list type or Restaurant type.
        if isinstance(restaurantDetails, list):
            # if its a list, the restaurant has not been bought yet. 
            # if the manager cannot afford the restaurant, it does not convert to a restaurant object.
            if self.get_bitecoins() < int(restaurantDetails[2]): 
                return f"{self.get_name()} does not have enough money to afford {restaurantDetails[0]}"
            
            # if the manager can afford, the Restaurant constructor is called in with specified fields.
            restaurantsDictionary[boardPosition] = Restaurant(restaurantDetails[0], restaurantDetails[1], restaurant_price=int(restaurantDetails[2]), board_position=boardPosition)
                
            # updating the restaurants managed, position and bitecoins of the manager.
            self.update_restaurants_managed(restaurantsDictionary[boardPosition])
            self.update_position(boardPosition)
            self.update_bitecoins(-restaurantsDictionary[boardPosition].get_restaurant_price())
                
            # adding a new comanager to the restaurant.
            restaurantsDictionary[boardPosition].add_new_comanager(self)
            
            # since the manager was the first one to purchase the share, they become the first manager.
            return f"{self.get_name()} becomes the first manager of {restaurantsDictionary[boardPosition].get_restaurant_name()}"
        
        else:
            # if its already an object, we can check if the restaurant is not available.
            if not (restaurantsDictionary[boardPosition].has_manager_availability()):
                return f"{restaurantsDictionary[boardPosition].get_restaurant_name()} is no longer available"
            
            # if the restaurant is available, we can check if the manager can afford the restaurant shares.
            if self.get_bitecoins() < restaurantsDictionary[boardPosition].get_restaurant_price():
                return f"{self.get_name()} does not have enough money to afford {restaurantsDictionary[boardPosition].get_restaurant_name()}"

            # updating the fields if the manager can buy the shares.
            self.update_restaurants_managed(restaurantsDictionary[boardPosition])
            self.update_position(boardPosition)
            self.update_bitecoins(-restaurantsDictionary[boardPosition].get_restaurant_price())
            restaurantsDictionary[boardPosition].add_new_comanager(self)
            
            # if there is only one manager managing the restaurant,
            if (restaurantsDictionary[boardPosition].has_sole_manager()):
                # the manager is a sole manager if he owns 100% otherwise he is just main.
                replaceString = "a sole manager" if restaurantsDictionary[boardPosition].get_managerial_share(self) == 100 else "the head manager"
            # if there are multiple managers managing the restaurant,
            else:
                # the manager is a head if he owns 60%+, otherwise he is just a co-manager.
                replaceString = "the head manager" if restaurantsDictionary[boardPosition].get_managerial_share(self) >= 60 else "co-manager"
            
            return f"{self.get_name()} becomes {replaceString} of {restaurantsDictionary[boardPosition].get_restaurant_name()}"

                    
            
    def display_restaurants_managed(self):
        """
        Description: Prints a list of restaurants managed by the manager, alongside the total BiteCoins worth of restaurants
                     managed and the shares owned.
        """
        
        # variables to keep track of the bitecoins and shares.
        totalBitecoinsWorth = 0
        totalSharesWorth = 0
        
        # traversing through each restaurant type inside the class variable RESTAURANT_TYPES in Restaurant class.
        for restaurantType in Restaurant.RESTAURANT_TYPES:
            
            # since we need to print restaurants that are of particular restaurant types, we are choosing only the 
            # restaurants that are matching with the restaurantType.
            availableRestaurants = [ restaurant for restaurant in self.get_restaurants_managed() if restaurant.get_restaurant_type() == restaurantType ]
            
            # if any element exists, print the type title.
            if availableRestaurants:
                print(restaurantType.upper())
                
                # repetitively adding the BiteCoins and Shares of the restaurants, while printing the list of restaurants
                # for a particular restaurant type.
                for index, restaurantInList in enumerate(availableRestaurants, start=1):
                    totalBitecoinsWorth += restaurantInList.get_restaurant_price() * int ( restaurantInList.get_managerial_share(self) / 30 )
                    totalSharesWorth += restaurantInList.get_restaurant_price() * ( restaurantInList.get_managerial_share(self) / 100 )
                    
                    print(f"{index}. {restaurantInList.get_restaurant_name()} ({restaurantInList.get_restaurant_price()} BiteCoins, {restaurantInList.get_managerial_share(self)}%)")
        
        # printing end statements.
        print("OVERALL")
        print(f"Restaurants worth {totalBitecoinsWorth} BiteCoins")
        print(f"Managerial shares worth {int ( totalSharesWorth )} BiteCoins")            
            
                
                    
    def lose_bitecoin(self, restaurantsDictionary: dict):
        """
        Description: Update BiteCoins of managers that enter the restaurants they do not manage.

        Parameters:
        @param dict restaurantsDictionary: Details of all restaurants.
        """
        # assuming the restaurant at the current position is a Restaurant object, we can access the object through this code.
        restaurantDetail = restaurantsDictionary[self.get_current_position()]

        # keeping track of the bitecoins to lose for the manager.        
        bitecoinsToLose = 0
        
        # a list of managers to pay the 50% fee, excluding the members that are themselves inside the list.
        managerPayList = [ manager for manager in list(set(restaurantDetail.get_managers_list())) if manager != self ]
        
        # updating bitecoins
        for manager in managerPayList:
            moneyGained = round( (restaurantDetail.get_managerial_share(manager) / 100) * (restaurantDetail.get_restaurant_price() * 0.5) + 0.1)
            manager.update_bitecoins(moneyGained)
            self.update_bitecoins(-moneyGained)    
        
           
    def check_winning_conditions(self, numOfRestaurants: int = 4,avgManagerialShare: float = 0,numOfTypes: int = 3) -> bool:
        """
        Description: Checks whether the manager is within the winning conditions to win the game.

        Parameters:
        @param int numOfRestaurants: Number of restaurants needed to own to win the game; default is 4.
        @param float avgManagerialShare: Average managerial share needed to win the game; default is 0.
        @param int numOfTypes: Number of types of restaurants to own in order to win the game; default is 1.

        Returns:
        @return bool: Returns whether the manager wins or not.
        """
        # checking if the number of restaurants owned meets the criteria.
        if not len(self.get_restaurants_managed()) >= numOfRestaurants:
            return False
        
        # checking if the average managieral share meets the criteria.
        listOfShares = [ restaurant.get_managerial_share(self) for restaurant in self.get_restaurants_managed() ]
        average = sum(listOfShares) / len(listOfShares)
        
        if not average >= avgManagerialShare:
            return False
        
        # checking if the types of restaurants meet the criteria.
        numOfTypesOwned = len(list(set([ restaurant.get_restaurant_type() for restaurant in self.get_restaurants_managed() ])))
        if not numOfTypesOwned >= numOfTypes:
            return False
        
        return True

    def get_next_positions(self, detailsDictionary):
        boardSize = int ( ( list(detailsDictionary.keys())[-1] + 1 ) ** 0.5 )
        boardRow = int ( self.get_current_position() / (boardSize) )
        boardColumn = int ( self.get_current_position() % (boardSize) )

        isASoleManager = any([restaurant.has_sole_manager() and restaurant.get_managerial_share(self) == 100 for restaurant in self.get_restaurants_managed()])
        listOfCoordinates = []
        # checking for up
        if boardRow - 1 >= 0:
            listOfCoordinates.append((boardRow - 1, boardColumn))
        
        # checking for down 
        if boardRow + 1 <= (boardSize - 1):
            listOfCoordinates.append((boardRow + 1, boardColumn))
        
        # checking for left
        if boardColumn - 1 >= 0:
            listOfCoordinates.append((boardRow, boardColumn - 1))
        
        # checking for right
        if boardColumn + 1 <= (boardSize - 1):
            listOfCoordinates.append((boardRow, boardColumn + 1))
        
        if isASoleManager:
            # checking for diagonal up left
            if boardRow - 1 >= 0 and boardColumn - 1 >= 0:
                listOfCoordinates.append((boardRow - 1, boardColumn - 1))
            
            # checking for diagonal up right
            if boardRow - 1 >= 0 and boardColumn + 1 <= (boardSize - 1):
                listOfCoordinates.append((boardRow - 1, boardColumn + 1))
            
            # checking for diagonal down left
            if boardRow + 1 <= (boardSize - 1) and boardColumn - 1 >= 0:
                listOfCoordinates.append((boardRow + 1, boardColumn - 1))
            
            # checking for diagonal down right
            if boardRow + 1 <= (boardSize - 1) and boardColumn + 1 <= (boardSize - 1):
                listOfCoordinates.append( (boardRow+1, boardColumn+1) )
                
        return (sorted([ coordinate[0] * boardSize + coordinate[1] for coordinate in listOfCoordinates ]))
        
   
class Restaurant:
    """
    Description: Restaurant is a class that contains the attributes and behaviours of a restaurant.
    Attributes include their name, type, price, board position, and the list of managers managing
    the place. Behaviours include checking manager availability, adding new comanagers, checking if
    the restaurant is owned by a single manager, and checking the managerial share of a manager of
    a given restaurant.
    """
    # static (class) variable
    RESTAURANT_TYPES = ['Desserts & Beverages', 'Farm-to-Table', 'Fusion Cuisine', 'Fast Food']
    
    def __init__(self, restaurant_name: str, restaurant_type: str, restaurant_price: int, board_position: int):
        """
        Description: Constructor for the Restaurant class.

        Parameters:
        @param str restaurant_name: String that represents the name of the restaurant.
        @param str restaurant_type: String that represents the type of restaurant.
        @param int restaurant_price: Integer that represents the price of buying the restaurant.
        @param int board_position: Integer that represents the board position of the restaurant.
        """
        self.restaurant_name = restaurant_name
        self.restaurant_type = restaurant_type
        self.restaurant_price = restaurant_price
        self.board_position = board_position
        self.managers_list = []
    
    # set of getters.
    def get_restaurant_name(self) -> str:
        """
        Description: Getter method for the instance variable "restaurant_name"

        Returns:
        @return str: The name of the restaurant.
        """
        return self.restaurant_name
    
    def get_restaurant_type(self) -> str:
        """
        Description: Getter method for the instance variable "restaurant_type"

        Returns:
        @return str: The type of restaurant.
        """
        return self.restaurant_type
    
    def get_restaurant_price(self) -> int:
        """
        Description: Getter method for the instance variable "restaurant_price"

        Returns:
        @return int: The price of buying the restaurant.
        """
        return self.restaurant_price
    
    def get_board_position(self) -> int:
        """
        Description: Getter method for the instance variable "board_position"

        Returns:
        @return int: The board position of the restaurant.
        """
        return self.board_position
    
    def get_managers_list(self) -> list:
        """
        Description: Getter method for the instance variable "managers_list"

        Returns:
        @return list: A list of RestaurantManager objects.
        """
        return self.managers_list
    
    
    # set of updators and retrievers
    def has_manager_availability(self) -> bool:
        """
        Description: Checks if there is any space for a new manager to manage the restaurant.

        Returns:
        @return bool: True if there are less than three managers managing the restaurant.
        """
        return len(self.get_managers_list()) < 3
    
    def add_new_comanager(self, manager: object):
        """
        Description: Adds a new comanager to the list if there is any space available.

        Parameters:
        @param RestaurantManager manager: Manager to add to the list of managers managing the restaurant.
        """
        if (self.has_manager_availability()):
            self.get_managers_list().append(manager) # add only if there is space left.
        
        # keeping the symbols of the manager together if the same manager symbol is spotted on the first and last index of the managers list.
        if len(self.get_managers_list()) == 3:
            if (self.get_managers_list()[2] == self.get_managers_list()[0]):
                # swapping the second and third symbol.
                temp = self.get_managers_list()[1]
                self.get_managers_list()[1] = self.get_managers_list()[2]
                self.get_managers_list()[2] = temp
            
    def has_sole_manager(self) -> bool:
        """
        Description: Checks if only one manager owns all of the restaurant.

        Returns:
        @return bool: Returns true if the same manager occupied three spaces of the managers list.
        """
        # using set() method to store unique RestaurantManager objects only.
        return len ( list ( set (self.get_managers_list()) ) ) == 1 

    def get_managerial_share(self, manager: object) -> int:
        """
        Description: Returns the number of shares the manager has for the restaurant.

        Parameters:
        @param RestaurantManager manager: The manager's shares to be checked.

        Returns:
        @return int: The shares owned by the manager.
        """
        sumManagerialShare = 0 # storing the number of shares the manager has.
        if manager in self.get_managers_list():
            for i in range( len (self.get_managers_list()) ):
                
                # if the manager is in the first index of the managers list, they will have 40% of shares.
                # otherwise, it is 30% of shares.
                if self.get_managers_list()[i] == manager:
                    sumManagerialShare += (40 if i == 0 else 30)
        
        return sumManagerialShare
    
    def __str__(self) -> str:
        """
        Description: A function that returns the name of the restaurant.

        Returns:
        @return str: A string that contains the name of the restaurant.
        """
        return self.get_restaurant_name()
    
    def __repr__(self) -> object:
        """
        Description: __repr__() functions calls the __str__() function

        Returns:
        @return object: The function object __str__() is returned, which returns a string.
        """
        return self.__str__()

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
    
    
class DiagonalGrid(ABC):
    """
    Description: DiagonalGrid is an abstract class that contains the template of the attributes and behaviours
                 that a grid can inherit and implement. Each grid has its own name, dedicated board position,
                 and the restaurant from which is accessed from the dictionary passed as an argument. The only
                 abstract method implemented here allows to give an effect to the managers.
    """
    
    def __init__(self, board_position: int, details_dictionary: dict):
        """
        Description: Constructor for the DiagonalGrid class.

        Parameters:
        @param int board_position: The board position of one particular restaurant.
        @param dict details_dictionary: The dictionary the program will access the restaurant details from.
        """
        self.grid_name = ""
        self.board_position = board_position
        self.details_dictionary = details_dictionary
    
    @abstractmethod
    def receive_grid_effect(self, manager: object):
        """
        Description: Abstract method to be implemented in child classes.

        Parameters:
        @param RestaurantManager manager: The manager object that will be going through the effect.
        """
        pass

    def __str__(self) -> str:
        """
        Description: String representation function for the class.
        
        Returns:
        @return str: String that represents the name of the grid.
        """
        return self.grid_name
    
    def __repr__(self) -> object:
        """
        Description: Returns the string representation __str__() function

        Returns:
        @return object: __str__() function will be returned.
        """
        return self.__str__()

class StartGrid(DiagonalGrid):
    """
    Description: StartGrid is a child class of the DiagonalGrid class that contains the attributes and 
                 behaviours of a start grid in the game board.
    """
    
    def __init__(self, board_position: int, details_dictionary: dict):
        """
        Description: Constructor for the StartGrid class.

        Parameters:
        @param int board_position: The position of the start grid.
        @param dict details_dictionary: The dictionary details that the board will be using.
        """
        super().__init__(board_position, details_dictionary)
        self.grid_name = "Start Grid"
    
    def receive_grid_effect(self, manager: object) -> str:
        """
        Description: Gives the manager 200 BiteCoins when they arrive to the start grid.

        Parameters:
        @param RestaurantManager manager: The manager that is currently playing in the game.

        Returns:
        @return str: The result of the grid effect taking place.
        """
        manager.update_bitecoins(200)
        return f"GRID EFFECT: {manager.get_name()} collected 200 BiteCoins as you reached the starting position!\nTotal BiteCoins now: {manager.get_bitecoins()}"

class ChanceGrid(DiagonalGrid):
    """
    Description: ChanceGrid is a child class of the DiagonalGrid class that contains the attributes
                 and behaviours of a chance grid in the game board.
    """
    def __init__(self, board_position: int, details_dictionary: dict):
        """
        Description: Constructor for the ChanceGrid class.

        Parameters:
        @param int board_position: The position of where the chance grid will be.
        @param dict details_dictionary: The dictionary that contains the restaurant details.
        """
        super().__init__(board_position, details_dictionary)
        self.grid_name = "Chance Grid"
        
    def receive_grid_effect(self, manager: object) -> object:
        """
        Description: Randomly chooses which effect to take place when landing on a chance grid.

        Parameters:
        @param RestaurantManager manager: The manager that is currently playing the game.

        Returns:
        @return str: The result of the effect taking place.
        """
        return random.choice([self.get_reward, self.get_penalty, self.get_randomly_transported])(manager)
      
    def get_reward(self, manager: object) -> str:
        """
        Description: Increases the manager's bitecoins by 50%.

        Parameters:
        @param RestaurantManager manager: The manager that is currently playing.

        Returns:
        @return str: The result of the reward effect taking place.
        """
        toCollect = int (manager.get_bitecoins() * 0.5)
        manager.update_bitecoins(toCollect)
        return f"GRID EFFECT: {manager.get_name()} collected {toCollect} BiteCoins\nTotal BiteCoins now: {manager.get_bitecoins()}"
    
    def get_penalty(self, manager: object) -> str:
        """
        Description: Deducts the manager's bitecoins by 30%

        Parameters:
        @param RestaurantManager manager: The manager that is currently playing.

        Returns:
        @return str: The result of the penalty effect taking place.
        """
        toLose = -1 * int (manager.get_bitecoins() * 0.3)
        manager.update_bitecoins(toLose) 
        return f"GRID EFFECT: {manager.get_name()} lost {- toLose} BiteCoins\nTotal BiteCoins now: {manager.get_bitecoins()}"
        
    
    def get_randomly_transported(self, manager):
        position = random.choice(list(self.details_dictionary.keys()))
        
        while position == manager.get_current_position():
            position = random.choice(list(self.details_dictionary.keys()))
        
        manager.update_position(position)
        beforeEffect = manager.get_bitecoins()
        
        print(f"GRID EFFECT: {manager.get_name()} has been moved to position {manager.get_current_position()} on the board!")
        
        print(manager.buy_restaurant(self.details_dictionary, manager.get_current_position()))
        
        # we need to consider if the restaurant is a list or object.
        if isinstance(self.details_dictionary[manager.get_current_position()], Restaurant):
            if not self.details_dictionary[manager.get_current_position()].has_manager_availability():
                if self.details_dictionary[manager.get_current_position()].get_managerial_share(manager) == 0:
                    manager.lose_bitecoins(self.details_dictionary)
        
        return f"Total BiteCoins left: {manager.get_bitecoins()}"
