"""
Main idea: The program takes in three BERYL dollar units and prints them appropriately in the console.
"""

"""
The list listOfBerylDollars[] will take in the appropriate number of Dorabies, Doubloons and Dusts,
and store them individually inside of a list.
"""
# takes in three numbers; later converts the string numbers into integer data type, and store them in a list.
listOfBerylDollars = list( map( int, input("BERYL DOLLAR FUNDS\nEnter number of Dorabie, Doubloon and Dust:\n" ).split() ) )

# while loop runs indefinitely until the user enters exactly three numbers.
while ( len( listOfBerylDollars ) != 3 ):

    # prints the appropriate error message; and re-prompts the user to input three numbers.
    listOfBerylDollars = list( map( int, input("Please enter following the proper format e.g. 3 5 10\nEnter number of Dorabie, Doubloon and Dust:\n").split() ) )

# extracting dorabies, doubloons, and dusts and storing them in appropriate variables.
numOfDorabies = listOfBerylDollars[0]
numOfDoubloons = listOfBerylDollars[1]
numOfDusts = listOfBerylDollars[2]

# manipulates string if numbers of dorabies, doubloons, and dusts are greater or equal to 1.
hasMultipleDorabies = "Dorabies" if ( numOfDorabies > 1 or numOfDorabies == 0 ) else "Dorabie"
hasMultipleDoubloons = "Doubloons" if ( numOfDoubloons > 1 or numOfDoubloons == 0 ) else "Doubloon"
hasMultipleDusts = "Dusts" if ( numOfDusts > 1 or numOfDusts == 0) else "Dust"

# printing the final output
print("You have {0} {1}, {2} {3} and {4} {5}".format( numOfDorabies, hasMultipleDorabies, numOfDoubloons, hasMultipleDoubloons, numOfDusts, hasMultipleDusts ))
