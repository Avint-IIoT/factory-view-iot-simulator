import json
import logging
import shutil
import threading
from pathlib import Path
from urllib.parse import quote

import uvicorn
import yaml
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mqtt_client import connect_mqtt
from devices import site_monitor, nrgy_monitor, machine_monitor, site_monitor_cch, site_monitor_inz, ipc_monitor

# Rutas absolutas: el simulador funciona sin importar desde qué carpeta se ejecute
SIMULATOR_DIR = Path(__file__).resolve().parent
BASE_DIR = SIMULATOR_DIR.parent
CONFIG_FILE = BASE_DIR / "config.yaml"
EXAMPLE_CONFIG_FILE = BASE_DIR / "config.example.yaml"

# Cada tipo de dispositivo es una función que devuelve un dict con los datos a publicar.
# Para agregar un tipo nuevo basta con registrarlo aquí (la UI lo muestra automáticamente).
DEVICE_TYPES = {
    "site_monitor": site_monitor.generate_payload,
    "nrgy_monitor": nrgy_monitor.generate_payload,
    "machine_monitor": machine_monitor.generate,
    "site_monitor_cch": site_monitor_cch.generate_payload,
    "site_monitor_inz": site_monitor_inz.generate_payload,
    "ipc_monitor": ipc_monitor.generate_payload,
}

MIN_INTERVAL = 1  # segundos

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("simulador")

app = FastAPI()
templates = Jinja2Templates(directory=SIMULATOR_DIR / "templates")
app.mount("/static", StaticFiles(directory=SIMULATOR_DIR / "static"), name="static")


# ---------------------------------------------------------------------------
# Configuración (config.yaml)
# ---------------------------------------------------------------------------

config_lock = threading.Lock()  # evita que dos peticiones escriban el archivo a la vez


def load_config():
    if not CONFIG_FILE.exists():
        shutil.copy(EXAMPLE_CONFIG_FILE, CONFIG_FILE)
    with open(CONFIG_FILE, encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    config.setdefault("devices", [])
    return config


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True)


def validate_device(device_id, device_type, interval, devices, editing=False):
    """Devuelve un mensaje de error, o None si el dispositivo es válido."""
    if not device_id.strip():
        return "El ID no puede estar vacío."
    if device_type not in DEVICE_TYPES:
        return f"Tipo de dispositivo desconocido: {device_type}"
    if interval < MIN_INTERVAL:
        return f"El intervalo debe ser de al menos {MIN_INTERVAL} segundo(s)."
    exists = any(d["id"] == device_id for d in devices)
    if exists and not editing:
        return f"Ya existe un dispositivo con ID {device_id}."
    if not exists and editing:
        return f"No existe el dispositivo {device_id}."
    return None


# ---------------------------------------------------------------------------
# Simulación: un hilo por dispositivo
# ---------------------------------------------------------------------------

mqtt_client = None
running = {}  # id del dispositivo -> threading.Event para detener su hilo


def run_device(device, stop_event):
    gen = DEVICE_TYPES[device["type"]]
    while not stop_event.is_set():
        try:
            payload = gen()
            if mqtt_client.is_connected():
                mqtt_client.publish(device["topic"], json.dumps(payload))
                log.info("[%s] -> %s", device["id"], payload)
            else:
                log.warning("[%s] Sin conexión al broker, mensaje no enviado", device["id"])
        except Exception:
            # Un error en un dispositivo no debe detener la simulación
            log.exception("[%s] Error generando o publicando datos", device["id"])
        # wait() en lugar de sleep(): al detener el dispositivo, el hilo termina de inmediato
        stop_event.wait(device["interval"])


def start_device(device):
    if device.get("type") not in DEVICE_TYPES:
        log.error("[%s] Tipo desconocido '%s', no se inicia", device.get("id"), device.get("type"))
        return
    stop_event = threading.Event()
    running[device["id"]] = stop_event
    threading.Thread(target=run_device, args=(device, stop_event), daemon=True).start()
    log.info("[%s] Iniciado (cada %ss en %s)", device["id"], device["interval"], device["topic"])


def stop_device(device_id):
    stop_event = running.pop(device_id, None)
    if stop_event:
        stop_event.set()
        log.info("[%s] Detenido", device_id)


def restart_device(device):
    stop_device(device["id"])
    start_device(device)


# ---------------------------------------------------------------------------
# Interfaz web
# ---------------------------------------------------------------------------

def redirect_home(error=None):
    url = f"/?error={quote(error)}" if error else "/"
    return RedirectResponse(url, status_code=303)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, error: str | None = None):
    config = load_config()
    return templates.TemplateResponse(request=request, name="index.html", context={
        "devices": config["devices"],
        "device_types": DEVICE_TYPES.keys(),
        "mqtt_connected": mqtt_client is not None and mqtt_client.is_connected(),
        "mqtt_host": config.get("mqtt", {}).get("host"),
        "error": error,
    })


@app.post("/add")
def add_device(type: str = Form(...), device_id: str = Form(...), topic: str = Form(...), interval: int = Form(...)):
    device_id = device_id.strip()
    with config_lock:
        config = load_config()
        error = validate_device(device_id, type, interval, config["devices"])
        if error:
            return redirect_home(error)

        device = {"type": type, "id": device_id, "topic": topic.strip(), "interval": interval}
        config["devices"].append(device)
        save_config(config)

    start_device(device)
    return redirect_home()


@app.post("/edit")
def edit_device(device_id: str = Form(...), topic: str = Form(...), interval: int = Form(...)):
    with config_lock:
        config = load_config()
        device = next((d for d in config["devices"] if d["id"] == device_id), None)
        error = validate_device(device_id, device["type"] if device else "", interval, config["devices"], editing=True)
        if error:
            return redirect_home(error)

        device["topic"] = topic.strip()
        device["interval"] = interval
        save_config(config)

    restart_device(device)
    return redirect_home()


@app.post("/delete")
def delete_device(device_id: str = Form(...)):
    with config_lock:
        config = load_config()
        config["devices"] = [d for d in config["devices"] if d["id"] != device_id]
        save_config(config)

    stop_device(device_id)
    return redirect_home()


def start_simulator():
    global mqtt_client
    config = load_config()
    mqtt_client = connect_mqtt(config["mqtt"])

    for device in config["devices"]:
        start_device(device)


if __name__ == "__main__":
    start_simulator()
    uvicorn.run(app, host="0.0.0.0", port=9876)
