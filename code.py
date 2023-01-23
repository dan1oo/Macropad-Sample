#Libraries(found in lib)
import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad
import traceback
MACRO_FOLDER = '/macros'
macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

# CLASS
class Layout:  #Each macro is represented as an 'App', stored in a dictionary with 3 values: Name, Macro, and Order
    def __init__(self, macro):  
        self.title = macro['title']
        self.macros = macro['macros']
        self.order = macro['order']
    def active(self):
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()
        macropad.pixels.show()
        macropad.display.refresh()
    def switch(self):
        #Activate application settings
        group[13].text = self.title   # Application name
        for i in range(12):
            if i < len(self.macros): # Key in use, set label + LED color
                macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                macropad.pixels[i] = 0
                group[i].text = ''

# Load all the macros from .py files in FOLDER
macros = []
files = os.listdir(MACRO_FOLDER)
files.sort()
for i in files:
    if i.endswith('.py') and not i.startswith('._'): #Make sure it is a valid .py file
        try:
            module = __import__(MACRO_FOLDER + '/' + i[:-3])
            macros.append(Layout(module.Layout))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            print("ERROR in", filename)
else:
    pass

# DISPLAY
# Set up display as Group() - append group with each display element - 12 label keys and 13 rectangles, similar to regular python display library
group = displayio.Group()
for i in range(12): #arrange labels for 12 keys
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF, anchored_position=((macropad.display.width - 1) * (i%3) / 2,macropad.display.height - 1 -(3 - (i//3)) * 12),anchor_point=((i%3) / 2, 1.0)))
    group.append(Rect((macropad.display.width - 1) * (i%3) / 2,macropad.display.height - 1 -(3 - (i//3)) * 12),anchor_point=((i%3) / 2, 1.0)), fill=0xFFFFFF))
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFF000))
macropad.display.show(group)


# MAIN  Much of this section was taken from common repos as a main loop for determining when buttons are pressed.


last_pos = macros[app_index].order
app_index = 0
macros[app_index].switch()

while True:
    # Read encoder position and determine whether to switch layouts
    pos = macropad.encoder
    if pos != last_pos:
        app_index = pos % len(macros)
        macros[app_index].switch()
        last_pos = pos

    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:
        last_encoder_switch = encoder_switch
        if len(macros[app_index].macros) < 13:
            continue    # No 13th macro, just resume main loop
        key_number = 12 # else process below as 13th macro
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(macros[app_index].macros):
            continue # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed
    #Continue if key has been pressed
    sequence = macros[app_index].macros[key_number][2]
    if pressed:           # If keys are pressed
        
        if key_number < 12:             #Main keys(non encoder)
            macropad.pixels[key_number] = 0xFFFFFF
            macropad.pixels.show()
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    macropad.keyboard.press(item)
                else:
                    macropad.keyboard.release(-item)
            elif isinstance(item, float):
                time.sleep(item)
            elif isinstance(item, str):
                macropad.keyboard_layout.write(item)
            elif isinstance(item, list):
                for code in item:
                    if isinstance(code, int):
                        macropad.consumer_control.release()
                        macropad.consumer_control.press(code)
                    if isinstance(code, float):
                        time.sleep(code)
            elif isinstance(item, dict):
                if 'buttons' in item:
                    if item['buttons'] >= 0:
                        macropad.mouse.press(item['buttons'])
                    else:
                        macropad.mouse.release(-item['buttons'])
    else: #release keys
        macropad.release_all()
