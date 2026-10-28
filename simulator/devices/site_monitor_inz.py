import random
import time

def generate_payload():
    return {
        "ts": int(time.time()),
        "meas_temp_1": round(random.uniform(0, 60), 2),
        "meas_hmdt_1": round(random.uniform(20, 90), 2),
        "meas_temp_2": round(random.uniform(0, 60), 2),
        "meas_hmdt_2": round(random.uniform(20, 90), 2),
        "state_door_1": random.choice([0, 1]),
        "state_smok": random.choice([0, 1]),
        "state_flod": random.choice([0, 1]),
        "state_motn": random.choice([0, 1]),
        "cmd_fans": round(random.uniform(0, 9999), 2),
        "cmd_accs": random.choice([0, 1]),
        "state_vndl": random.choice([0, 1]),
        "meas_temp_3": round(random.uniform(-30, 10), 2)
    }