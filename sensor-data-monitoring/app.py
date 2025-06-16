import serial
import paho.mqtt.client as mqtt
import time
import re

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# --- MQTT Broker Configuration ---
MQTT_BROKER = "157.173.101.159"
MQTT_PORT = 1883
MQTT_TOPIC = "mike/sensor_data"

# --- Global variables ---
ser = None
mqtt_client = None

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect to MQTT broker, return code {rc}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code: %s" % rc)
    if rc != 0:
        print("Unexpected disconnection. Attempting to re-connect...")
        time.sleep(5) # Wait before attempting to reconnect
        try:
            mqtt_client.reconnect()
        except Exception as e:
            print(f"Reconnect failed: {e}")

# --- Main Logic ---
if __name__ == "__main__":
    # 1. Initialize Serial Port
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"Successfully opened serial port: {SERIAL_PORT}")
    except serial.SerialException as e:
        print(f"Error opening serial port {SERIAL_PORT}: {e}")
        print("Please ensure the Arduino is connected and the correct port is selected.")
        exit()

    # 2. Initialize MQTT Client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect

    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
        print(f"Attempting to connect to MQTT broker: {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        ser.close()
        exit()

    print(f"Listening for sensor data on {SERIAL_PORT} and publishing to '{MQTT_TOPIC}'...")

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(f"Received from Arduino: '{line}'")

                # Use regex to parse the data (e.g., "T:25.00,H:60.00")
                match = re.match(r"T:([\d.]+),H:([\d.]+)", line)
                if match:
                    temperature = match.group(1)
                    humidity = match.group(2)

                    data_to_publish = line

                    try:
                        mqtt_client.publish(MQTT_TOPIC, data_to_publish)
                        print(f"Published to MQTT: '{data_to_publish}'")
                    except Exception as e:
                        print(f"Error publishing to MQTT: {e}")
                else:
                    print(f"Could not parse data: '{line}'")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting script...")
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial port closed.")
        if mqtt_client:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
            print("Disconnected from MQTT broker.")
        print("App terminated.")