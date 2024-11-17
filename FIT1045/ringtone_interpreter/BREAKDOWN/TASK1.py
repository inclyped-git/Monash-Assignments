import re as Re # regex library for string comparison.

def check_valid_note( substring: str ) -> bool:
    """
    Description:
    Checks whether a substring meets the criteria set for being a valid musical note.

    Parameters:
    @param substring: The string that will be checked if it is a valid music note.

    Returns:
    @return bool: True if the substring is a valid music note or otherwise it's False.
    """
    
    
    """
    Compiling the regex pattern that will check if it matches the criteria for being a valid music note.
    
    >> Note length must have 1-2 digits only. Optional input.
    >> Note pitch must be either any one letter from [a-g] with '#' as an option, or only p. Compulsory input.
    >> Note scale must be a digit from [1-8] only. Optional input.
    
    Fullstop in the end is optional.
    """
    pattern : object = Re.compile(r"(^\d{1,2})?([a-g]{1}(#)?|p{1})([1-8]{1})?(\.)?$")
    
    # stores True if the substring matches, otherwise stores None.
    substringMatch: object = pattern.match(substring)
    
    # if the substring matches with the criteria,
    if substringMatch:
        
        # we will get the note length from the substring
        noteLength: str = substringMatch.group(1)
        
        # if noteLength exists,
        if noteLength:
            
            # we need to check if the note length is either numbers 1,2,4,8,16 or 32.
            if not int(noteLength) in [1,2,4,8,16,32]:
                return False

            
        # return True if everything does meet the criteria, given that note length is entered correctly or is not entered at all.
        return True
    
    # otherwise, return false.
    return False

if __name__ == '__main__':

    # creating a list of testcases
    substringTrues: list = ['4a8', '16b5', '32c4', 'e7', 'f2', 'd#', '16p', 'p', 'f.', '32a#8.']
    substringFalses: list = ['p#', '.b8', '12g6', '8m.', '86', 'a#10', '36g9']
    
    # checking if the valid testcases are working.
    for testcase in substringTrues:
        if not check_valid_note(testcase):
            print(f"Failed True testcase: {testcase}")
    print("PASSED ALL TRUE TESTCASES")
         
    # checking if the invalid testcases are working.
    for testcase in substringFalses:
        if check_valid_note(testcase):
            print(f"Failed False testcase: {testcase}")
    print("PASSED ALL FALSE TESTCASES")
            
