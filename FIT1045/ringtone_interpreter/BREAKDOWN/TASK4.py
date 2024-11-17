import re as Re # import regex pattern recognition.
import unittest # import unittesting library.

### TASK 1 ###
def check_valid_note( substring : str ) -> bool:
    
    """
    
    Description:
    Checks whether a substring meets the given criteria set for being a valid musical note.
    
    Parameters:
    @param substring: The string that will be checked if it is a valid music note.
    
    Returns:
    @return bool: True if the substring is a valid music note or otherwise it's False.
    
    """
    
    # creating a regex pattern that contains all the rules that make a musical note valid.
    notePattern : re.Pattern = Re.compile(r"(^\d{1,2})?([a-g]{1}(#)?|p{1})([1-8]{1})?(\.)?$")
    
    # stores a match object if the substring matches the regex pattern. Otherwise, stores a None.
    substringMatch : re.Match = notePattern.match( substring )
    
    # if there is a match,
    if substringMatch:
        
        # we need to check the note length specifically is correct or not.
        noteLength : str = substringMatch.group(1)
        
        # since note length is optional, we can check if it exists.
        if noteLength:
            
            # if it exists, we need to check if the note length meets the criteria set.
            # the valid lengths are 1,2,4,8,16,32.
            if not int(noteLength) in [1,2,4,8,16,32]:
                return False
        
        # since the other attributes of the substring is checked within the regex pattern, we can just return True.
        return True
    
    # if the match fails,
    return False

### TASK 2 ###
def generate_valid_ringtone( ringtoneDetails : str ) -> list:
    
    """
    
    Description:
    Returns a list of title, default values, and notes data of a valid ringtone. If the ringtone
    is not valid, it returns an empty list.
    
    Parameters:
    @param ringtoneDetails: The details that contain information about a specific ringtone.
    
    Returns:
    @return list: An empty list or list with corresponding ringtone's title, default values and note data.
    
    """
    
    # if there is no string, return empty list.
    if not any ( ringtoneDetails ):
        return []
    
    # splitting the string into three distinctive fields.
    optionalData : tuple
    noteData : str
    
    # creates an packed iterable if default values or default values and title were given. noteData is compulsory.
    *optionalData, noteData = Re.split( ':', ringtoneDetails )
    
    # converting all characters to lowercase in noteData and stripping any whitespace.
    noteData = Re.sub( r'\s', '', noteData ).lower()
    
    ###TECHNIQUE: LIST COMPREHENSION###
    # checking if all of the note data is correct.
    # Split the note data in separate substrings, and checks each substring is valid or not. all() checks if all the data in the list is truthy.
    if all ( [ check_valid_note( substring ) for substring in Re.split( ',' , noteData ) ] ):
        
        # we need to check if the default values pattern is correctly written or not.
        defaultValuesPattern: re.Pattern = Re.compile( r"^(\s*|(d=[1-9]\d*,o=[1-9]\d*,b=[1-9]\d*))$" )
        
        # if there is any optional data written,
        if optionalData:
            
            # stripping off whitespace and converting default values to lower case.
            optionalData[-1] : str = Re.sub( r'\s','',optionalData[-1] ).lower()
            
            # if the default values are written correctly,
            if defaultValuesPattern.match( optionalData[-1] ):
                
                # if the length of the optionalData iterable is 1, only default values and note data were given.
                # otherwise, all of the three fields were given in the ringtone details.
                tempListToAppend : list = [ optionalData[-1], noteData ]
                return [''] + tempListToAppend if len(optionalData) == 1 else [ optionalData[0].lstrip().rstrip() ] + tempListToAppend
        
        # otherwise return empty title and default values, with the note data.
        else:
            return [''] * 2 + [ noteData ]
    
    # if the ringtone details given fail to meet at least one of the criteria, return empty list.
    return []
    
### TASK 4 ###            
def get_ringtone_notes( defaultValues : str, noteData : str ) -> list:
    
    """
    
    Description:
    Returns a list of notes to play with specific note durations and playback note numbers
    from a given default values and note data.
    
    Parameters:
    @param defaultValues: The default values set for the note length, scale and beats.
    
    Returns:
    @return list: Returns a nested list of musical notes from the given parameters.
     
    """
    # similar to task 1, storing the regex pattern for a specific substring.
    notePattern : re.Pattern = Re.compile(r"(^\d{1,2})?([a-g]{1}(#)?|p{1})([1-8]{1})?(\.)?$")
    
    # default values for the music note data.
    d : int = 4; o : int = 5; b : int = 60;
    
    # dictionary to store the note pitch and its corresponding scale value.
    dictionaryOfPitchScales : dict = {
        'C' : 0, 'D' : 2, 'E' : 4,
        'F' : 5, 'G' : 7, 'A' : 9,
        'B' : 11, 'P' : -400
    }
    
    # final list to store the list of playable notes.
    listOfNotes : list = []
    
    ###TECHNIQUE: TUPLE COMPREHENSION###
    # if the default values are given, override the defaults given above.
    # findall() returns a list of numbers found inside the default values string, and puts each number into respective variables.
    if defaultValues:
        d,o,b = ( int(number) for number in Re.findall(r'\b\d+\b', defaultValues) )
        
    
    # iterating through each substring of the note data string.
    for note in Re.split(',', noteData):
        
        hasFullStop : bool = False
        playBackNote : int = 0
        
        noteMatch : re.Match = notePattern.match(note)
        
        # getting the values of the length, scale, pitch, and fullstop.
        noteLength : str = noteMatch.group(1)
        noteScale : str = noteMatch.group(4)
        noteFullStop : str = noteMatch.group(5)
        notePitch : str = noteMatch.group(2)
        
        # overriding variables accordingly.
        noteLength : int = int ( noteLength ) if noteLength else d
        noteScale : int = int( noteScale ) if noteScale else o
        hasFullStop : bool = True if noteFullStop else False
        
        # calculating the noteDuration
        noteDuration : float =  ( ( 4 / noteLength ) * ( 60 / b ) ) 
        noteDuration = noteDuration if not hasFullStop else noteDuration * 1.5
        noteDuration = round( noteDuration, 2 )
        
        # grabbing the note pitch and extracting its letter.
        pitchLetter : chr = notePitch[0]
        playBackNote : int = dictionaryOfPitchScales[ pitchLetter.upper() ]
        
        # if there is a '#' we need to add one to the value.
        if 'p' in pitchLetter:
            pass # if there is a p, return the playBackNote value stored inside the dictionary.
        elif not noteMatch.group(3):
            playBackNote = playBackNote + ( (noteScale - 1) * 12 )
        else:
            playBackNote = playBackNote + 1 + ( (noteScale -1) * 12 )
        
        listOfNotes.append( [ noteDuration, playBackNote ] )
    
    return listOfNotes # returns the list of notes to be played.
        
### TASK 5 ###
def generate_commands( ringtonesLists : list, songTitlesLists : list ) -> tuple:
    
    """
    
    Description:
    The function will return a string of JavaScript commands from the given lists of ringtone
    data and song titles.
    
    Parameters:
    @param ringtonesLists: A list of ringtone details.
    @param songTitlesLists: A list of ringtone titles.
    
    Returns:
    @return tuple: A tuple of JavaScript commands and anchor HTML statements.
    
    """
    
    # variables to store the end results
    validRingtones : str = ""
    titleRingtones : str = ""
    
    # iterating through each nested list of ringtones lists.
    position : int = 0
    for ringtoneList in ringtonesLists:
        
        validRingtones += "function play" + str(position) + "() {\n"
        validRingtones += concatenateJavaScriptCommands(ringtoneList)
        validRingtones += "}"
        
        position += 1
        if position < len(ringtonesLists):
            validRingtones += "\n"
    
    position : int = 0 # Overriding
    for title in songTitlesLists:
        
        # if a title exists,
        finalTitle : str = title if title else "UNTITLED SONG"
        titleRingtones += f"<p><a href='javascript:play{position}();'>PLAY {finalTitle.upper()}</a></p>"
        
        position += 1
        if position < len(songTitlesLists):
            titleRingtones += "\n"
        
    return ( validRingtones, titleRingtones )
        
### TASK 6 ###
def convert_song_file( fileName: str ) -> list:
    
    """
    
    Description:
    The function returns a set of ringotne titles and ringtone notes to play for each title given.
    
    Parameters:
    @param file: The name of the file where the data will be extracted.
    
    Returns:
    @return list: A list of titles list and ringtone notes list.
        
    """
    
    # variables to store the results
    listOfRingtones : list = []
    numberOfLines : int = 0
    
    ###TECHNIQUE: EXCEPTION HANDLING###
    try:
        songFile : _io.TextIOWrapper = open(fileName, 'r')
        currentFile : list = songFile.readlines()
        numberOfLines = len(currentFile)
        
        ###TECHNIQUE: LIST COMPREHENSION###
        listOfRingtones = [ line for line in currentFDile if Re.sub(r'\s','',line) ] # removing empty lines from the file.
        
        songFile.close()
        
    except FileNotFoundError: # in case the file was not found.
        print(f'FILE {fileName} NOT FOUND') 
        
    except IOError: # in case of any errors in working with the file.
        print(f"COULD NOT READ FILE {fileName}")
    
    ###TECHNIQUE: LIST COMPREHENSION###
    # further filtering out the invalid ringtones from the listOfRingtones.
    listOfRingtones = [ generate_valid_ringtone( ringtoneDetail ) for ringtoneDetail in listOfRingtones if any(generate_valid_ringtone(ringtoneDetail)) ]
    
    print(f"Read {numberOfFileLines} lines from \"{fileName}\".\nGenerated {len(listOfRingtones)} valid songs.")
    
    # variables to store the final titles, and ringtone notes.
    titles : list = []
    ringtoneNotes : list = []
    
    for ringtoneDetail in listOfRingtones:
        
        titles.append( ringtoneDetail[0] )
        ringtoneNotes.append( get_ringtone_notes(ringtoneDetail[1], ringtoneDetail[2]) )
    
    with open('play_ringtones.html', 'w') as ringtoneFile:

        ringtoneFile.write("<html>\n<head>\n<script src='WebAudioFontPlayer.js'></script>\n<script src='Soundfile_sf2.js'></script>\n<script>\nvar preset=soundfile_sf2;\nvar AudioContextFunc = window.AudioContext || window.webkitAudioContext;\nvar AC = new AudioContextFunc();\nvar player=new WebAudioFontPlayer();\nplayer.adjustPreset(AC,preset);\n")
        ringtoneFile.write( generate_commands(ringtoneNotes, titles)[0] )
        ringtoneFile.write("\n</script>\n</head>\n<body>\n<h1>\"Mamba Number Py\" Ringtone Interpreter</h1>\n")
        ringtoneFile.write( generate_commands(ringtoneNotes, titles)[1] )
        ringtoneFile.write("\n</body>\n</html>")
        
    return [titles, ringtoneNotes]
    
### HELPER FUNCTIONS ###
###TECHNIQUE: RECURSION###
def concatenateJavaScriptCommands(  ringtoneList : list, index : int = 0, endTime : float = 0.0, stringToReturn : str = "" ) -> str:
    """
    
    Description:
    Recursively appends JavaScript commands into a string variable, and returns the string.
    
    Parameters:
    @param ringtoneList: The list that contains ringtone information.
    @param index: Keeps track of how many notes are there inside the ringtoneList
    @param endTime: The time that each note ends.
    @param stringToReturn: The string that is to be returned
    
    Returns:
    @return str: The string of JavaScript commands.
    
    """
    
    if index >= len( ringtoneList ):
        return stringToReturn # BASE CASE: if the function reaches the end of the list, return the string.
    
    ringtoneDetail = ringtoneList[index]
    stringToReturn += f"var audioBufferSourceNode = player.queueWaveTable(AC, AC.destination, preset, AC.currentTime+{round(endTime, 2)}, {ringtone[1]}, {ringtone[0]});\n"
    
    return concatenateJavaScriptCommands(ringtoneList, position + 1, endTime + ringtone[0], stringToReturn) # RECURSIVE CASE: calling the function with updated parameters.

### TASK 3 ###
class RingtoneTestCase(unittest.TestCase):
    """
    
    RingtoneTestCase class contains behaviours that test the check_valid_note() and generate_valid_ringtone()
    functions individually, checking if the function behaves as intended when given different types of cases.
    
    """
    
    def test1_check_valid_note( self ):
        """
        
        Description: 
        Checks the boundary conditions of the substring's note length.
        It should pass for the values 1,32 and fail for values 0,33
        
        """
        noteLengthCases : list = [0,1,32,33] # boundary conditions for the function.
        
        for lengthCase in noteLengthCases:
            
            # if the length is not within the given criteria range, it should return False.
            if lengthCase == 0 or lengthCase == 33:
                assert check_valid_note( str(lengthCase) + 'a1' ) == False, "The test cases doesn't work for boundary condition lengths 0 or 33."
            
            else: # if it is within the range, return True.
                assert check_valid_note( str(lengthCase) + 'a1' ), "The test cases doesn't work for boundary condition lengths 1 or 32."
    
    def test2_check_valid_note( self ):
        # length negative numbers within range [1-32]
        """
        
        Description: 
        Checks if the function returns False for negative length numbers.
        
        """
        noteLengthCases : list = [-32,-16,-8,-4,-2,-1]
        
        for lengthCase in noteLengthCases:
            
            # if the length is a negative, it should return False.
            assert check_valid_note( str(lengthCase) + 'a1' ) == False, "The function does not return False for negative numbers!"
        
    def test3_check_valid_note( self ):
        """
        
        Description: 
        Checks whether the note pitch is within the range. Returns true if the character
        is between [a-g] with optional '#' or a p with no '#'. Returns false if the 
        condition is not met.
        
        """
        notePitchCases : list = ['h','h#','i','i#','y','y#','z','z#','p#'] # invalid pitches
        
        for pitchCase in notePitchCases:
            
            # throws AssertionError if the pitchCase evaluates to True.
            assert check_valid_note( pitchCase ) == False, "The function considers outside the range of [a-g] or accepts p with '#'"
    
    def test4_check_valid_note( self ):
        """
        
        Description: 
        Checks if the pitch is not a special character. 
        If it is, the function should return False.  
        
        """
        # special characters
        notePitchCases : str = ".,:;!?()<>*{}()&^$#@+-_=/%"
        
        for pitchCase in notePitchCases:
            # AssertionError is thrown if the special character is allowed to evaluate the function to true.
            assert check_valid_note( pitchCase ) == False, "The function accepts special characters as well!"

    def test5_check_valid_note( self ):
        """
        
        Description: 
        The function should return False if there is a negative number in the note scale.
        
        """
        # list of negative numbers
        noteScaleCases : list = [-1,-2,-3,-4,-5,-6,-7,-8]
        
        for scaleCase in noteScaleCases:
            # Passes the test case if the negative number evaluates the function to false.
            assert check_valid_note('1a' + str(scaleCase)) == False, "The function also accepts negative number!"
    
    def test6_check_valid_note( self ):
        """
        
        Description: 
        Returns False for false boundary conditions, returns True for boundary conditions
        within the range [1-8].
        
        """
        
        # note scale test cases.
        noteScaleCases : list = [0,1,8,9]
        
        for scaleCase in noteScaleCases:
            
            # should return false if the scales are outside the range.
            if scaleCase == 0 or scaleCase == 9:
                assert check_valid_note( '1a' + str(scaleCase) ) == False, "The function accepts boundary conditions 0 or 9, but it should not!"
            
            else: # otherwise it should return true.
                assert check_valid_note('1a' + str(scaleCase) ), "The function does not behave as intended for boundary conditions 1 or 8."
    
    def test1_generate_valid_ringtone( self ):
        """
        
        Description: 
        Checks if the function accepts negative default values and zero. It should return empty list if 
        negative values or zero are given. 
        
        """
        
        # test cases
        defaultValuesCases : list = [-1,0,-20,-69, -400]
        
        for valueCase in defaultValuesCases:
                
                # should return empty list if the default values are not non-zero positive integers.
                assert generate_valid_ringtone(f'd={valueCase},o={valueCase},b={valueCase}:4c3') == [], "The function does not check the default values for negative numbers or zero correctly!"

    def test2_generate_valid_ringtone( self ):
        """
        
        Description: 
        Checks if the order of the ringtone string is correct or not. Returns an empty list
        if the order is incorrect. 
        
        """
        
        # test cases of different orders.
        ringtoneCases : list = ['d=4,o=5,b=60:Scale:4c5,4d5,4e5,4f5,4g5,4a5,4b5,4c6', '4c5, 4d5,4 e5, 4f 5,4g5, 4a5,  4B5, 4C 6:D= 8 , O  =  4,B =100', ' 32p,8 c, 8 c,    8g,   8G,8 A ,8A,    G: Twinkle Twinkle'] 
        
        for ringtoneCase in ringtoneCases:
            # Gets an AssertionError if the function does not carefully consider the order of the ringtone details entered.
            assert generate_valid_ringtone(ringtoneCase) == [], "The function does not work as intended. The order of the ringtone was not considered carefully!"


if __name__ == '__main__':
    unittest.main()
