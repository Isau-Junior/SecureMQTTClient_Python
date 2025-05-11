from mqtt_client import MQTTClient
from dotenv import load_dotenv
import os
import uuid
import time

def get_machine_id(file_path='machine_id.txt'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            machine_id = file.read().strip()
    else:
        machine_id = str(uuid.uuid1())
        with open(file_path, 'w') as file:
            file.write(machine_id)
    return machine_id


def main():
    load_dotenv(override=True)

    client_id = os.getenv("CLIENT_NAME") + get_machine_id()
    broker_host = os.getenv("BROKER_HOST")
    broker_port = int(os.getenv("PORT"))
    user_name = os.getenv("USER_NAME")
    password = os.getenv("PASSWORD")
    ca_cert = os.getenv('CERT_PATH')

    client = MQTTClient(
        client_id,
        broker_host,
        broker_port,
        user_name,
        password,
        ca_cert
    )

    try:
        client.connect()
        # Teste de subscribe
        client.subscribe("teste/status", qos=1)
         # Teste de publish
        client.publish("teste/status", "Hello World!", qos=1)
        # Permanece alguns segundos para receber callbacks
        print("Aguardando callbacks…")
        time.sleep(5)
    except Exception as e:
        print("Erro durante o teste:", e)
    finally:
        client.disconnect()

if  __name__ == "__main__":
    main()