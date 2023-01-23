from adafruit_hid.keycode import Keycode 
from adafruit_hid.consumer_control_code import ConsumerControlCode

layout = {'title' : 'Danlooo', # Application name
        'macros' : [ #Each row corresponds to respective row and keys on the hardware
                     #Consumer control codes control media commands, Keycodes control nonstring keys.
       
        (0x9e0129, 'Console', [',']), (0x9e0129, 'Clip', ([Keycode.ALT,'1'])), (0x9e0129, 'Mute', ['`']),
        
        (0x9e0129, 'Alt tab', [Keycode.ALT, Keycode.TAB]), (0x9e0129, 'PW', ['Sample']), (0x9e0129, 'UT PW', ['Sample']),
       
        (0x9e0129, 'Vol-', [[ConsumerControlCode.VOLUME_DECREMENT]]),(0x29e0129, 'Vol+', [[ConsumerControlCode.VOLUME_INCREMENT]]),(0x9e0129, 'AB', [Keycode.F3]),
       
        (0x9e0129,  '<<', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),(0x9e0129, 'Play/Pause', [[ConsumerControlCode.PLAY_PAUSE]]),(0x9e0129, '>>', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
        # Digital Encoder
        (0x9e0129, '', [Keycode.BACKSPACE])
    ], 'order' : 1
}
