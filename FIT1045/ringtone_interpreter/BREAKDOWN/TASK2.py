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
