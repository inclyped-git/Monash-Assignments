# visited arrays and dollar indicators
visited0 = [(3,2), (3,3), (3,4)] 
dollar_indicator0 = [235, -12, -89]

visited1 = [(3,4), (2,4), (1,4)]
dollar_indicator1 = [-89, -76, 365]

visited2 = [(2, 2), (2, 3), (2, 4), (2, 5)]
dollar_indicator2 = [112, -46, -76, -11]

# combined all the visited and dollar indicators
VISITED_LIST= [visited0,visited1,visited2]
DOLLAR_INDICATOR_LIST= [dollar_indicator0,dollar_indicator1,dollar_indicator2]

# getting the amount of dorabies, doubloons and dusts from the user.
listOfBerylDollars = list(map(int, input("Enter number of Dorabie, Doubloon and Dust:\n").split()))        

# getting the exchange rates
dustsToDoubloons = int(input("Enter the Dusts-to-Doubloons exchange rate:\n"))
dustsToDorabies = int(input("Enter the Doubloons-to-Dorabies exchange rate:\n")) * dustsToDoubloons

# list of choice
listOfChoice = int(input("Pick one of the 3 character lists between 0-2 (inclusive)!\n"))

# total dusts before manipulating it with the dollar indicator.
totalDustsBefore = listOfBerylDollars[0] * dustsToDorabies + listOfBerylDollars[1] * dustsToDoubloons + listOfBerylDollars[2]

"""
Description: Converts all of the indicator into dorabies, doubloons and dusts, and also convert all of them to dusts.

@param indicator: int -> takes in the dollar indicator
@return int

"""
def convertDollarIndicatorToDust(indicator):
    if indicator > 0:
        convertedDorabies = int(indicator / 100)
        remainingIndicator = indicator - convertedDorabies * 100
        
        convertedDoubloons = int(remainingIndicator / 10)
        remainingIndicator = remainingIndicator - convertedDoubloons * 10
        
        return remainingIndicator + convertedDoubloons * dustsToDoubloons + convertedDorabies * dustsToDorabies

    elif indicator < 0:
        indicator = -1 * indicator
        convertedDorabies = int ( indicator / 10 )
        remainingIndicator = indicator - convertedDorabies * 10
        
        return -1 * ( convertedDorabies * dustsToDorabies + remainingIndicator * dustsToDoubloons )
    
    return 0

# sentinel
canExitLoop = False
index = 0 # keeping track of the count
currentCoordinate = (0, 0)

totalDustsAfter = totalDustsBefore
finalDorabies = 0; finalDoubloons = 0; finalDusts = 0

while not canExitLoop and index < len(VISITED_LIST):
    currentCoordinate = VISITED_LIST[listOfChoice][index]
    currentIndicator = DOLLAR_INDICATOR_LIST[listOfChoice][index]
    
    totalDustsAfter += convertDollarIndicatorToDust(currentIndicator)
    
    finalDorabies = int (totalDustsAfter / dustsToDorabies) if int (totalDustsAfter / dustsToDorabies) > 0 else 0
    remainingDusts = totalDustsAfter - finalDorabies * dustsToDorabies
    
    finalDoubloons = int (remainingDusts / dustsToDoubloons) if int (remainingDusts / dustsToDoubloons) > 0 else 0
    remainingDusts = remainingDusts - finalDoubloons * dustsToDoubloons
    
    finalDusts = remainingDusts if remainingDusts > 0 else 0
    
    if totalDustsAfter < 0:
        canExitLoop = True
    
    index += 1
        
print(f"Reached position {currentCoordinate} with {finalDorabies} Dorabies, {finalDoubloons} Doubloons and {finalDusts} Dusts")
