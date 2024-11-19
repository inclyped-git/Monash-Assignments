"""
Name: REDACTED
Last Modified: 11/10/2024
Version No: 3
Description: Seven seg control file
"""

# importing modules.
from pymata4 import pymata4
import time
import math
from seven_segment import sev_segment_init, seven_segment_display_operate, get_refresh_rate

# creating an Arduino instance.
arduinoBoard: pymata4.Pymata4 = pymata4.Pymata4()

thermistorPin = 1 # A1 analog pin
arduinoBoard.set_pin_mode_analog_input(thermistorPin)
powerPin = 3
arduinoBoard.set_pin_mode_digital_output(powerPin)
arduinoBoard.digital_write(powerPin, 1)

# pins that control segments.
serialPinSeg: int = 8
latchPinSeg: int = 9
shiftPinSeg: int = 10

# maintenance pin.
mainPin: int = 7
normalPin: int = 13

def polling_loop() -> int:
    """
    Description: Polls the thermistor for analog voltage.

    Parameters: N/A

    Returns: None
    """

    while True:
        try:
            thermistorAnalogVoltage = arduinoBoard.analog_read(thermistorPin)[0] # The thermistor's analogue voltage value
            if thermistorAnalogVoltage > 0:
                temperature = temp_convert(thermistorAnalogVoltage)
                return temperature
        except KeyboardInterrupt:
            system_menu()

def temp_convert(thermistorAnalogVoltage) -> int:
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
        return int((-21.21*math.log(thermistorResistance)) + 72.203)
    except KeyboardInterrupt:
        system_menu()

def system_menu():
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
                print("You have entered Normal Operation Mode")
                sev_segment_init(arduinoBoard, serialPinSeg, latchPinSeg, shiftPinSeg)
                seven_segment_display_operate(arduinoBoard, serialPinSeg, latchPinSeg, shiftPinSeg, "COM1", 2, refreshRate=1000/3, scrollTime=0.5)
                normal_mode()
            # Data Observation Mode
            elif mode == "2":
                print("You have entered Data Observation Mode")
                sev_segment_init(arduinoBoard, serialPinSeg, latchPinSeg, shiftPinSeg)
                seven_segment_display_operate(arduinoBoard, serialPinSeg, latchPinSeg, shiftPinSeg, "COM2", 2, refreshRate=1000/3, scrollTime=0.5)
            # Maintenance Adjustment Mode
            elif mode == "3":
                print("You have entered Maintenance Adjustment Mode")
                sev_segment_init(arduinoBoard, serialPinSeg, latchPinSeg, shiftPinSeg)
                seven_segment_display_operate(arduinoBoard, serialPinSeg, latchPinSeg, shiftPinSeg, "COM3", 2, refreshRate=1000/3, scrollTime=0.5)
            # User does not provide valid input
            else:
                print("\nPlease provide a valid input.")
        except KeyboardInterrupt:
            arduinoBoard.shutdown()
            time.sleep(1)
            quit()
             # End of code

def normal_mode():
    """
    Description: This function runs the normal operation mode

    Parameters: N/A

    Returns: None
    """
    while True:
        try:
            duration = [15, 5, 3, 15, 5, 3]
            for index in range(len(duration)):
                seven_segment_display_operate(arduinoBoard, serialPinSeg, latchPinSeg, shiftPinSeg, f"stage {index + 1}", duration[index], refreshRate=1000/3, scrollTime=0.5)

            refreshRateOutput = get_refresh_rate()
            seven_segment_display_operate(arduinoBoard, serialPinSeg, latchPinSeg, shiftPinSeg, f"{int(refreshRateOutput)}", 1, refreshRate=1000/3, scrollTime=0.5)

            temperature = polling_loop()
            seven_segment_display_operate(arduinoBoard, serialPinSeg, latchPinSeg, shiftPinSeg, f"{int(temperature)} C", 1, refreshRate=1000/3, scrollTime=0.5)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    system_menu()