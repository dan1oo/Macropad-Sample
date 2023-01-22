from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
from adafruit_hid.consumer_control_code import ConsumerControlCode

app = {'title' : 'Danlooo', # Application name
    'macros' : [
        (0x9e0129, 'Console', [',']),
        (0x9e0129, 'Clip', ([Keycode.ALT,'1'])),
        (0x9e0129, 'Mute', ['`']),
        # 2nd row ----------
        (0x9e0129, 'Alt tab', [Keycode.ALT, Keycode.TAB]),
        (0x9e0129, 'PW', ['Look/aturphonebruh7']),
        (0x9e0129, 'UT PW', ['Look.aturphonebruh7']),
        # 3rd row ----------
        (0x9e0129, 'Vol-', [[ConsumerControlCode.VOLUME_DECREMENT]]),
        (0x29e0129, 'Vol+', [[ConsumerControlCode.VOLUME_INCREMENT]]),
        (0x9e0129, 'AB', [Keycode.F3]),
        # 4th row ----------
        (0x9e0129,  '<<', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x9e0129, 'Play/Pause', [[ConsumerControlCode.PLAY_PAUSE]]),
        (0x9e0129, '>>', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
     
        (0x9e0129, '', [Keycode.BACKSPACE])
    ]
}
