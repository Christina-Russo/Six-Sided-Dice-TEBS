"""
    This will only work on a pico

    Code for simulating our sensor array for testing purposes.
    This emulates a chain of 20 x 8-bit shift registers split into 10 rows of 2.
    10 hall effect sensors are attached to the first 10 parallel pins.

    Data out pin:   GPIO17
    Latch load pin: GPIO22
    Clock pin:      GPIO16

    These need to connect up with the relevant pins on the Raspberry Pi GPIO.  The
    pins needed will be in board_reader.py file.

    There are 4 physical hall effect sensors that read into the last 4 bits of the
    chain. You can use those for live testing.
"""


from machine import Pin
from time import sleep

LOW = 0
HIGH = 1

DATA = [0b11111111, 0b11111111,
        0b11111111, 0b11111111,
        0b11111111, 0b11111111,
        0b11111111, 0b11111111,
        0b11111111, 0b11111111,
        0b11111111, 0b11111111,
        0b11111111, 0b11111111,
        0b11111111, 0b11111111,
        0b11111111, 0b11111111,
        0b11111111, 0b11111111,
        ]
data_shift = DATA[:]

data_out_pin = machine.Pin(0, machine.Pin.OUT, value=LOW)
latch_pin = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
clk_pin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
he1 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
he2 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
he3 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
he4 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# LED_PIN = 25 # For Pico
LED_PIN = "LED" # For Pico W
led = machine.Pin(LED_PIN, machine.Pin.OUT, value=0)

curr_clk = LOW
clock_tick = False

def clk_interrupt(pin):
    global data_shift
    # sleep(0.05) # for debouncing
    if latch_pin.value() == HIGH:
        # print("clock")
        shift_data(data_shift)
    data_out_pin.value(data_shift[-1] & 0b00000001)
    
def latch_interrupt(pin):
    global DATA, data_shift
    flags = pin.irq().flags()
    if flags & Pin.IRQ_RISING:
        pass
        # print("latchon")
        # handle rising edge
    else:
        # handle falling edge
        data_shift = DATA[:]
        live_sensors = 0b11110000 | he1.value() | (he2.value() << 1) | (he3.value() << 2) | (he4.value() << 3)
        # print([he1.value(), (he2.value() << 1), (he3.value() << 2), (he4.value() << 3)])
        # print("Live sensors: " + str(live_sensors), end=' ')
        data_shift[-1] = live_sensors
        
        # print("latchoff")
    
def shift_data(data):
    global data_shift
    x = 19
    while x >= 0:
        data[x] = data[x] >> 1
        if x > 0 and not data[x - 1] & 0b00000001:
            data[x] &= 0b01111111
        else:
            data[x] |= 0b10000000
        x -= 1

    # print(data[19])
    data_shift = data[:]

# Wakeup blinks
for i in range(7):
    led.value(i%2)
    sleep(0.3)

clk_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=clk_interrupt)
latch_pin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=latch_interrupt)

# comment out loop when sending values to pico
# state = 0
# latch = 0

blink = False
while 1:
    # print(data_shift)
    # print([he1.value(), (he2.value() << 1), (he3.value() << 2), (he4.value() << 3)])
    led.value(blink)
    blink = not blink
    sleep(1)
