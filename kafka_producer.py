from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

buildings = ['A', 'B', 'C']
sensor_types = ['temperature', 'humidity', 'energy_consumption', 'co2']

while True:
    message = {
        "timestamp": int(time.time() * 1000),
        "device_id": f"sensor-{random.randint(1, 100):03d}",
        "building": random.choice(buildings),
        "floor": random.randint(1, 5),
        "type": random.choice(sensor_types),
        "value": round(random.uniform(0, 100), 2),
        "unit": "°C" if random.choice(sensor_types) == "temperature" else "kWh" if random.choice(sensor_types) == "energy_consumption" else "ppm"
    }
    producer.send('sensor_data', value=message)
    print(f"Produced: {message}")
    time.sleep(1)  # 1 message/seconde
