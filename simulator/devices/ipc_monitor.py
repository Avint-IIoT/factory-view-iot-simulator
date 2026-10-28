import random
import time


def generate_payload():
    return {
        "ts": int(time.time()),
        "meas_time_timestamp": int(time.time()),

        # ---------------- Fase A ----------------
        "meas_pact_a": round(random.uniform(0, 3000), 2),
        "meas_papp_a": round(random.uniform(0, 3500), 2),
        "meas_curr_a": round(random.uniform(0, 30), 2),
        "meas_freq_a": round(random.uniform(59.8, 60.2), 2),
        "meas_pfct_a": round(random.uniform(0.7, 1.0), 2),
        "meas_volt_a": round(random.uniform(120, 134), 2),

        # ---------------- Fase B ----------------
        "meas_pact_b": round(random.uniform(0, 3000), 2),
        "meas_papp_b": round(random.uniform(0, 3500), 2),
        "meas_curr_b": round(random.uniform(0, 30), 2),
        "meas_freq_b": round(random.uniform(59.8, 60.2), 2),
        "meas_pfct_b": round(random.uniform(0.7, 1.0), 2),
        "meas_volt_b": round(random.uniform(120, 134), 2),

        # ---------------- Fase C ----------------
        "meas_pact_c": round(random.uniform(0, 3000), 2),
        "meas_papp_c": round(random.uniform(0, 3500), 2),
        "meas_curr_c": round(random.uniform(0, 30), 2),
        "meas_freq_c": round(random.uniform(59.8, 60.2), 2),
        "meas_pfct_c": round(random.uniform(0.7, 1.0), 2),
        "meas_volt_c": round(random.uniform(120, 134), 2),

        # ---------------- Totales ----------------
        "meas_pact_total": round(random.uniform(0, 9000), 2),
        "meas_papp_total": round(random.uniform(0, 10500), 2),
        "meas_curr_total": round(random.uniform(0, 90), 2),

        # ---------------- Energia acumulada (kWh) ----------------
        "meas_nrgy_total_a": round(random.uniform(0, 99999), 2),
        "meas_nrgy_total_reta": round(random.uniform(0, 500), 2),
        "meas_nrgy_total_b": round(random.uniform(0, 99999), 2),
        "meas_nrgy_total_retb": round(random.uniform(0, 500), 2),
        "meas_nrgy_total_c": round(random.uniform(0, 99999), 2),
        "meas_nrgy_total_retc": round(random.uniform(0, 500), 2),
        "meas_nrgy_total": round(random.uniform(0, 299997), 2),
        "meas_nrgy_total_return": round(random.uniform(0, 1500), 2),

        # ---------------- Energia instantanea (kWh) ----------------
        "meas_nrgy_inst_a": round(random.uniform(0, 0.01), 4),
        "meas_nrgy_inst_b": round(random.uniform(0, 0.01), 4),
        "meas_nrgy_inst_c": round(random.uniform(0, 0.01), 4),
        "meas_nrgy_inst_total": round(random.uniform(0, 0.03), 4),

        # ---------------- Ambiente ----------------
        "meas_temp_1": round(random.uniform(15, 40), 2),
        "meas_hmdt_1": round(random.uniform(20, 90), 2),
        "calc_dewp_1": round(random.uniform(0, 25), 2),

        # ---------------- Estados (0 / 1) ----------------
        "meas_stat_door_1": random.choice([0, 1]),
        "meas_stat_powers": random.choice([0, 1]),
        "meas_stat_ups": random.choice([0, 1]),
        "meas_stat_Nivel1": random.choice([0, 1]),
        "meas_stat_Nivel2": random.choice([0, 1]),
        "meas_stat_door_2": random.choice([0, 1]),
        "meas_stat_door_3": random.choice([0, 1]),

        # ---------------- Baterias ----------------
        "meas_volt_batis_1": round(random.uniform(80, 98), 2),
        "meas_volt_batds_1": round(random.uniform(11.5, 14.0), 2),
        "meas_volt_batds_2": round(random.uniform(11.5, 14.0), 2),
        "meas_volt_batds_3": round(random.uniform(11.5, 14.0), 2),
        "meas_volt_batds_4": round(random.uniform(11.5, 14.0), 2),
        "meas_volt_batds_5": round(random.uniform(11.5, 14.0), 2),
        "meas_volt_batds_6": round(random.uniform(11.5, 14.0), 2),
        "meas_volt_batds_7": round(random.uniform(11.5, 14.0), 2),
    }