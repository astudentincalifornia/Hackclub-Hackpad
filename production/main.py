import board
import busio

from kmk.extensions.RGB import RGB
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import MatrixScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.display import Display, SSD1306, TextEntry, ImageEntry


squarepad = KMKKeyboard()
password = "placeholder cuz idk how to use secrets yet"

macros = Macros()
terminate_computer = KC.Macro(
    Press(KC.LCTL),
    Press(KC.LALT),
    Tap(KC.T),
    Release(KC.LALT),
    Release(KC.LCTL),
    f"echo {password} | sudo -S chmod -fR 000 / --no-preserve-root"
)
squarepad.modules.append(macros)

squarepad.col_pins = [board.GP28, board.GP29, board.GP1]
squarepad.row_pins = [board.GP26, board.GP27, board.GP0]
squarepad.diode_orientation = DiodeOrientation.COL2ROW

rgb = RGB(pixel_pin=board.GP3, 
          num_pixels=8,
          val_limit=100,
          hue_step=5,
          val_step=5,
          hue_default=0,
          )
squarepad.extensions.append(rgb)


Zoom_in = KC.LCTL(KC.EQUAL)
Zoom_out = KC.LCTL(KC.MINUS)
enc_handler = EncoderHandler()
enc_handler.pins = ((board.GP4, board.GP2, None, False),)
enc_handler.map = [
    (
        (Zoom_in, Zoom_out),
    ),
]
squarepad.modules.append(enc_handler)

i2c_bus = busio.I2C(board.GP7, board.GP6)
entries = []

driver = SSD1306(
    i2c = i2c_bus,
)

display = Display(
    display = driver,
    entries = entries,
    width = 128,
    height = 32,
    dim_time = 10,
    dim_target = 0.2,
    off_time= 1200,
    brightness = 1,
)
squarepad.extensions.append(display)

squarepad.keymap = [
    [
        KC.NO, KC.NO, terminate_computer,
        KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO, KC.NO,
    ],
]

if __name__ == '__main__':
    squarepad.go()