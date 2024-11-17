"""
The program takes a list of characters and includes a welcome message.
"""
# list of character names
EXAMPLE_CHARACTER_LIST0 = ['LELO MUSK', 'SUPERMARIO', 'MICHONNE', 'WOLVERINE']
EXAMPLE_CHARACTER_LIST1 = ['HOMELANDER', 'TERMINATOR', 'MR. MONASH', 'HERMIONE GRANGER', 'SUNFLOWER']
EXAMPLE_CHARACTER_LIST2 = ['THANOS']
EXAMPLE_CHARACTER_LIST3 = ['TERMINATOR', 'MR. MONASH']
NESTED_EXAMPLE_CHARACTER_LISTS = [EXAMPLE_CHARACTER_LIST0, EXAMPLE_CHARACTER_LIST1, EXAMPLE_CHARACTER_LIST2, EXAMPLE_CHARACTER_LIST3]

# asking user to input the list choice they prefer.
listChoice = int(input("Pick one of the 4 character lists between 0-3 (inclusive)!\n"))

# if the list length is more than 1, it joins the characters names with commas from index 0 to the second last of the list.
if len(NESTED_EXAMPLE_CHARACTER_LISTS[listChoice]) == 1: # if len() == 1
    print("It is the year 3045. Sentient Artificial Intelligence Bots have now taken over.\n{0} must rise from the (Mon)ashes!\nThey are BERYL's only hope!".format(NESTED_EXAMPLE_CHARACTER_LISTS[listChoice][0]))
else: # if len() > 1
    print("It is the year 3045. Sentient Artificial Intelligence Bots have now taken over.\n{0} and {1} must rise from the (Mon)ashes!\nOnly one character may survive!".format(", ".join(NESTED_EXAMPLE_CHARACTER_LISTS[listChoice][:-1]), NESTED_EXAMPLE_CHARACTER_LISTS[listChoice][-1]))
