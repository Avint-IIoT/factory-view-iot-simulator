import random
import time

def generate_payload():
    b_voltage = random.uniform(120, 127)
    c_voltage = random.uniform(120, 127)
    b_current = random.uniform(1, 5)
    c_current = random.uniform(1, 5)

    return {
        "ts": int(time.time()),
        "time_elapsed": random.uniform(0, 10),
        "id": 0,
        "b_act_power": round(b_voltage * b_current * 0.9, 2),
        "b_aprt_power": round(b_voltage * b_current, 2),
        "b_current": round(b_current, 3),
        "b_freq": 60,
        "b_pf": round(random.uniform(0.8, 1), 2),
        "b_voltage": round(b_voltage, 1),
        "c_act_power": round(c_voltage * c_current * 0.9, 2),
        "c_aprt_power": round(c_voltage * c_current, 2),
        "c_current": round(c_current, 3),
        "c_freq": 60,
        "c_pf": round(random.uniform(0.8, 1), 2),
        "c_voltage": round(c_voltage, 1),
        "n_current": None,
        "total_act_power": round((b_voltage*b_current)+(c_voltage*c_current), 2),
        "total_aprt_power": round((b_voltage*b_current)+(c_voltage*c_current), 2),
        "total_current": round(b_current + c_current, 3),
        "total_act": random.uniform(1000000, 2000000),
        "b_wh": random.uniform(0, 2),
        "c_wh": random.uniform(0, 2),
        "total_wh": random.uniform(0, 5),
        "total_energy_diff": 0
    }
