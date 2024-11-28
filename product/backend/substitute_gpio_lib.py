
# GPIO Constants
LOW = 0
HIGH = 1

IN = 0
OUT = 1

PUD_DOWN = LOW

SERIAL_INPUT_PIN = 18
LATCH_OUTPUT_PIN = 15
CLOCK_OUTPUT_PIN = 14

global virtual_index
virtual_index = 0

BOARD = "BOARD" # Use board pins
BCM = BOARD

# Left 10 bits represent bits from the sensor and can be changed for testing
# Rightmost bits would be tied to ground on the shift register and should be
#   left at 0
_virtual_he_bits = [
    # ONLY ADJUST THESE     DON'T TOUCH
    1,1,0,0,0,0,0,0,0,0,    0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,    0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,    0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,    0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,    0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,    0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,    0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,    0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,    0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,1,    0,0,0,0,0,0,
]

PINS = {}

_mode = ""

def setup(pin: int, direction: int, initial=LOW, pull_up_down=None):
    PINS[pin] = {"direction": direction, "state": initial}

    # print(f"Pin {pin} is set to {'OUTPUT' if direction else 'INPUT'} with state {'HIGH' if initial else 'LOW'}")

def output(pin: int, newstate: int):
    global virtual_index
    pin_state = PINS.get(pin)
    if (pin_state is None) or (pin_state["direction"] != OUT):
        print(f"ERROR: Pin {pin} is not an OUTPUT")
    else:
        # If changing the latch pin, HIGH state mimics the parallel loading
        # LOW state is for the serial read
        if pin == LATCH_OUTPUT_PIN:
            if pin_state["state"] == HIGH and newstate == LOW:
                virtual_index = 0
        elif pin == CLOCK_OUTPUT_PIN:
            if (pin_state["state"] == HIGH
                and newstate == LOW
                and PINS[LATCH_OUTPUT_PIN]["state"] == HIGH):
                virtual_index += 1
        pin_state["state"] = newstate
        # print(f"Pin {pin} is set to state {'HIGH' if newstate else 'LOW'}")

def input(pin):
    global virtual_index
    pin_state = PINS.get(pin)
    if pin_state["direction"] != IN:
        print(f"ERROR: Pin {pin} is not an INPUT")
        return None

    # print(f"Reading from Pin {pin}")
    if pin == SERIAL_INPUT_PIN:
        if virtual_index > 159:
            return 0
        return _virtual_he_bits[virtual_index]
    return 0
    

def setmode(mode):
    if mode != BOARD:
        print("ERROR: Mode should be set to GPIO.BOARD")
        return
    _mode = BOARD

def getmode():
    return _mode

"""
    Functions for testing adjustments to the board are below
"""

def unset_at_coord(pos: tuple) -> None:
    _virtual_he_bits[pos[0] * 16 + pos[1]] = 0

def set_at_coord(pos: tuple) -> None:
    _virtual_he_bits[pos[0] * 16 + pos[1]] = 1
