"""Two usb joysticks to PPM signal (PPM = Puls-Positions-Modulation) converter with evdev, optimized for the Logitech attack 3"""

# Logitech Attack 3 output layout:
#     AXIS = X,Y,Z
#     BUTTON1 = 288
#     BUTTON2 = 289
#     BUTTON3 = 290
#     BUTTON4 = 291
#     BUTTON5 = 292
#     BUTTON6 = 293
#     BUTTON7 = 294
#     BUTTON8 = 295
#     BUTTON9 = 296
#     BUTTON10 = 297
#     BUTTON11 = 298

from evdev import InputDevice, categorize, ecodes, list_devices
from select import select
import PPM
import pigpio

class JoyStick: # class to create an object for each joystick
    def __init__(self, device):
        self.device = device
          
    def get_axis(self):
        valueX = round((self.device).absinfo(0).value * 3.921568627 + 1000) # input values calculated to PPM values, for each axis: X, Y, Z, min = 1000, center = 1500, max = 2000 uS, 1000/255=3.921568627
        valueY = round((self.device).absinfo(1).value * 3.921568627 + 1000)
        valueZ = round((self.device).absinfo(2).value * 3.921568627 + 1000)
        values_axis_list = [valueX, valueY, valueZ]
        return values_axis_list
    
    def get_buttons(self):
        value_buttons_tuple = (self.device).active_keys(verbose=True) # retrieving which button is being pressed, Logitech Attack 3 returns the values from 288 till 298, (298 - 288 = 11 buttons in total), depending on which button is activated
        button_list = [1000] * 11 # basic list, with 11 items, each item representing one button on the Logitech Attack 3
        if any(item[1] == 288 for item in value_buttons_tuple): # for some reason, the second value in the tuple represents the button status
            button_list[0] = 2000
        if any(item[1] == 289 for item in value_buttons_tuple):
            button_list[1] = 2000
        if any(item[1] == 290 for item in value_buttons_tuple):
            button_list[2] = 2000
        if any(item[1] == 291 for item in value_buttons_tuple):
            button_list[3] = 2000
        if any(item[1] == 292 for item in value_buttons_tuple):
            button_list[4] = 2000
        if any(item[1] == 293 for item in value_buttons_tuple):
            button_list[5] = 2000
        if any(item[1] == 294 for item in value_buttons_tuple):
            button_list[6] = 2000
        if any(item[1] == 295 for item in value_buttons_tuple):
            button_list[7] = 2000
        if any(item[1] == 296 for item in value_buttons_tuple):
            button_list[8] = 2000
        if any(item[1] == 297 for item in value_buttons_tuple):
            button_list[9] = 2000
        if any(item[1] == 298 for item in value_buttons_tuple):
            button_list[10] = 2000
        return button_list # return a list of the status of each momentary button: 1000 uS for not being pressed, 2000 uS for being pressed
    
NUMBER_OF_CHANNELS = 10
GPIO_PIN = 18 # pin number output for the PPM signal on the GPIO Raspberry Pi
pi = pigpio.pi()
if not pi.connected:
    exit(0)
pi.wave_tx_stop() # Start with a clean slate.
ppm = PPM.X(pi, GPIO_PIN, NUMBER_OF_CHANNELS, frame_ms=20) # initiating the PPM wave signal ?

devices_list = [InputDevice(path) for path in list_devices()]

if len(devices_list) == 0: # error message, if no joysticks are detected
    print("No joysticks detected")
    exit(0)

if len(devices_list) == 1:
    js1 = JoyStick(devices_list[0]) # creating one joystick object

if len(devices_list) > 1:
    js1 = JoyStick(devices_list[0]) # creating two joystick objects
    js2 = JoyStick(devices_list[1])

devices_dict = {dev.fd: dev for dev in devices_list} # converted to a dictionary, necessary to read out more than 1 device in the event loop

keys_list = [] 
for key, value in devices_dict.items(): # creates a reference list of the connected joystick, necessary to distinguish the events from each device
    keys_list.append(key)

while True: # event loop for more than one device
    r, w, x = select(devices_dict, [], [])
    for fd in r:
            for event in devices_dict[fd].read(): # event loop for more than one device
                
                if len(devices_list) == 1:
                    output_list = [1500, js1.get_axis()[0], js1.get_axis()[1], js1.get_axis()[2], js1.get_buttons()[0], js1.get_buttons()[1], js1.get_buttons()[2], js1.get_buttons()[3], js1.get_buttons()[4]]
                
                if len(devices_list) > 1:            
                    output_list = [1500, js1.get_axis()[0], js1.get_axis()[1], js2.get_axis()[0], js2.get_axis()[1],js1.get_buttons()[0], js1.get_buttons()[1], js2.get_buttons()[0], js2.get_buttons()[1]] # the PPM module input must be a list, representing one channel for each item, for some reason the first item (channel 0) is not recognized by the Radiomaster and Jumper Radios.
                
                #print(output_list)
                
                ppm.update_channels(output_list) # here is the output put into the PPM signal generator
