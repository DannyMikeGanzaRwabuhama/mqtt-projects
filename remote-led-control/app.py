import paho.mqtt.client as mqtt
import serial
import time

# --- MQTT Configuration ---
BROKER = "157.173.101.159"
PORT = 1883
TOPIC = "/mike/light_control"

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

# --- Global variable for serial connection ---
ser = None

# --- MQTT Callbacks ---

def on_connect(client, userdata, flags, rc):
    """Callback function when the client connects to the MQTT broker."""
    if rc == 0:
        print("Connected to MQTT broker!")
        client.subscribe(TOPIC) # Subscribe to the topic to receive commands
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Failed to connect to MQTT broker with code {rc}")

def on_message(client, userdata, msg):
    """Callback function when a message is received on the subscribed topic."""
    command = msg.payload.decode("utf-8").strip().upper() # Decode, trim whitespace, and convert to uppercase

    print(f"Received MQTT command: {command}")

    if ser and ser.is_open:
        try:
            # Send the command followed by a newline character
            # Your Arduino code uses readStringUntil('\n'), so a newline is crucial.
            ser.write((command + '\n').encode('utf-8'))
            print(f"Sent '{command}' to Arduino via serial.")
        except serial.SerialException as e:
            print(f"Error writing to serial port: {e}")
            # Attempt to reconnect or handle the error
    else:
        print("Serial port not open or not initialized. Cannot send command to Arduino.")

# --- Main Program Logic ---

if __name__ == "__main__":
    # Initialize Serial Port
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) # timeout helps prevent blocking
        time.sleep(2) # Give the serial port some time to initialize
        print(f"Successfully connected to serial port: {SERIAL_PORT}")
    except serial.SerialException as e:
        print(f"Error opening serial port {SERIAL_PORT}: {e}")
        print("Please check if the Arduino is connected and the port is correct/available.")
        exit() # Exit if we can't establish serial connection

    # Initialize MQTT Client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # Connect to MQTT Broker
    try:
        mqtt_client.connect(BROKER, PORT, 60)
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        ser.close() # Close serial if MQTT connection fails
        exit()

    # Start the MQTT loop in a non-blocking way
    mqtt_client.loop_start()

    print("Python script running, bridging MQTT to serial. Press Ctrl+C to exit.")

    try:
        # Keep the main thread alive so MQTT loop can run in the background
        while True:
            time.sleep(1) # Small delay to prevent busy-waiting
    except KeyboardInterrupt:
        print("\nExiting script...")
    finally:
        mqtt_client.loop_stop() # Stop the MQTT loop
        mqtt_client.disconnect() # Disconnect from MQTT broker
        if ser and ser.is_open:
            ser.close() # Close the serial port
            print("Serial port closed.")
        print("Script terminated.")