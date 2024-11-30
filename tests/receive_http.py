from flask import Flask, request, jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

# GPIO setup
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

@app.route('/gpio', methods=['POST'])
def control_gpio():
    try:
        data = request.json  # Get JSON data from the POST request
        if not data or 'state' not in data:
            return jsonify({'error': 'Invalid request, missing "state" key'}), 400

        state = data['state'].lower()

        if state == 'on':
            GPIO.output(LED_PIN, GPIO.HIGH)
            return jsonify({'message': f'GPIO {LED_PIN} turned ON'}), 200
        elif state == 'off':
            GPIO.output(LED_PIN, GPIO.LOW)
            return jsonify({'message': f'GPIO {LED_PIN} turned OFF'}), 200
        else:
            return jsonify({'error': 'Invalid state. Use "on" or "off".'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup_gpio():
    try:
        GPIO.cleanup()
        return jsonify({'message': 'GPIO cleanup done'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)