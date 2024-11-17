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

class RestaurantManager:
    """
    DUMMY CLASS
    You may leave this blank as your Restaurant Class will still work with this class left empty.
    """
    pass
