import random
import time

def generate_payload():
    return {
        "T": random.randint(20, 35),
        "H": random.randint(10, 60),
        "D": random.randint(0, 1),
        "S": random.randint(0, 1),
        "W": random.randint(0, 1),
        "M": random.randint(0, 1),
        "A": random.randint(0, 1),
        "F": random.randint(0, 1),
        "K": random.randint(0, 1),
        "V": random.randint(0, 1),
        "sT": 0,
        "ts": int(time.time())
    }
