import paho.mqtt.client as mqtt

# MQTT broker details
BROKER = "157.173.101.159"
PORT = 1883 # Default MQTT port
TOPIC = "/student_group/light_control"

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC) # Subscribe to the topic
    else:
        print(f"Connection failed with code {rc}")

# Call back when a message is received
def on_message(client, userdata, msg):
    command = msg.payload.decode("utf-8")
    if command == "ON":
        print("💡 Light is TURNED ON")
    elif command == "OFF":
        print("💡 Light is TURNED OFF")
    else:
        print(f"Received unknown command: {command}")

# Set up the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker and start the loop
client.connect(BROKER, PORT, 60)
client.loop_forever() # Keeps the script running and listening