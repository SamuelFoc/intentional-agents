# import RPi.GPIO as GPIO
from EmulatorGUI import GPIO
import time
import numpy as np

# GPIO Pin Setup
BUTTON_UP = 17
BUTTON_OK = 27
BUTTON_DOWN = 22
LED_PIN = 18
LDR_PIN = 0  # Simulated analog input

GPIO.setmode(GPIO.BCM)
GPIO.setup([BUTTON_UP, BUTTON_OK, BUTTON_DOWN], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm = GPIO.PWM(LED_PIN, 100)  # PWM frequency at 100 Hz
pwm.start(0)

# Simulated LDR Reading (Replace with ADC Reading)
def read_light_sensor():
    return np.random.randint(0, 1024)  # Replace this with actual ADC value

# Linear Mapping Parameters
MAX_BRIGHTNESS = 100  # LED PWM duty cycle
MAX_LIGHT_INTENSITY = 1024  # Maximum ADC value

def calculate_brightness(light_intensity):
    """Calculate LED brightness using linear mapping."""
    brightness = MAX_BRIGHTNESS * (1 - light_intensity / MAX_LIGHT_INTENSITY)
    return max(0, min(brightness, MAX_BRIGHTNESS))

# Reinforcement Learning Parameters
STATE_SPACE = 10  # Discretized light levels
ACTION_SPACE = 3  # Actions: Increase, Decrease, Maintain
q_table = np.zeros((STATE_SPACE, 10, ACTION_SPACE))  # Q-Table
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate

# Helper Functions
def take_action(action, current_brightness):
    """Adjust brightness based on action."""
    if action == 0:  # Increase
        return min(current_brightness + 1, 9)
    elif action == 1:  # Decrease
        return max(current_brightness - 1, 0)
    return current_brightness  # Maintain

# Initial States
current_brightness = 5  # LED brightness index
brightness_levels = np.linspace(0, MAX_BRIGHTNESS, 10)

try:
    while True:
        # Read ambient light
        light_intensity = read_light_sensor()
        light_state = min(int(light_intensity / 102.4), STATE_SPACE - 1)

        # Calculate initial brightness using linear mapping
        baseline_brightness = calculate_brightness(light_intensity)
        
        # RL Decision
        if np.random.uniform(0, 1) < epsilon:
            action = np.random.randint(0, ACTION_SPACE)  # Explore
        else:
            action = np.argmax(q_table[light_state, current_brightness])  # Exploit

        # Apply action
        adjusted_brightness = take_action(action, current_brightness)
        final_brightness = max(0, min(baseline_brightness + adjusted_brightness, MAX_BRIGHTNESS))
        pwm.ChangeDutyCycle(brightness_levels[adjusted_brightness])

        # Wait for feedback
        reward = -1  # Default penalty
        start_time = time.time()
        while time.time() - start_time < 5:  # 5-second feedback window
            if not GPIO.input(BUTTON_UP):
                reward = 1 if action == 0 else -1
                break
            elif not GPIO.input(BUTTON_OK):
                reward = 2 if action == 2 else -1
                break
            elif not GPIO.input(BUTTON_DOWN):
                reward = 1 if action == 1 else -1
                break

        # Update Q-Table
        q_table[light_state, current_brightness, action] += alpha * (
            reward + gamma * np.max(q_table[light_state, adjusted_brightness]) - q_table[light_state, current_brightness, action]
        )

        # Move to the new state
        current_brightness = adjusted_brightness

        print(f"Light: {light_intensity}, Brightness: {brightness_levels[current_brightness]}%, Reward: {reward}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    pwm.stop()
    GPIO.cleanup()
