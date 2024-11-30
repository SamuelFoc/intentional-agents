from flask import Flask, request, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

# GPIO setup
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Thresholds for controlling the LED
TEMP_THRESHOLD = 25.0  # Temperature in °C
HUMIDITY_THRESHOLD = 50.0  # Humidity in %

# Variables to store the latest temperature and humidity
latest_temperature = None
latest_humidity = None

@app.route('/temperature', methods=['POST'])
def temperature():
    global latest_temperature, latest_humidity
    try:
        # Parse JSON payload
        data = request.json
        temperature = data.get('temperature')
        humidity = data.get('humidity')

        if temperature is None or humidity is None:
            return {"error": "Invalid data, temperature and humidity are required"}, 400

        # Update the latest temperature and humidity
        latest_temperature = temperature
        latest_humidity = humidity

        # Log received data
        print(f"Received Temperature: {temperature}°C, Humidity: {humidity}%")

        # Control the LED based on thresholds
        if temperature > TEMP_THRESHOLD or humidity > HUMIDITY_THRESHOLD:
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED ON
            print("LED ON: Threshold exceeded")
        else:
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED OFF
            print("LED OFF: Threshold not exceeded")

        return {"status": "success", "temperature": temperature, "humidity": humidity}, 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}, 500

@app.route('/current_temperature', methods=['GET'])
def current_temperature():
    global latest_temperature, latest_humidity
    try:
        if latest_temperature is None or latest_humidity is None:
            return render_template('current_temperature.html', 
                                   temperature=None, humidity=None)

        # Render the template with the latest data
        return render_template(
            'current_temperature.html',
            temperature=latest_temperature,
            humidity=latest_humidity
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}, 500

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        GPIO.cleanup()  # Reset GPIO settings
        return {"message": "GPIO cleanup done"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
