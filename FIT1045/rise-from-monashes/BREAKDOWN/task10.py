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

#for debugging purpose only, please delete during final submission
if __name__ == "__main__":
    print(get_funds_string([4,5,19]))
    print(beryl_dollar_conversion(540, 20, 5)) 
    print(beryl_dollar_indicator(152, [0,3,5], 10, 5))
