import random
import time

def generate_payload():
    lat = 19.0457666 + random.uniform(-0.0005, 0.0005)
    lon = -98.2145333 + random.uniform(-0.0005, 0.0005)

    t1 = random.uniform(2, 9)
    t2 = random.uniform(2, 9)
    t3 = random.uniform(2, 9)
    t4 = random.uniform(2, 9)

    h1 = random.uniform(45, 85)
    h2 = random.uniform(45, 85)
    h3 = random.uniform(45, 85)
    h4 = random.uniform(45, 85)

    return {
        "GPS": {
            "lat": round(lat, 7),
            "lon": round(lon, 7),
            "pre": random.randint(0, 30),
            "sat": random.randint(3, 12)
        },
        "OBDII": {},
        "Acel": {
            "x": round(random.uniform(-10, 110), 1),
            "y": round(random.uniform(-10, 10), 1),
            "z": round(random.uniform(-10, 10), 1)
        },
        "ts": int(time.time()),
        "lat": round(lat, 7),
        "lon": round(lon, 7),
        "on": random.choice([0, 1]),
        "GSMsig": random.randint(0, 5),
        "batteryLevel": random.randint(60, 100),
        "T": round(t1, 2),
        "T2": round(t2, 2),
        "T3": round(t3, 2),
        "T4": round(t4, 2),
        "H": round(h1, 0),
        "H2": round(h2, 0),
        "H3": round(h3, 0),
        "H4": round(h4, 0),
        "tempPromedio": (t1 + t2 + t3 + t4) / 4,
        "tempMax": round(max(t1, t2, t3, t4), 2),
        "tempMin": round(min(t1, t2, t3, t4), 2),
        "humPromedio": (h1 + h2 + h3 + h4) / 4,
        "humMax": round(max(h1, h2, h3, h4), 0),
        "humMin": round(min(h1, h2, h3, h4), 0),
        "T1_max": round(t1 + random.uniform(0, 0.3), 2),
        "T1_min": round(t1 - random.uniform(0, 0.3), 2),
        "T2_max": round(t2 + random.uniform(0, 0.3), 2),
        "T2_min": round(t2 - random.uniform(0, 0.3), 2),
        "T3_max": round(t3 + random.uniform(0, 0.3), 2),
        "T3_min": round(t3 - random.uniform(0, 0.3), 2),
        "T4_max": round(t4 + random.uniform(0, 0.3), 2),
        "T4_min": round(t4 - random.uniform(0, 0.3), 2),
        "H1_max": round(h1 + random.uniform(0, 5), 0),
        "H1_min": round(h1 - random.uniform(0, 5), 0),
        "H2_max": round(h2 + random.uniform(0, 5), 0),
        "H2_min": round(h2 - random.uniform(0, 5), 0),
        "H3_max": round(h3 + random.uniform(0, 5), 0),
        "H3_min": round(h3 - random.uniform(0, 5), 0),
        "H4_max": round(h4 + random.uniform(0, 5), 0),
        "H4_min": round(h4 - random.uniform(0, 5), 0),
        "D": random.choice([0, 1]),
        "D2": random.choice([0, 1]),
        "D3": random.choice([0, 1]),
        "D4": random.choice([0, 1]),
        "LB1": random.choice([0, 1]),
        "LB2": random.choice([0, 1]),
        "LB3": random.choice([0, 1]),
        "LB4": random.choice([0, 1]),
        "S": random.choice([0, 1]),
        "W": random.choice([0, 1]),
        "V": random.choice([0, 1]),
        "K": random.choice([0, 1]),
        "A": random.choice([0, 1]),
        "B": random.choice([0, 1]),
        "F": random.choice([0, 1]),
        "D5": random.choice([0, 1])
    }