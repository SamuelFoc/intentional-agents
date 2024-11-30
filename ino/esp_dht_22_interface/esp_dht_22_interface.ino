#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// WiFi credentials
const char* ssid = "Networker";
const char* password = "primitiv255";

// DHT configuration
#define DHTPIN 4         // Pin where the DHT22 is connected
#define DHTTYPE DHT22    // Specify DHT type
DHT dht(DHTPIN, DHTTYPE);

// Server URL
const char* serverUrl = "http://192.168.0.2:5000/temperature";

void setup() {
  Serial.begin(115200);
  
  // Initialize the DHT sensor
  dht.begin();
  
  // Connect to WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Read temperature and humidity from the DHT sensor
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Check if reading was successful
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Log readings
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print("°C, Humidity: ");
  Serial.print(humidity);
  Serial.println("%");

  // Send data to server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverUrl);           // Specify the URL
    http.addHeader("Content-Type", "application/json"); // Add headers for JSON payload

    // Create JSON payload
    String payload = "{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + "}";

    // Send POST request
    int httpResponseCode = http.POST(payload);

    // Handle response
    if (httpResponseCode > 0) {
      String response = http.getString(); // Get the response to the request
      Serial.print("Server Response: ");
      Serial.println(response);
    } else {
      Serial.print("Error sending POST request: ");
      Serial.println(httpResponseCode);
    }

    http.end(); // Free resources
  } else {
    Serial.println("WiFi not connected!");
  }

  // Wait before sending the next reading
  delay(1000); // Send data every 1 second
}