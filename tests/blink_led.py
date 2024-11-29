import RPi.GPIO as GPIO
import time

# Set up the LED_PIN
LED_PIN = 18

# Set the Broadcom GPIOs numbering
GPIO.setmode(GPIO.BCM)
# Set the LED_PIN as OUTPUT
GPIO.setup(LED_PIN, GPIO.OUT)

while True:
    GPIO.output(LED_PIN, 1)
    time.sleep(1)
    GPIO.output(LED_PIN, 0)
    time.sleep(1)