"""
Name: Group A12, Daran Tan, Hamish Richardson, Jacky Yang, Sharvan Saikumar, Tony Liang
Last Modified: 11/10/2024
Version No: 2
Description: Seven seg import file
"""

# importing modules.
from pymata4 import pymata4
import time

lookupDictionary: dict[str, str] = {
    # edgcbfa
     "0":"1101111",
     "1":"1000010",
     "2":"1110101",
     "3":"0111101",
     "4":"0011110",
     "5":"0111011",
     "6":"1111011",
     "7":"0001101",
     "8":"1111111",
     "9":"0011111",
     "a":"1011111",
     "b":"1111010",
     "c":"1100011",
     "d":"1111100",
     "e":"1110011",
     "f":"1010011",
     "g":"0111111",
     "h":"1011010",
     "i":"1000010",
     "j":"0101100",
     "k":"1011110",
     "l":"1100010",
     "m":"1011000",
     "n":"1011000",
     "o":"1111000",
     "p":"1010111",
     "q":"0011111",
     "r":"1010000",
     "s":"0111011",
     "t":"1110010",
     "u":"1101000",
     "v":"1101110",
     "w":"0110110",
     "x":"1011110",
     "y":"0111110",
     "z":"1110101",
     ' ': "0000000"
}

displayBinaries: list[str] = [
    '0111',
    '1011',
    '1101',
    '1110'
]

refreshOutput = 0

def shift_bits_sev_segment(board: pymata4.Pymata4, bits: int, displays: int, registerSerialPin: int, registerLatchPin: int, registerShiftPin: int) -> None:
    """
    Description:
        Shifts bits to the shift register and updates the outputs displayed on the seven segment display.
    Parameter:
        board (pymata4.Pymata4) -> Board instance.
        bits (int) -> Digit bits information.
        displays (int) -> Information of which display to turn on.
        registerSerialPin (int) -> Serial pin of the shift register.
        registerLatchPin (int) -> Rclk pin of the shift register.
        registerShiftPin (int) -> Srclk pin of the shift register.
    Return:
        Void.
    """
    # first identify what displays to use and shift them to the registers.
    for displayIndex in range(4):
        board.digital_pin_write(registerSerialPin, int(displays[abs(displayIndex-3)]))
        board.digital_pin_write(registerShiftPin, 1)
        board.digital_pin_write(registerShiftPin, 0)

    # later shift the appropriate bits to display particular digits.
    for bitIndex in range(7):
        board.digital_pin_write(registerSerialPin, int(bits[abs(bitIndex-6)]))
        board.digital_pin_write(registerShiftPin, 1)
        board.digital_pin_write(registerShiftPin, 0)

    # update output to register.
    board.digital_pin_write(registerLatchPin, 1)
    board.digital_pin_write(registerLatchPin, 0)

def seven_segment_display_operate(board: pymata4.Pymata4, registerSerialPin: int, registerLatchPin: int, registerShiftPin: int, entry: str, duration: float, refreshRate: float = 1000/3, scrollTime: float = 0.5) -> None:
    """
    Description:
        Controls the display operation of the seven segment.
    Parameter:
        board (pymata4.Pymata4) -> Board instance.
        registerSerialPin (int) -> Serial pin of the register.
        registerLatchPin (int) -> Rclk pin of the register.
        registerShiftPin (int) -> Srclk pin of the register.
        entry (str) -> Entry to be displayed.
    Return:
        Void.
    """

    entry = entry.ljust(4) if len(entry) < 4 else entry + " " # creates empty spaces if the digits is less than 4 length.
    """
    Citation: https://www.w3schools.com/python/ref_string_ljust.asp
    .ljust() method returns a string with additional whitespaces to the right of the string identified.
    This will be helpful in scenarios where the string is less than four digits, we can just add whitespaces to make the scrolling session better.

    Examples:
    txt = "banana"
    x = txt.ljust(10)
    >> x = "banana    "

    string = "hello world"
    y = string.ljust(6)
    >> y = "hello world"

    p = 123
    z = p.ljust(4)
    >> z = "123 "
    """

    # bits to be displayed stored in a list.
    codes: list[int] = [lookupDictionary[entry[i].lower()] for i in range(len(entry))]
    
    startTime = time.time()
    try:
        while (time.time() - startTime) < duration:
            # iterate over the list and display the digits.

            currTime = time.time()
            while time.time() - currTime < scrollTime:
                for i in range(4):
                    shift_bits_sev_segment(board, codes[i], displayBinaries[i], registerSerialPin, registerLatchPin, registerShiftPin)
                    time.sleep(1/refreshRate)
                    global refreshOutput
                    refreshOutput = int(refreshRate)
            
            # shift by 1 digit to the left.
            firstElement = codes.pop(0)
            codes.append(firstElement)
    except KeyboardInterrupt:
        quit()

def sev_segment_init(board: pymata4.Pymata4, registerSerialPin: int, registerLatchPin: int, registerShiftPin: int) -> dict[str, int]:
    """
    Description:
        This method sets up the pins for the arduino to shift bits to the 595N shift register.
    Parameter:
        board (pymata4.Pymata4) -> Arduino board instance.
        registerSerialPin -> Shift register SER pin.
        registerLatchPin -> Shift register RCLK pin.
        registerShiftPin -> Shift register SRCLK pin.
    Return:
        (dict[str, int]) -> Look up dictionary for seven segment.
    """

    # storing pins as a iterable to easily iterate and set pin.
    pinsToSetup: list[int] = [registerSerialPin, registerLatchPin, registerShiftPin]

    for pin in pinsToSetup:
        board.set_pin_mode_digital_output(pin)

    # return the look up dictionary for traffic lights.
    return lookupDictionary

def get_refresh_rate():
    global refreshOutput
    return int(refreshOutput)