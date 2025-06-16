#include <DHT.h>

// Define the DHT sensor type and pin
#define DHTPIN 2
#define DHTTYPE DHT11

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("DHT11 Sensor Reader");
  dht.begin();
}

void loop() {
  delay(2000);

  // Read temperature
  float temperature = dht.readTemperature();

  // Read humidity
  float humidity = dht.readHumidity();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print("T:");
  Serial.print(temperature, 2);
  Serial.print(",H:");
  Serial.print(humidity, 2);
  Serial.println();
}