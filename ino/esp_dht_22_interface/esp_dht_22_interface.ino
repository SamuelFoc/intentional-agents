#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// ---- WIFI ------------------------------------------------------
const char* ssid = "Networker";
const char* password = "primitiv255";

// ---- DHT -------------------------------------------------------
#define DHTPIN 4         
#define DHTTYPE DHT22    
DHT dht(DHTPIN, DHTTYPE);

// ---- API -------------------------------------------------------
const char* serverUrl = "http://192.168.0.2:5000/temperature";

// ----------------------------------------------------------------

// Sleep duration (in microseconds)
const uint64_t sleepDuration = 1 * 60 * 1000000; // 1 minute

void setup() {
  Serial.begin(115200);
  // Initialize the DHT sensor
  dht.begin();
  connectToWiFi();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Check if reading was successful
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    goToDeepSleep();
  }

  // Log readings
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print("°C, Humidity: ");
  Serial.print(humidity);
  Serial.println("%");

  // Send data to server
  if (WiFi.status() == WL_CONNECTED) {
    sendToServer(temperature, humidity);
  } else {
    Serial.println("WiFi not connected!");
  }

  // Go to deep sleep to save energy
  goToDeepSleep();
}

// Function to connect to WiFi
void connectToWiFi() {e
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

// Function to send data to the server
void sendToServer(float temperature, float humidity) {
  HTTPClient http;
  http.begin(serverUrl); // Specify the URL
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
}

// Function to enter deep sleep
void goToDeepSleep() {
  Serial.println("Going to deep sleep...");
  WiFi.disconnect(true); // Disconnect WiFi to save power
  WiFi.mode(WIFI_OFF);   // Turn off WiFi
  esp_deep_sleep_start(); // Start deep sleep
}

void configureSleepDuration() {
  esp_sleep_enable_timer_wakeup(sleepDuration); // Set deep sleep duration
}
