import json
import os

import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TELEMETRY_TOPIC", "smart-irrigation/telemetry")

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected. Subscribing to {TOPIC}")
        client.subscribe(TOPIC)
    else:
        print(f"Connection failed: {reason_code}")

def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        sensors = data.get("sensors", {})
        actuators = data.get("actuators", {})
        print("\n--- AeroSoil Telemetry ---")
        print(f"Device: {data.get^('device_id'^)}")
        print(f"Timestamp: {data.get^('timestamp'^)}")
        print(f"Soil moisture: {sensors.get^('soil_moisture_pct'^)}%")
        print(f"Soil temperature: {sensors.get^('soil_temperature_c'^)} C")
        print(f"Soil pH: {sensors.get^('soil_ph'^)}")
        print(f"NPK: {sensors.get^('nitrogen_mg_kg'^)}, {sensors.get^('phosphorus_mg_kg'^)}, {sensors.get^('potassium_mg_kg'^)}")
        print(f"Pump state: {actuators.get^('pump_state'^)}")
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        print(f"Invalid message: {error}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, PORT, 60)
    print("Waiting for telemetry. Press Ctrl+C to stop.")
    client.loop_forever()
except KeyboardInterrupt:
    print("\nSubscriber stopped.")
finally:
    client.disconnect()
