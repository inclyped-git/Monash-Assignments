"""
Main idea: The program will convert amount of Dusts to appropriate Dorabie, Doubloon, and remaining
Dusts amounts.    
"""

# amountOfDuts takes in the number of dusts the user wants to convert.
amountOfDusts = int( input("BERYL DOLLAR CONVERSION\nEnter the amount of Dusts you wish to convert:\n") )

# getting the exchange rates from the user.
dustToDoubloon_rate = int( input("Enter the Dusts-to-Doubloons exchange rate:\n") )
doubloonToDorabies_rate = int( input("Enter the Doubloons-to-Dorabies exchange rate:\n") )

# the dust to dorabie rate is identical to dust to doubloon rates multiplied with doubloon to dorabie rates.
dustToDorabie_rate = (dustToDoubloon_rate * doubloonToDorabies_rate) 

# converting dusts to dorabies and remaining dusts.
convertedDorabies =  int ( amountOfDusts / dustToDorabie_rate )
remainingDusts = amountOfDusts - ( convertedDorabies * dustToDorabie_rate )

# converting remaining dusts to doubloons and final dusts.
convertedDoubloons = int ( remainingDusts / (dustToDoubloon_rate) )
convertedDusts = remainingDusts - ( convertedDoubloons * dustToDoubloon_rate )

print("{0} Dusts has been converted to {1} Dorabies, {2} Doubloons and {3} Dusts".format( amountOfDusts, convertedDorabies, convertedDoubloons, convertedDusts ))
