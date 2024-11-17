import re as Re # regex library for string comparison.
import unittest # unit test library for testing purposes.

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

def generate_valid_ringtone( ringtone: str ) -> list:
    """
    Description: Returns a list of title, default values and notes data from a given
                 ringtone. Returns an empty list if the given ringtone string does not meet
                 the criteria.

    Parameters:
    @param ringtone: Ringtone string that contains all of the data.

    Returns:
    @return list: A list containing the details of the ringtone.
    """
    
    # if there is no string, return empty list.
    if not any( ringtone ):
        return []
    
    # splitting the string into respective fields: title, default values, and note data.
    optionalData : tuple
    noteData: str
    
    *optionalData, noteData = Re.split( ':', ringtone )
    
    # converting all characters to lowercase in notedata and stripping any whitespace.
    noteData : str = Re.sub(r'\s','',noteData).lower()
    
    ###TECHNIQUE: LIST COMPREHENSION###
    # checking if all of the substrings in the note data is a valid note.
    if all( [ check_valid_note( substring ) for substring in Re.split( ',', noteData )] ):
        
        # now we will check if the default values syntax is correct or not.
        
        # default values section must be either empty or must have d=x,o=x,b=x for some number x.
        defaultValuesPattern : object = Re.compile( r"^(\s*|(d=[1-9]\d*,o=[1-9]\d*,b=[1-9]\d*))$" )
        
        # if there is any optional data written,
        if any (optionalData):
            
            # if the default values are matching the criteria.
            if defaultValuesPattern.match( Re.sub( r'\s','',optionalData[-1] ).lower() ):
                
                # return only empty title, default values and notedata if only default values are given, else print all three criterias.
                listToAppend : list = [ Re.sub(r'\s','',optionalData[-1]).lower() ] + [ noteData ]
                return [''] + listToAppend if len(optionalData) == 1 else [ optionalData[0].lstrip().rstrip() ] + listToAppend
        
        else:
            # if there is no title or default values given, print only the note data with empty title and default values.
            return [''] * 2 + [ noteData ]

        
    return [] # if the ringtone fails to meet all of the criteria.
    

class RingtoneTestCase(unittest.TestCase):
    """
    RingtoneTestCase class contains behaviours that test the check_valid_note() and generate_valid_ringtone()
    functions individually, checking if the function behaves as intended when given different types of cases.
    """
    
    def test1_check_valid_note(self: object) -> None:
        """
        Description: Checks the boundary conditions of the substring's note length.
                     It should pass for the values 1,32 and fail for values 0,33
        """
        noteLengthCases : list = [0,1,32,33] # boundary conditions for the function.
        
        
        for lengthCase in noteLengthCases:
            
            # if the length is not within the given criteria range, it should return False.
            if lengthCase == 0 or lengthCase == 33:
                assert check_valid_note( str(lengthCase) + 'a1' ) == False, "The test cases doesn't work for boundary condition lengths 0 or 33."
            
            else: # if it is within the range, return True.
                assert check_valid_note( str(lengthCase) + 'a1' ), "The test cases doesn't work for boundary condition lengths 1 or 32."
    
    def test2_check_valid_note(self: object) -> None:
        # length negative numbers within range [1-32]
        """
        Description: Checks if the function returns False for negative length numbers.
        """
        noteLengthCases : list = [-32,-16,-8,-4,-2,-1]
        
        for lengthCase in noteLengthCases:
            
            # if the length is a negative, it should return False.
            assert check_valid_note( str(lengthCase) + 'a1' ) == False, "The function does not return False for negative numbers!"
        
    def test3_check_valid_note(self: object) -> None:
        """
        Description: Checks whether the note pitch is within the range. Returns true if the character
                     is between [a-g] with optional '#' or a p with no '#'. Returns false if the 
                     condition is not met.
        """
        notePitchCases : list = ['h','h#','i','i#','y','y#','z','z#','p#'] # invalid pitches
        
        for pitchCase in notePitchCases:
            
            # throws AssertionError if the pitchCase evaluates to True.
            assert check_valid_note( pitchCase ) == False, "The function considers outside the range of [a-g] or accepts p with '#'"
    
    def test4_check_valid_note(self: object) -> None:
        """
        Description: Checks if the pitch is not a special character. If it is, the function should return False.  
        """
        # special characters
        notePitchCases : str = ".,:;!?()<>*{}()&^$#@+-_=/%"
        
        
        for pitchCase in notePitchCases:
            # AssertionError is thrown if the special character is allowed to evaluate the function to true.
            assert check_valid_note( pitchCase ) == False, "The function accepts special characters as well!"

    def test5_check_valid_note(self: object) -> None:
        """
        Description: The function should return False if there is a negative number in the note scale.
        """
        # list of negative numbers
        noteScaleCases : list = [-1,-2,-3,-4,-5,-6,-7,-8]
        
        for scaleCase in noteScaleCases:
            # Passes the test case if the negative number evaluates the function to false.
            assert check_valid_note('1a' + str(scaleCase)) == False, "The function also accepts negative number!"
    
    def test6_check_valid_note(self: object) -> None:
        """
        Description: Returns False for false boundary conditions, returns True for boundary conditions
                     within the range [1-8]
        """
        
        # note scale test cases.
        noteScaleCases : list = [0,1,8,9]
        
        for scaleCase in noteScaleCases:
            
            # should return false if the scales are outside the range.
            if scaleCase == 0 or scaleCase == 9:
                assert check_valid_note( '1a' + str(scaleCase) ) == False, "The function accepts boundary conditions 0 or 9, but it should not!"
            
            else: # otherwise it should return true.
                assert check_valid_note('1a' + str(scaleCase) ), "The function does not behave as intended for boundary conditions 1 or 8."
    
    def test1_generate_valid_ringtone(self: object) -> None:
        """
        Description: Checks if the function accepts negative default values and zero. It should return empty list if 
                     negative values or zero are given. 
        """
        
        # test cases
        defaultValuesCases : list = [-1,0,-20,-69, -400]
        
        for valueCase in defaultValuesCases:
                
                # should return empty list if the default values are not non-zero positive integers.
                assert generate_valid_ringtone(f'd={valueCase},o={valueCase},b={valueCase}:4c3') == [], "The function does not check the default values for negative numbers or zero correctly!"

    def test2_generate_valid_ringtone(self: object) -> None:
        """
        Description: Checks if the order of the ringtone string is correct or not. Returns an empty list
                     if the order is incorrect. 
        """
        
        # test cases of different orders.
        ringtoneCases : list = ['d=4,o=5,b=60:Scale:4c5,4d5,4e5,4f5,4g5,4a5,4b5,4c6', '4c5, 4d5,4 e5, 4f 5,4g5, 4a5,  4B5, 4C 6:D= 8 , O  =  4,B =100', ' 32p,8 c, 8 c,    8g,   8G,8 A ,8A,    G: Twinkle Twinkle'] 
        
        for ringtoneCase in ringtoneCases:
            # Gets an AssertionError if the function does not carefully consider the order of the ringtone details entered.
            assert generate_valid_ringtone(ringtoneCase) == [], "The function does not work as intended. The order of the ringtone was not considered carefully!"
    
if __name__ == '__main__':
    unittest.main()
