"""
The program will make the user lose or gain BERYL dollars appropriately, depending
on the variable dollarIndicator.
"""

# taking initial dorabies, doubloons, and dusts and storing them in a list startingFundsList[]
startingFundsList = list( map( int, input("BERYL DOLLAR COLLECTION OR DEPLETION\nEnter number of Dorabie, Doubloon and Dust:\n").split() ) )

# inquiring about the exchange rates
dustsToDoubloons_rate = int(input("Enter the Dusts-to-Doubloons exchange rate:\n"))
doubloonsToDorabies_rate = int(input("Enter the Doubloons-to-Dorabies exchange rate:\n"))

# getting the dollar indicator
dollarIndicator = int(input("Enter the Dollar Indicator:\n"))

# converting dollarIndicator into dusts
totalDusts = 0
if (dollarIndicator> 0): # if dollar indicator is positive.
    
    # first digit of the indicator is the dorabie amount added to the initial dorabie amount.
    convertedDorabies = int( dollarIndicator / 100 )
    remainingDollarIndicator = dollarIndicator - ( convertedDorabies * 100 ) # remaining dollar indicators is calculated.
    
    # second digit of the indicator is the doubloon amount added to the initial doubloon amount.
    convertedDoubloons = int ( remainingDollarIndicator / 10 )
    remainingDollarIndicator = remainingDollarIndicator - convertedDoubloons * 10 # remaining dollar indidcators is calculated.
    
    print("Collected {0} Dorabies, {1} Doubloons and {2} Dusts".format(convertedDorabies, convertedDoubloons, remainingDollarIndicator)) # prints number of dorabie, doubloon, and dust going to be added to the starting funds.
    
    totalDusts = remainingDollarIndicator + ( convertedDoubloons * dustsToDoubloons_rate ) + ( convertedDorabies * ( dustsToDoubloons_rate * doubloonsToDorabies_rate ) ) # convert all of the converted units back to dusts.

else: # if dollar indicator is negative.
    
    # first digit of the indicator is the dorabie amount going to be subtracted from the starting dorabie amount.
    convertedDorabies = int ( dollarIndicator / 10 )
    remainingDollarIndicator = dollarIndicator - ( convertedDorabies * 10 ) # remaining dollar indicators is calculated.
    
    print("Lost {0} Dorabies, {1} Doubloons and 0 Dusts".format( - convertedDorabies, - remainingDollarIndicator)) # prints number of dorabie, doubloons going to be lost from the starting funds.
    
    totalDusts = ( remainingDollarIndicator * dustsToDoubloons_rate ) + ( convertedDorabies * (dustsToDoubloons_rate * doubloonsToDorabies_rate) ) # convert all of the converted units back to dusts.

# getting the starting dorabie, doubloon, and dust amounts from the list startingFundsList[]
startingDorabies = startingFundsList[0]
startingDoubloons = startingFundsList[1]
startingDusts = startingFundsList[2]

# converting starting dorabies, doubloons, dusts all to dusts.
startingTotalDusts = startingDorabies * (dustsToDoubloons_rate * doubloonsToDorabies_rate)
startingTotalDusts += startingDoubloons * (dustsToDoubloons_rate)
startingTotalDusts += startingDusts

# adding the starting dust amount with the dusts converted from the dollar indicator.
finalTotalDusts = startingTotalDusts + totalDusts

# converting the final dusts back to dorabies, doubloons, and remaining dusts
finalDorabies = int ( finalTotalDusts / (dustsToDoubloons_rate * doubloonsToDorabies_rate) )
remainingFinalDusts = finalTotalDusts - ( finalDorabies *  (dustsToDoubloons_rate * doubloonsToDorabies_rate) ) # remaning dusts after dorabie conversion

finalDoubloons = int ( remainingFinalDusts / (dustsToDoubloons_rate) )
finalDusts = remainingFinalDusts - ( finalDoubloons * dustsToDoubloons_rate ) # remaning dusts after doubloon conversion

# if final dorabies, doubloons, dusts are less than 0, the variable should store 0. Otherwise, leave it as it is.
finalDorabies = finalDorabies if finalDorabies > 0 else 0 
finalDoubloons = finalDoubloons if finalDoubloons > 0 else 0
finalDusts = finalDusts if finalDusts > 0 else 0

# final output; if positive dollarIndicator >> funds increased. Otherwise, funds decreased.
if (dollarIndicator > 0):
    print("Funds increased to {0} Dorabies, {1} Doubloons and {2} Dusts".format(finalDorabies, finalDoubloons, finalDusts))
else:
    print("Funds decreased to {0} Dorabies, {1} Doubloons and {2} Dusts".format(finalDorabies, finalDoubloons, finalDusts))
