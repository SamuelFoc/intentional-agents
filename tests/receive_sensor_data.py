from flask import Flask, request, jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

# GPIO setup
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Thresholds for controlling the LED
TEMP_THRESHOLD = 25.0  # Temperature in °C
HUMIDITY_THRESHOLD = 50.0  # Humidity in %

@app.route('/temperature', methods=['POST'])
def temperature():
    try:
        # Parse JSON payload
        data = request.json
        temperature = data.get('temperature')
        humidity = data.get('humidity')

        if temperature is None or humidity is None:
            return jsonify({'error': 'Invalid data, temperature and humidity are required'}), 400

        # Log received data
        print(f"Received Temperature: {temperature}°C, Humidity: {humidity}%")

        # Control the LED based on thresholds
        if temperature > TEMP_THRESHOLD or humidity > HUMIDITY_THRESHOLD:
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED ON
            print("LED ON: Threshold exceeded")
        else:
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED OFF
            print("LED OFF: Threshold not exceeded")

        return jsonify({'status': 'success', 'temperature': temperature, 'humidity': humidity}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        GPIO.cleanup()  # Reset GPIO settings
        return jsonify({'message': 'GPIO cleanup done'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
