"""
Name: REDACTED
Last Modified: 11/10/2024
Version No: 10
Description: The main python file controlling all the subsystems and components via one Arduino Uno, under the overall traffic lights system
"""

# Importing modules
from pymata4 import pymata4
import time
import math
from matplotlib import pyplot as plt

# Establishing communication with Arduino
board = pymata4.Pymata4()

# Configuring pins for Approach Ultrasonic Sensor
triggerPin = 17 # A3 analog pin
echoPin = 18 # A4 analog pin

board.set_pin_mode_digital_output(triggerPin)
board.set_pin_mode_digital_input(echoPin)

# Setting up the pin for sonar:
board.set_pin_mode_sonar(triggerPin, echoPin, timeout=200000) # Timeout of 200000 gives max distance of 60 cm

# Configuring pins for the push buttons
firstButtonPin = 19 # A5 analog pin
secondButtonPin = 16 # A2 analog pin

def button_pressed(data: list) -> None:
    """
    Description: Callback function when either push button is pressed.

    Parameters: data - A list of the state of the push button and the time

    Returns: None
    """
    global buttonCount
    global trafficStage
    global shortStage1
    global buttonPressedInStageOne

    # data[2] contains the button state (0 for pressed, 1 for not pressed)
    if data[2] == 0:  # Button pressed (state is LOW)
        buttonCount += 1
        if trafficStage == 1 and buttonPressedInStageOne == False: #If the button is pressed in stage one, 5 seconds left in the cycle
            buttonPressedInStageOne = True
            shortStage1 = True
            print("\nButton pressed in Stage One")
    time.sleep(0.25)

# Configuring analogue pins for the LDR and Thermistor
thermistorPin = 1 # A1 analog pin
ldrPin = 0 # A0 analog pin

board.set_pin_mode_analog_input(thermistorPin)
board.set_pin_mode_analog_input(ldrPin)

def slide_switch(data: list) -> None:
    """
    Description: Callback function when the slide switch is changed

    Parameters: data - A list of the state of the push button and the time

    Returns: None
    """
    if data[2] == 0: # If the slide switch is off, go back to system_menu()
        raise KeyboardInterrupt

# Configuring pins for the Slide Switch
switchPin = 2 # Input pin for the slide switch
powerPin = 3 # To manually output 5V, if slide switch is on

board.set_pin_mode_digital_input(switchPin)
board.set_pin_mode_digital_output(powerPin)

# pins that control traffic lights register.
serialPin: int = 6
latchPin: int = 5
shiftPin: int = 4

# maintenance pin.
mainPin: int = 7
# normal pin
normalPin: int = 13
# both for flashing yellow light

board.set_pin_mode_digital_output(mainPin)
board.set_pin_mode_digital_output(normalPin)

def traffic_light_init(board: pymata4.Pymata4, registerSerialPin: int, registerLatchPin: int, registerShiftPin: int) -> None:
    """
    Description:
        This function sets up the pins for the arduino to shift bits to the 595N shift register to control the traffic lights, and returns the bytes that represent all stages of the operation.
    Parameter:
        board (pymata4.Pymata4) -> Arduino board instance.
        registerSerialPin -> Shift register SER pin.
        registerLatchPin -> Shift register RCLK pin.
        registerShiftPin -> Shift register SRCLK pin.
    Return: None
    """

    # storing pins as a iterable to easily iterate and set pin.
    pinsToSetup: list[int] = [registerSerialPin, registerLatchPin, registerShiftPin]
    for pin in pinsToSetup:
        board.set_pin_mode_digital_output(pin)

traffic_light_init(board, serialPin, latchPin, shiftPin)

# Look up dictionary for 7 seg display
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

trafficLightLookUp: dict[str, int] = {
    # RYG RYG RG 
    "1": 0b00110010,
    "2": 0b01010010,
    "3": 0b10010010,
    "4": 0b10000101,
    "5": 0b10001000,
    "6": 0b10010010
 }

buttonCount = 0
switchState = 1
trafficStage = 0
shortStage1 = False
buttonPressedInStageOne = False
durationLeftInStageTwo = 0
stopLoop = False # To potentially stop normal loop early if button is pressed in stage one
extendStage2 = False # To extend stage 2
stage2Extended = False # Whether or not stage 2 has been extended if button was pressed in stage one
pin = "1234" # Pin to enter Maintenance Adjustment Mode
pinAttemptsCount = 0 # Global variable: counts number of user attempts to get into Maintenance Adjustment Mode
timeOut = 120 # If PIN is incorrect 3 times, timeout for 120 seconds or 2 minutes
isTimeOut = False # Check if timeOut is still occurring, for the case that the user KeyboardInterrupts while in an ongoing timeOut
timePassed = 0 # To continue ongoing timeOut if user tries to enter Maintenance Adjustment Mode but timeout is still ongoing 
speedLimit = 1.5 # kilometres per hour
"""
Physically, I can't move my hand at like 60 km/h, with experimentation, the approximate max speed is 2 km/h.
To test for overspeeding, set speedLimit to ~ 1.5 km/h in Maintenance Adjustment Mode 
"""
yellowLightDistance = 5 # The distance when the yellow main road lights are on, that causes the yellow lights to extend for 3 seconds
sevenSegMessage = "1234" # User can choose a 4 digit alphanumeral to display
pollingTime = 0 # Global variable to use to determine how much time.sleep() left for Stage 5 lights to flash in order to reach 4-7 Hz
totalPollingTime = 0 # Making sure that at a maximum, data is outputted every 1 sec
distanceValues = [] # To filter for output
historyDistValues = [] # All filtered distance values to check for overspeeding over time and any possible accidents
plotDistance = {}
tempValues = [] # To filter for output
ldrValues = [] # To filter for output

def system_menu() -> None:
    """
    Description: This function is essentially the main function or the services subsystem.
    Giving user the choice to enter any of 3 modes.

    Parameters: N/A

    Returns: None
    """
    while True:
        try:
            # Give user option to enter different modes
            mode = input("\nPlease enter the corresponding number to enter:\n1: Normal Operation Mode\n2: Data Observation Mode\n3: Maintenance Adjustment Mode\n")
            # Normal Operation Mode
            if mode == "1":
                normal_mode()
            # Data Observation Mode
            elif mode == "2":
                data_observation_mode()
            # Maintenance Adjustment Mode
            elif mode == "3":
                maintenance_mode()
            # User does not provide valid input
            else:
                print("\nPlease provide a valid input.")
        except KeyboardInterrupt or EOFError:
            board.shutdown()
            time.sleep(1)
            quit()
             # End of code

def normal_mode() -> None:
    """
    Description: This function runs the normal operation mode

    Parameters: N/A

    Returns: None
    """
    global stopLoop

    global serialPin, latchPin, shiftPin, normalPin, mainPin
    shift_bits_traffic_lights(0b0000000, serialPin, latchPin, shiftPin, board) # Reset all lights
    turn_off_maintenance_mode(board, normalPin)
    turn_on_normal_mode(board, mainPin)  

    print("\nYou have entered Normal Operation Mode")
    time.sleep(0.25)

    while True:
        try:
            def slide_switch(data) -> None:
                """"
                Description: Callback function in normal mode loop if slide switch is ever changed

                Parameters: data - list of the time and state of the switch

                Returns: None
                """
                global stopLoop
                time.sleep(0.25)
                if data[2] == 0: # If the slide switch is off, stop the normal operation mode
                    stopLoop = True

            board.set_pin_mode_digital_input(switchPin, callback=slide_switch)
            board.set_pin_mode_digital_output(powerPin)
            if stopLoop == True:
                raise KeyboardInterrupt
            
            onOrOff = board.digital_read(switchPin)[0]

            board.digital_write(powerPin, onOrOff)
            if onOrOff == 0:
                print("No Power Available. Turn the slide switch on.")
                raise KeyboardInterrupt

            time.sleep(1)
            stage_one()
            stage_two()
            stage_three()
            stage_four()
            stage_five()
            stage_six()
        except KeyboardInterrupt:
            stopLoop = False
            time.sleep(0.25)
            system_menu() # CTRL-C goes back to services subsystem/main menu

def data_observation_mode() -> None:
    """
    Description: This function runs the data observation mode.

    Parameters: N/A

    Returns: None
    """
    global plotDistance, serialPin, latchPin, shiftPin, normalPin, mainPin

    shift_bits_traffic_lights(0b0000000, serialPin, latchPin, shiftPin, board)
    turn_off_normal_mode(board, normalPin)
    turn_on_maintenance_mode(board, mainPin)
    shift_bits_traffic_lights(0b01001000, serialPin, latchPin, shiftPin, board)

    print("\nYou have entered Data Observation Mode")
    try:
        timeValues = list(plotDistance.keys())
        timePlot = []
        distance = []

        totalTime = 0
        index = -1
        while totalTime <= 20:
            try:
                totalTime += timeValues[index]
                timePlot.append(totalTime)
                distance.append(plotDistance[timeValues[index]])
                index -= 1
            except IndexError:
                timePlot = []
                distance = []
                print("Not enough data to plot the last 20 seconds.")
                break
        if len(timePlot) > 0:
            # plot the data with title, legend, axes labels.
            plt.plot(timePlot[::-1], distance)
            plt.title("Traffic distance for the last 20 seconds")
            plt.xlabel("Time (s)")
            plt.ylabel("Distance (cm)")
            plt.legend(["Traffic distance over time"])
            plt.savefig("trafficDistance.png")
            plt.show()
            board.shutdown()
            time.sleep(0.25)
            quit()
    except KeyboardInterrupt:
        board.shutdown()
        time.sleep(0.25)
        quit()

def maintenance_mode() -> None:
    """
    Description: This function runs the maintenance adjustment mode, asking user for a pin to enter and change system parameters

    Parameters: N/A

    Returns: None
    """
    global serialPin, latchPin, shiftPin, normalPin, mainPin

    shift_bits_traffic_lights(0b00000000, serialPin, latchPin, shiftPin, board)
    turn_off_normal_mode(board, normalPin)
    turn_on_maintenance_mode(board, mainPin)
    shift_bits_traffic_lights(0b01001000, serialPin, latchPin, shiftPin, board) # Turn on the flashing yellow lights

    # User must enter correct PIN to continue to Maintenance Adjustment Mode
    while True:
        global pinAttemptsCount
        global isTimeOut
        global timePassed # To continue ongoing timeOut if user tries to enter Maintenance Adjustment Mode but timeout is still ongoing 
        
        try:
            pinUserAttempt = input("\nPlease enter PIN: ")
            if pinUserAttempt == pin and isTimeOut == False: # In the case that they get it correct and there's no timeout occuring
                break
            elif isTimeOut == True: # Doesn't matter whether pin is correct, if timeout is still ongoing, not allowed in
                for timePassed in range(timePassed,timeOut): # Start timeout again from last amount of time passed, up to 120 seconds overall
                    print(f"{timeOut - timePassed} seconds left")
                    time.sleep(1)
                isTimeOut = False # Allows for user to enter if they get pin correct next time

                pinAttemptsCount = 0 # Reset number of attempts allowed
            else:
                print("\nPIN is incorrect.")
                pinAttemptsCount += 1
                pinAttemptsLeft = 3 - pinAttemptsCount
                print(f"\n{pinAttemptsLeft} attempts remaining.")
        
                # Users have 3 attempts to provide the correct PIN. If number of user attempts exceed number of attempts user will be notified. 
                if pinAttemptsCount == 3:
                    print("\nToo many incorrect attempts. User is timed out from 2 minutes.")
                    isTimeOut = True # Restricts user from entering for 120 seconds
                    # User is timed out for 2 minutes. Time remaining is displayed every second in seconds. 
                    for timePassed in range(1,timeOut):
                        print(f"{timeOut - timePassed} seconds left")
                        time.sleep(1)
                    isTimeOut = False
                    
                    # Reset number of user attempts. 
                    pinAttemptsCount = 0
        except KeyboardInterrupt:
            system_menu()

    print("\nYou have entered Maintenance Adjustment Mode")
    # Displays the current global/system parameters once user has provided correct PIN.

    while True:
        try:
            global speedLimit
            global yellowLightDistance
            global sevenSegMessage

            adminStartTime = time.time()
            changeParameter = input(f"\nPlease enter the corresponding number to change a parameter:\n1. Speed limit: {speedLimit} km/h\n2. Distance to extend yellow lights for 3 seconds: {yellowLightDistance} cm\n3. 7 Segment Message: {sevenSegMessage}\n")
            if time.time() - adminStartTime >= 20:
                print("\nYou took too long. Admin access is only allowed for 20 seconds.")
                break
            if changeParameter == "1":
                adminStartTime = time.time()
                newSpeedLimit = float(input("\nInput new speed limit (km/h): "))
                if time.time() - adminStartTime >= 20:
                    print("\nYou took too long. Admin access is only allowed for 20 seconds.")
                    break
                if 0 <= newSpeedLimit <= 1.5: # The max velocity that the Ultrasonic can sense
                    speedLimit = newSpeedLimit
                else:
                    print("\nSpeed Limit is not within allowable 0 to 1.5 km/h range. Try Again.")
            if changeParameter == "2":
                adminStartTime = time.time()
                newYellowLightDistance = float(input("\nInput new Yellow Light Distance (cm): "))
                if time.time() - adminStartTime >= 20:
                    print("\nYou took too long. Admin access is only allowed for 20 seconds.")
                    break
                if 0 <= newYellowLightDistance <= 60: # The max distance is 60 cm, that the Ultrasonic sensor can sense
                    yellowLightDistance = newYellowLightDistance
                else:
                    print("\nYellow Light Distance is not within allowable 0 to 60 cm range. Try Again.")
            if changeParameter == "3":
                adminStartTime = time.time()
                newSevenSegMessage = input("\nInput a new message to display: ")
                if time.time() - adminStartTime >= 20:
                    print("\nYou took too long. Admin access is only allowed for 20 seconds.")
                    break
                try: # Verify seven seg message
                    if 1 <= len(newSevenSegMessage): # Length of message has to be 1 or more characters
                        digitIndex = 0
                        while digitIndex < len(newSevenSegMessage):
                            digit = newSevenSegMessage[digitIndex]
                            if digit not in lookupDictionary: # Checking if the message is even possible according to the lookupDictionary
                                print("\nMessage includes invalid characters.")
                                break
                            else:
                                digitIndex += 1
                        if digitIndex == len(newSevenSegMessage):
                            sevenSegMessage = newSevenSegMessage # If all chars passed, change system parameter
                    else:
                        print("\nEmpty message was given (has to have at least one character). Try Again.")
                except ValueError:
                    print("Message is invalid. Try Again.")
            else:
                print("\nPlease choose a parameter to change.")
        except ValueError: # For invalid inputs for system parameters 1 and 2
            print("\nPlease enter a number")
        except KeyboardInterrupt:
            system_menu()

def polling_loop() -> None:
    """
    Description: Polls the LDR, thermistor for analog voltage, Ultrasonic sensor for distance and push buttons for high or low state,
    every 0.07 seconds. It takes all these values up to 1 second (the polling rate).

    Parameters: N/A

    Returns: None
    """
    while True:
        try:
            global startTime, distanceValues, tempValues, ldrValues

            startTime = time.time() # Start time in seconds

            distance = board.sonar_read(triggerPin) # Ultrasonic Sensor distance data in centimetres
            distanceValues.append(distance[0]) # sonar_road returns tuple (distance, time)
        
            thermistorAnalogVoltage = board.analog_read(thermistorPin)[0] # The thermistor's analogue voltage value
            if thermistorAnalogVoltage > 0:
                tempValues.append(thermistorAnalogVoltage)
            
            ldrVoltage = board.analog_read(ldrPin) # The LDR's analogue voltage value
            ldrValues.append(ldrVoltage[0]) # analog_read returns tuple (analog voltage, time)

            time.sleep(0.07) # Refer to comment below
            """
            The reason for this is because the Ultrasonic Sensor's readings are lagging behind signficantly,
            due to the overload in measurements it needs to make, without sleeping for 0.1 secs.

            The time to sleep was determined to be optimal through experimentation.
            - 0.5 seconds would incur a different type of delay due to the extended amount of time passed from the last measurement
            - 0.05 would incur a similar delay due to the frequency of measurements, but the median filtering later on smooths the data
            """

            endTime = time.time() # End time in seconds
            
            global pollingTime
            global totalPollingTime

            pollingTime = endTime - startTime
            totalPollingTime += pollingTime
            break
        except KeyboardInterrupt:
            system_menu()

def polling_console() -> None:
    """
    Description: Outputs filtered data calculated from the polling loop and takes into account any overspeeding and possible accidents

    Parameters: N/A

    Returns None
    """
    global totalPollingTime, pollingTime, distanceValues, tempValues, ldrValues, trafficStage, yellowLightDistance, extendStage2, stage2Extended, plotDistance
    try:
        if len(tempValues) > 13: # If the polling has reached the polling rate of at least one second, starting filtering values
            filteredDistance = filter_values(distanceValues)
            filteredTemp = temp_convert(filter_values(tempValues))
            tempFeeling = temp_state(filteredTemp) # 'Hot' 'Warm' 'Normal' or 'Cold' states
            filteredLDR = filter_values(ldrValues)
            [ldrVoltage, nightOrDay] = ldr_info(filteredLDR)
            plotDistance[totalPollingTime] = filteredDistance # To plot later on
        
            print(f"\nStage: {trafficStage}\nPolling Rate: {totalPollingTime:.2f} s\nDistance: {filteredDistance:.2f} cm\nTemperature: {filteredTemp:.2f} degrees Celcius\nTemperature State: {tempFeeling}\nLDR Analog Voltage: {filteredLDR:.2f}\nLDR Voltage: {ldrVoltage:.2f} V\nDay or night time: {nightOrDay}")
            if trafficStage == 2 and stage2Extended == False and filteredDistance <= yellowLightDistance: # Yellow main road lights
                extendStage2 = True
            speeding(filteredDistance, totalPollingTime) # Check for overspeeding
            accident() # Check for possible accidents

            # Reset polling data storage once polling cycle has ended
            pollingTime = 0
            totalPollingTime = 0
            distanceValues = []
            tempValues = []
            ldrValues = []
    except KeyboardInterrupt:
        extendStage2 = False
        system_menu()

def temp_convert(thermistorAnalogVoltage) -> float:
    """
    Description: This function converts the thermistor's analog voltage to voltage and
    utilises the voltage divider formula rearranged to calculate the resistance of the thermistor
    to then calculate the temperature in degrees Celcius.

    Parameters: 
        thermistorAnalogVoltage - voltage measured by thermistor.

    Returns:
        float - Celsius value.
    """
    
    try:
        thermistorVoltage = int(thermistorAnalogVoltage) * (5 / 1023)
        thermistorResistance = ((thermistorVoltage * 10000) / (5 - thermistorVoltage))/1000 # In kilo-ohms
        return (-21.21*math.log(thermistorResistance)) + 72.203
    except KeyboardInterrupt:
        system_menu()

def speeding(filteredDistance, movingTime) -> None:
    """
    Description: Uses all the filtered distance data to calculate the speed in km/h and determines whether the 'car' is overspeeding.

    Parameters: 
        filteredDistance - filtered distance
        movingTime - time taken for the car while moving
    
    Returns:
        None
    """
    try:
        historyDistValues.append(filteredDistance)
        if len(historyDistValues) >= 2:
            # Convert the distance values from cm to km, time from seconds to hrs, calculate speed in km/h
            speed = abs((historyDistValues[-1]/100000) - (historyDistValues[-2]/100000))/(movingTime/3600)
            """
            speed (km/h) = (end distance in km - start distance in km)/(time in hrs)
            """
            if speed > speedLimit:
                print(f"Car is overspeeding. The speed limit is {speedLimit} km/h, the car is travelling at {speed} km/h.")
    except KeyboardInterrupt:
        system_menu()

def accident() -> None:
    """
    Description: Outputs a message indicating a possible accident if the last 5 filtered distance values are the same.

    Parameters: N/A

    Returns: None
    """
    # If the distance hasn't changed for approximately 15 seconds, indicate a possible accident
    global trafficStage
    try:
        if len(historyDistValues) >= 15:
            # If the last 5 distance values are the same
            checkDistValues = historyDistValues[-15:] # Last 5 distance values
            accidentDistValue = checkDistValues[-1] # The value to check to be constant
            notMovingCount = checkDistValues.count(accidentDistValue) # Counting number of matching values
            if notMovingCount == 15:
                print("There may have been a collision, accident or breakdown.")
        if len(historyDistValues) >= 3 and trafficStage == 1:
            # This is for the console alert that shows when the vehicle hasn't moved during Green Main Traffic Light (Stage 1) for more than 3 seconds
            checkDistValues = historyDistValues[-3:] # Last 5 distance values
            accidentDistValue = checkDistValues[-1] # The value to check to be constant
            notMovingCount = checkDistValues.count(accidentDistValue) # Counting number of matching values
            if notMovingCount == 3:
                print("The car hasn't moved for over 3 seconds while the main road light is Green.")
    except KeyboardInterrupt:
        system_menu()

def filter_values(values) -> float:
    """
    Description: This function filters all polled data using an averaging method

    Parameters: values - The inputted list to filter for one averaged value

    Returns: float - The average of the values parameter list
    """

    # Previously used median method
    """
    ascendingOrder = sorted(values)
    if len(values) % 2 == 0: # Median formula for even number of values
        median = (ascendingOrder[int(len(values)/2)] + ascendingOrder[int((len(values)/2) + 1)])/2
    else: # Median formula for odd number of values
        median = ascendingOrder[int((len(values) + 1)/2)]
    return median
    """

    try:
        total = 0
        for value in values:
            total += value
        
        return total/len(values)
    except KeyboardInterrupt:
        system_menu()

def temp_state(filteredTemp):
    """
    Description: This function determines whether the temperature is considered to be 'Hot', 'Warm', 'Normal', 'Cold'.

    Parameters: filteredTemp - The average filtered temperature to determine the state of feeling

    Returns: tempFeeling - The feeling in terms of hot, warm, normal and cold
    """
    try:
        if filteredTemp >= 35:
            tempFeeling = "Hot"
        elif filteredTemp >= 25:
            tempFeeling = "Warm"
        elif filteredTemp > 20:
            tempFeeling = "Normal" # Between 20 and 25
        else:
            tempFeeling = "Cold"

        return tempFeeling
    except KeyboardInterrupt:
        system_menu()

def ldr_info(ldrAnalogVoltage) -> list:
    voltage = ldrAnalogVoltage * (5 / 1023)

    nightOrDay = None
    if voltage <= 2.5: # Day-night exchange
        nightOrDay = "Day-time"
    else:
        nightOrDay = "Night-time"

    return [voltage, nightOrDay]

def shift_bits_traffic_lights(bits: int, registerSerialPin: int, registerLatchPin: int, registerShiftPin: int, board: pymata4.Pymata4) -> None:
    """
    Description:
        Shifts bit by bit from a byte representing the state of the traffic light stages to the shift register.
    Parameter:
        bits (int) -> Byte representing the state of each light.
        registerSerialPin (int) -> Serial pin of the shift register.
        registerLatchPin (int) -> RCLK pin of the shift register.
        registerShiftPin (int) -> SRCLK pin of the shift register.
        board (pymata4.Pymata4) -> Arduino instance.
    Return: 
        Void.
    """
    # turn off the latch pin.
    board.digital_pin_write(registerLatchPin, 0)

    # have to loop backwards since registers behave as stacks.
    for index in range(8):

        # retrieve bit to display and add it to serial.
        bitToDisplay: int = (bits >> index) & 1
        board.digital_pin_write(registerSerialPin, bitToDisplay)

        # shift the bits.
        board.digital_pin_write(registerShiftPin, 0)
        board.digital_pin_write(registerShiftPin, 1)

    # turn on the latch pin to push the resultant byte.
    board.digital_pin_write(registerLatchPin, 1)

def turn_on_maintenance_mode(board: pymata4.Pymata4, maintainancePin: int) -> None:
    """
    Description: Write maintenance Pin on

    Parameters: board - arduino, maintenancePin - the pin to turn on the flashing yellow lights

    Returns: None
    """
    board.digital_pin_write(maintainancePin, 1)

def turn_off_maintenance_mode(board: pymata4.Pymata4, maintainancePin: int) -> None:
    """
    Description: Write maintenance Pin off

    Parameters: board - arduino, maintenancePin - the pin to turn on the flashing yellow lights

    Returns: None
    """
    board.digital_pin_write(maintainancePin, 0)

def turn_on_normal_mode(board: pymata4.Pymata4, normalPin: int) -> None:
    """
    Description: Write normal mode Pin on

    Parameters: board - arduino, maintenancePin - the pin to turn on the cyclical lights

    Returns: None
    """
    board.digital_pin_write(normalPin, 1)

def turn_off_normal_mode(board: pymata4.Pymata4, normalPin: int) -> None:
    """
    Description: Write normal mode Pin off

    Parameters: board - arduino, maintenancePin - the pin to turn on the cyclical lights

    Returns: None
    """
    board.digital_pin_write(normalPin, 0)

# defining different stages in the traffic operation.
def stage_one() -> None:
    """
    __description__: Controls the stage one process of the traffic operation.

    __returns__: void.

    """
    try:
        global trafficStage
        global buttonPressedInStageOne
        global shortStage1
        global stopLoop
        global durationLeftInStageTwo
        trafficStage = 1

        def slide_switch(data):
            """"
                Description: Callback function in normal mode loop if slide switch is ever changed

                Parameters: data - list of the time and state of the switch

                Returns: None
            """
            time.sleep(0.25)
            global stopLoop
            if data[2] == 0:
                stopLoop = True

        board.set_pin_mode_digital_input(switchPin, callback=slide_switch)
        board.set_pin_mode_digital_output(powerPin)

        # Configuring buttons to register being pressed in Stage One
        board.set_pin_mode_digital_input_pullup(firstButtonPin, callback=button_pressed)
        board.set_pin_mode_digital_input_pullup(secondButtonPin, callback=button_pressed)

        currentTime: time = time.time()
        duration: int = 15
        
        while time.time() - currentTime < duration: # For 15 seconds
            if stopLoop == True:
                raise KeyboardInterrupt
            if shortStage1 == True:
                durationLeft = duration - (time.time() - currentTime)
                if durationLeft >= 5:
                    duration = 5
                    currentTime = time.time()
                else:
                    durationLeftInStageTwo = 5 - durationLeft
                shortStage1 = False
            shift_bits_traffic_lights(trafficLightLookUp["1"], 6, 5, 4, board)
            polling_loop()
            polling_console()
    except KeyboardInterrupt:
        buttonPressedInStageOne = False
        shortStage1 = False
        stopLoop = False
        time.sleep(0.25)
        system_menu()

def stage_two() -> None:
    """
    __decription__: Controls the stage two process of the traffic operation.

    __returns__: void.
    
    """

    try:
        global trafficStage
        global buttonPressedInStageOne
        global durationLeftInStageTwo
        global stopLoop
        global extendStage2
        global stage2Extended
        trafficStage = 2

        def slide_switch(data):
            """"
                Description: Callback function in normal mode loop if slide switch is ever changed

                Parameters: data - list of the time and state of the switch

                Returns: None
            """
            time.sleep(0.25)
            global stopLoop
            if data[2] == 0:
                stopLoop = True

        board.set_pin_mode_digital_input(switchPin, callback=slide_switch)
        board.set_pin_mode_digital_output(powerPin)

        # Configuring buttons to register being pressed in Stage Two
        board.set_pin_mode_digital_input_pullup(firstButtonPin, callback=button_pressed)
        board.set_pin_mode_digital_input_pullup(secondButtonPin, callback=button_pressed)

        currentTime: time = time.time()
        duration: int = 5
        if buttonPressedInStageOne == True:
            duration = durationLeftInStageTwo

        while time.time() - currentTime < duration:
            if stopLoop == True:
                raise KeyboardInterrupt
            if extendStage2 == True and buttonPressedInStageOne == False: # Given that the button was not pressed in Stage One, meaning the cycle doesn't end after 5 more seconds.
                duration += 3 # Add 3 seconds to the Yellow Main Road Lights Stage when the distance measured is in the range to extend Stage 2 by 3 more seconds
                print(f"\n3 seconds added to Stage 2. Time left in Stage 2: {duration - (time.time() - currentTime):.2f}s")
                extendStage2 = False
                stage2Extended = True
            shift_bits_traffic_lights(trafficLightLookUp["2"], 6, 5, 4, board)
            polling_loop()
            polling_console()
        stage2Extended = False
    except KeyboardInterrupt:
        buttonPressedInStageOne = False
        stopLoop = False
        extendStage2 = False
        stage2Extended = False
        time.sleep(0.25)
        system_menu()

def stage_three() -> None:
    """
    __description__: Controls the stage three of the traffic operation.

    __returns__: void.
    """
    try:
        global trafficStage
        global buttonPressedInStageOne
        global stopLoop
        trafficStage = 3

        def slide_switch(data):
            """"
                Description: Callback function in normal mode loop if slide switch is ever changed

                Parameters: data - list of the time and state of the switch

                Returns: None
            """
            time.sleep(0.25)
            global stopLoop
            if data[2] == 0:
                stopLoop = True

        board.set_pin_mode_digital_input(switchPin, callback=slide_switch)
        board.set_pin_mode_digital_output(powerPin)

        # Configuring buttons to register being pressed in Stage Three
        board.set_pin_mode_digital_input_pullup(firstButtonPin, callback=button_pressed)
        board.set_pin_mode_digital_input_pullup(secondButtonPin, callback=button_pressed)

        duration: int = 3
        currentTime = time.time()
        
        while time.time() - currentTime < duration:
            if stopLoop == True:
                raise KeyboardInterrupt

            if buttonPressedInStageOne == True:
                break
            else:
                shift_bits_traffic_lights(trafficLightLookUp["3"], 6, 5, 4, board)
                polling_loop()
                polling_console()
    except KeyboardInterrupt:
        buttonPressedInStageOne = False
        stopLoop = False
        time.sleep(0.25)
        system_menu()

def stage_four() -> None:
    """
    __description__: Controls the fourth stage of the traffic operation.

    __returns__: void.
    
    """
    try:
        global buttonCount
        global buttonPressedInStageOne
        global trafficStage
        global stopLoop
        trafficStage = 4

        def slide_switch(data):
            """"
                Description: Callback function in normal mode loop if slide switch is ever changed

                Parameters: data - list of the time and state of the switch

                Returns: None
            """
            time.sleep(0.25)
            global stopLoop
            if data[2] == 0:
                stopLoop = True

        board.set_pin_mode_digital_input(switchPin, callback=slide_switch)
        board.set_pin_mode_digital_output(powerPin)

        # Print number of presses registered to the console
        print(f"\nNumber of presses registered: {buttonCount}")
        # Reset button count in Stage 4
        buttonCount = 0

        duration: int = 15
        currentTime: time = time.time()

        while time.time() - currentTime < duration:
            if stopLoop == True:
                raise KeyboardInterrupt

            if buttonPressedInStageOne == True:
                break
            else:
                shift_bits_traffic_lights(trafficLightLookUp["4"], 6, 5, 4, board)
                polling_loop()
                polling_console()
    except KeyboardInterrupt:
        buttonPressedInStageOne = False
        stopLoop = False
        time.sleep(0.25)
        system_menu()

def stage_five() -> None:
    """
    __description__: Controls the fifth stage of the traffic operation.

    __returns__: void.

    """
    try:
        global trafficStage
        global buttonPressedInStageOne
        global stopLoop
        trafficStage = 5

        def slide_switch(data):
            """"
                Description: Callback function in normal mode loop if slide switch is ever changed

                Parameters: data - list of the time and state of the switch

                Returns: None
            """
            time.sleep(0.25)
            global stopLoop
            if data[2] == 0:
                stopLoop = True

        board.set_pin_mode_digital_input(switchPin, callback=slide_switch)
        board.set_pin_mode_digital_output(powerPin)

        # Configuring buttons to register being pressed in Stage Five
        board.set_pin_mode_digital_input_pullup(firstButtonPin, callback=button_pressed)
        board.set_pin_mode_digital_input_pullup(secondButtonPin, callback=button_pressed)

        currentTime: time = time.time()
        duration: int = 5

        while time.time() - currentTime < duration:
            if stopLoop == True:
                raise KeyboardInterrupt

            if buttonPressedInStageOne == True:
                break
            else:
                shift_bits_traffic_lights(trafficLightLookUp["5"], 6, 5, 4, board)
                polling_loop()
                polling_console()
    except KeyboardInterrupt:
        buttonPressedInStageOne = False
        stopLoop = False
        time.sleep(0.25)
        system_menu()

def stage_six() -> None:
    """
    __description__: Describes the sixth stage of the traffic operation.

    __returns__: void.
    
    """
    try:
        global trafficStage
        global buttonPressedInStageOne
        global stopLoop
        trafficStage = 6

        def slide_switch(data):
            """"
                Description: Callback function in normal mode loop if slide switch is ever changed

                Parameters: data - list of the time and state of the switch

                Returns: None
            """
            time.sleep(0.25)
            global stopLoop
            if data[2] == 0:
                stopLoop = True

        board.set_pin_mode_digital_input(switchPin, callback=slide_switch)
        board.set_pin_mode_digital_output(powerPin)

        # Configuring buttons to register being pressed in Stage Six
        board.set_pin_mode_digital_input_pullup(firstButtonPin, callback=button_pressed)
        board.set_pin_mode_digital_input_pullup(secondButtonPin, callback=button_pressed)

        duration: int = 3
        currentTime: time = time.time()

        while time.time() - currentTime < duration:
            if stopLoop == True:
                raise KeyboardInterrupt

            if buttonPressedInStageOne == True:
                break
            else:
                shift_bits_traffic_lights(trafficLightLookUp["6"], 6, 5, 4, board)
                polling_loop()
                polling_console()
        buttonPressedInStageOne = False
    except KeyboardInterrupt:
        buttonPressedInStageOne = False
        stopLoop = False
        time.sleep(0.25)
        system_menu()

if __name__ == '__main__':
    system_menu()