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

# CLASS
class Layout:  #Each macro is represented as an 'App', stored in a dictionary with 2 values: Name and Macros
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
apps = []
files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py') and not filename.startswith('._'):
        try:
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            apps.append(App(module.Layout))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            print("ERROR in", filename)
            traceback.print_exception(err, err, err.__traceback__)
if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass
        
        
# DISPLAY


macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

# Set up disp;ay
group = displayio.Group()
for i in range(12): #arrange labels for 12 keys
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF, anchored_position=((macropad.display.width - 1) * (i%3) / 2,macropad.display.height - 1 -(3 - (i//3)) * 12),anchor_point=((i%3) / 2, 1.0)))
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFF000))
group.append(Rect(0,14,macropad.displaywidth, 26, fill = 0xFFF000))
macropad.display.show(group)


# MAIN  Very confusing


last_pos = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0
apps[app_index].switch()

while True:
    # Read encoder position
    pos = macropad.encoder
    if pos != last_pos:
        app_index = pos % len(apps)
        apps[app_index].switch()
        last_pos = pos

    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:
        last_encoder_switch = encoder_switch
        if len(apps[app_index].macros) < 13:
            continue    # No 13th macro, just resume main loop
        key_number = 12 # else process below as 13th macro
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed

    sequence = apps[app_index].macros[key_number][2]
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
    else:
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    macropad.keyboard.release(item)
            elif isinstance(item, dict):
                if 'buttons' in item:
                    if item['buttons'] >= 0:
                        macropad.mouse.release(item['buttons'])
                elif 'tone' in item:
                    macropad.stop_tone()
        macropad.consumer_control.release()
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
            macropad.pixels.show()
