# Simulador IoT MQTT — Avint Factory View

Simulador de dispositivos IoT industriales que publican telemetría en formato JSON por **MQTT**.
Desde una interfaz web puedes crear, editar y eliminar dispositivos sin modificar código.

## 🚀 Características

- Simulación de varios tipos de dispositivos:

  | Tipo                | Descripción                                   |
  |---------------------|-----------------------------------------------|
  | `site_monitor`      | Monitor de sitio                              |
  | `site_monitor_cch`  | Monitor de sitio (variante CCH)               |
  | `site_monitor_inz`  | Monitor de sitio (variante INZ)               |
  | `nrgy_monitor`      | Monitor de energía (voltaje, corriente, potencia) |
  | `machine_monitor`   | Máquina con entradas analógicas, digitales y salidas |
  | `ipc_monitor`       | Monitor de PC industrial (IPC)                |

- Publicación periódica a cualquier broker MQTT
- Gestión de dispositivos desde una UI web
- Configuración persistente en `config.yaml`
- Contenerizado con Docker

---

## 📋 Requisitos

- **Python 3.10+** (o Docker)
- Git
- Opcional: un cliente MQTT para ver los mensajes, por ejemplo [MQTT Explorer](https://mqtt-explorer.com/)

---

## ▶️ Ejecutar localmente (Python)

```bash
git clone https://github.com/Avint-IIoT/factory-view-iot-simulator.git
cd factory-view-iot-simulator

# Crear y activar un entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt

# Ejecutar desde la raíz del proyecto
python simulator/main.py
```

Abre **http://localhost:9876** en el navegador.

> La primera vez, si no existe `config.yaml`, se crea automáticamente a partir de `config.example.yaml`.

---

## 🐳 Ejecutar con Docker

```bash
docker build -t iot-simulator .

# Linux / macOS / PowerShell
docker run --rm -it -p 9876:9876 -v ${PWD}/config.yaml:/app/config.yaml iot-simulator
```

> Antes de montar el volumen, crea `config.yaml` copiando `config.example.yaml`
> (si no, Docker crea una carpeta vacía con ese nombre).

---

## ⚙️ Configuración

El archivo `config.yaml` define el broker y los dispositivos:

```yaml
mqtt:
  host: broker.hivemq.com
  port: 1883
  username: ''
  password: ''

devices:
- id: SM-001
  type: site_monitor
  topic: capacitacion/factory/site_monitor/SM-001
  interval: 10        # segundos entre mensajes
```

- `config.yaml` **no se sube al repositorio** (está en `.gitignore`), así cada uno puede usar su propio broker y credenciales.
- Los dispositivos agregados desde la UI se guardan en `config.yaml`.
  **Reinicia el simulador** para que empiecen a publicar.

> ⚠️ `broker.hivemq.com` es un broker público: cualquiera puede leer lo que publiques. Úsalo solo con datos de prueba
> y usa un prefijo de topic propio (por ejemplo `capacitacion/<tu-nombre>/...`) para no mezclarte con otros.

---

## 👀 Ver los mensajes

Con **MQTT Explorer**: conéctate a `broker.hivemq.com:1883` y busca el topic `capacitacion/#`.

Con **mosquitto** desde la terminal:

```bash
mosquitto_sub -h broker.hivemq.com -t "capacitacion/#" -v
```

---

## 🧱 Estructura del proyecto

```
.
├── config.example.yaml     # Configuración de ejemplo
├── Dockerfile
├── requirements.txt
├── CHANGELOG.md
└── simulator/
    ├── main.py             # App web (FastAPI) + hilos de simulación
    ├── mqtt_client.py      # Conexión al broker MQTT
    ├── devices/            # Un archivo por tipo de dispositivo
    │   ├── site_monitor.py
    │   ├── site_monitor_cch.py
    │   ├── site_monitor_inz.py
    │   ├── nrgy_monitor.py
    │   ├── machine_monitor.py
    │   └── ipc_monitor.py
    ├── templates/
    │   └── index.html
    └── static/
        └── img/
```

---

## 🛠️ Agregar un nuevo tipo de dispositivo

1. Crea `simulator/devices/mi_dispositivo.py` con una función que devuelva un `dict`:

   ```python
   import random, time

   def generate_payload():
       return {
           "ts": int(time.time()),
           "temperatura": round(random.uniform(20, 30), 2),
       }
   ```

2. Regístralo en `DEVICE_TYPES` dentro de `simulator/main.py`.
3. Agrega la opción en el `<select name="type">` de `simulator/templates/index.html`.
