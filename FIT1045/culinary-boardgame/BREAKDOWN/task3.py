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


class Restaurant:
    """
    DUMMY CLASS
    You may leave this blank as your RestaurantManager Class will still work with this class left empty.
    """
    pass
