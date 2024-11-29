import RPi.GPIO as GPIO
import time

# Set up the LED_PIN
LED_PIN = 18
BTN_UP = 17
BTN_DOWN = 22
BTN_OK = 27

# Set the Broadcom GPIOs numbering
GPIO.setmode(GPIO.BCM)
# Set the LED_PIN as OUTPUT
GPIO.setup(LED_PIN, GPIO.OUT)
# Set the BTN pins as INPUTS with PULL-UP resistors
GPIO.setup([BTN_UP, BTN_OK, BTN_DOWN], GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
        # Read button states
        up_btn = GPIO.input(BTN_UP)   # Read BTN_UP state
        ok_btn = GPIO.input(BTN_OK)   # Read BTN_OK state
        down_btn = GPIO.input(BTN_DOWN)  # Read BTN_DOWN state

        if not up_btn:  # BTN_UP pressed (active LOW)
            GPIO.output(LED_PIN, 1)  # Turn LED ON
            print("ON")
        elif not down_btn:  # BTN_DOWN pressed (active LOW)
            GPIO.output(LED_PIN, 0)  # Turn LED OFF
            print("OFF")

        time.sleep(0.1)  # Debounce delay
    