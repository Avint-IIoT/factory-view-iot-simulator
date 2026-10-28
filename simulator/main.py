import yaml, time, threading, json, os, shutil
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import multipart
from fastapi.staticfiles import StaticFiles

from mqtt_client import connect_mqtt
from devices import site_monitor, nrgy_monitor, machine_monitor, site_monitor_cch, site_monitor_inz, ipc_monitor

CONFIG_FILE = "config.yaml"
EXAMPLE_CONFIG_FILE = "config.example.yaml"
DEVICE_TYPES = {
    "site_monitor": site_monitor.generate_payload,
    "nrgy_monitor": nrgy_monitor.generate_payload,
    "machine_monitor": machine_monitor.generate,
    "site_monitor_cch": site_monitor_cch.generate_payload,
    "site_monitor_inz": site_monitor_inz.generate_payload,
    "ipc_monitor": ipc_monitor.generate_payload
}

app = FastAPI()
templates = Jinja2Templates(directory="simulator/templates")
app.mount("/static", StaticFiles(directory="simulator/static"), name="static")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        shutil.copy(EXAMPLE_CONFIG_FILE, CONFIG_FILE)
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f)


def run_device(device, mqtt_client):
    gen = DEVICE_TYPES[device["type"]]
    while True:
        payload = gen()
        mqtt_client.publish(device["topic"], json.dumps(payload))
        print(f"[{device['id']}] -> {payload}")
        time.sleep(device["interval"])


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    config = load_config()
    return templates.TemplateResponse(request=request, name="index.html", context={"devices": config["devices"]})


@app.post("/add")
def add_device(type: str = Form(...), device_id: str = Form(...), topic: str = Form(...), interval: int = Form(...)):
    config = load_config()
    config["devices"].append({
        "type": type,
        "id": device_id,
        "topic": topic,
        "interval": interval
    })
    save_config(config)
    return RedirectResponse("/", status_code=303)

@app.post("/edit")
def edit_device(device_id: str = Form(...), topic: str = Form(...), interval: int = Form(...)):
    config = load_config()

    for d in config["devices"]:
        if d["id"] == device_id:
            d["topic"] = topic
            d["interval"] = interval
            break

    save_config(config)
    return RedirectResponse("/", status_code=303)

@app.post("/delete")
def delete_device(device_id: str = Form(...)):
    config = load_config()
    config["devices"] = [d for d in config["devices"] if d["id"] != device_id]
    save_config(config)
    return RedirectResponse("/", status_code=303)


def start_simulator():
    config = load_config()
    client = connect_mqtt(config["mqtt"])
    client.loop_start()

    for device in config["devices"]:
        t = threading.Thread(target=run_device, args=(device, client), daemon=True)
        t.start()


if __name__ == "__main__":
    threading.Thread(target=start_simulator, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=9876)
