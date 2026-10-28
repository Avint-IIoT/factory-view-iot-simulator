import random
import time


def generate():
    return {

        # Analog inputs
        "A1": round(random.uniform(18, 35), 2),  # Temperatura °C
        "A2": round(random.uniform(30, 80), 2),  # Humedad %
        "A3": round(random.uniform(0, 100), 2),  # Presión simulada
        "A4": round(random.uniform(0, 100), 2),  # Vibración simulada

        # Digital inputs
        "D1": random.randint(0, 1),
        "D2": random.randint(0, 1),
        "D3": random.randint(0, 1),
        "D4": random.randint(0, 1),
        "D5": random.randint(0, 1),
        "D6": random.randint(0, 1),
        "D7": random.randint(0, 1),
        "D8": random.randint(0, 1),

        # Outputs
        "O1": random.randint(0, 1),
        "O2": random.randint(0, 1),
        "O3": random.randint(0, 1),
        "O4": random.randint(0, 1),
        "O5": random.randint(0, 1),
        "O6": random.randint(0, 1),
        "O7": random.randint(0, 1),
        "O8": random.randint(0, 1),

        # Timestamp
        "ts": int(time.time())
    }