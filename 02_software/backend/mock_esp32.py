import json
import os
import random
import time
import signal

import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TELEMETRY_TOPIC", "smart-irrigation/telemetry")
DEVICE_ID = "esp32_station_01"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Connected to MQTT broker: {BROKER}:{PORT}")
    else:
        print(f"Connection failed: {reason_code}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    time.sleep(1)

    while True:
        payload = {
            "device_id": DEVICE_ID,
            "timestamp": int(time.time()),
            "sensors": {
                "soil_moisture_pct": round(random.uniform(20, 80), 1),
                "soil_temperature_c": round(random.uniform(15, 35), 1),
                "soil_ph": round(random.uniform(5.5, 8.0), 1),
                "nitrogen_mg_kg": None,
                "phosphorus_mg_kg": None,
                "potassium_mg_kg": None
            },
            "actuators": {"pump_state": False}
        }

        info = client.publish(TOPIC, json.dumps(payload), qos=0)
        info.wait_for_publish()
        print(f"Published to {TOPIC}: {json.dumps^(payload^)}")
        time.sleep(5)

except KeyboardInterrupt:
    print("\nPublisher stopped.")
finally:
    client.loop_stop()
    client.disconnect()
