import logging

import paho.mqtt.client as mqtt

log = logging.getLogger("mqtt")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        log.error("No se pudo conectar al broker: %s", reason_code)
    else:
        log.info("Conectado al broker MQTT")


def on_connect_fail(client, userdata):
    # Se llama cuando no se puede abrir la conexión (host mal escrito, puerto cerrado, sin red...)
    log.error("No se pudo alcanzar el broker. Revisa host y puerto en config.yaml. Reintentando...")


def on_disconnect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        log.warning("Se perdió la conexión con el broker (%s). Reintentando...", reason_code)
    else:
        log.info("Desconectado del broker")


def connect_mqtt(config):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_connect_fail = on_connect_fail
    client.on_disconnect = on_disconnect

    if config.get("username"):
        client.username_pw_set(config["username"], config.get("password"))

    # Si se pierde la conexión, paho reintenta solo (entre 1 y 30 segundos)
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    # connect_async no falla si el broker no está disponible al arrancar:
    # el loop sigue intentando conectarse en segundo plano.
    log.info("Conectando a %s:%s ...", config["host"], config["port"])
    client.connect_async(config["host"], config["port"], keepalive=60)
    client.loop_start()
    return client
