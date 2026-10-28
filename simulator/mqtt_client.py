import paho.mqtt.client as mqtt

def connect_mqtt(config):
    client = mqtt.Client()
    
    if config.get("username"):
        client.username_pw_set(config["username"], config["password"])
    
    client.connect(config["host"], config["port"], 60)
    return client
