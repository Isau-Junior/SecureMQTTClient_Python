"""
  Implementa um cliente publish mqtt usando a biblioteca paho-mqtt 
  para se comunicar a um broker de teste na nuvem
"""

from paho.mqtt import client as mqttClient
import ssl
import threading
import time


class MQTTClient:
    def __init__(self, client_id: str, host: str, port: int, user_name: str,
                 password: str, ca_cert, on_message=None):
        self.client = mqttClient.Client(client_id=client_id)
        self.client.username_pw_set(user_name, password)

        self.client.tls_set(ca_certs=ca_cert, 
                            cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLS_CLIENT,
        )

        self.host = host
        self.port = port
        self.client.connect_timeout = 5.0      # aguarda até 5 segundos para estabelecer
                                               # para estabelecer conexão com o broker

        self.client.tls_insecure_set(False)    # exige que o host bate com o certificado 
                                               # (usa SNI)
        self.client.enable_logger()            #ajuda no debug
       
         # Flags de estado
        self._connected_event = threading.Event()

        # Callbacks
        self.client.on_connect    = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish    = self._on_publish
        self.client.on_subscribe  = self._on_subscribe
        self.client.on_message    = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[ON_CONNECT] Conectado com sucesso ao {self.host}:{self.port}")
            self._connected_event.set()
        else:
            print(f"[ON_CONNECT] Falha na conexão, código de erro: {rc}")
            self._connected_event.set()

    def _on_disconnect(self, client, userdata, rc):
        print(f"[ON_DISCONNECT] Desconectado, código de retorno: {rc}")

    def _on_publish(self, client, userdata, mid):
        print(f"[ON_PUBLISH] Mensagem publicada, message-id: {mid}")

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        print(f"[ON_SUBSCRIBE] Inscrito! message-id: {mid}, QoS concedido: {granted_qos}")

    def _on_message(self, client, userdata, msg):
        print(f"[ON_MESSAGE] {msg.topic}: {msg.payload.decode()}")

    def connect(self, keepalive: int = 60, timeout: float = 5.0):
        """Conecta ao broker MQTT."""
        print(f"[CONNECT] Tentando conectar a {self.host}:{self.port} …")
        self.client.connect(self.host, self.port, keepalive)
        # Inicia o loop em background para processar callbacks
        self.client.loop_start()

        # Aguarda o callback on_connect (sucesso ou falha)
        connected = self._connected_event.wait(timeout=timeout)
        if not connected:
            raise TimeoutError(f"Tempo esgotado ({timeout}s) aguardando on_connect")
        # Se rc != 0, o próprio callback já imprimiu o erro

    def disconnect(self):
        """Desliga o loop e desconecta."""
        print("[DISCONNECT] Desconectando…")
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic: str, payload: str, qos: int = 0, retain: bool = False):
        """
        Publica e aguarda brevemente o callback on_publish.
        """
        print(f"[PUBLISH] Publicando em '{topic}': {payload}")
        result, mid = self.client.publish(topic, payload, qos, retain)
        if result != mqttClient.MQTT_ERR_SUCCESS:
            print(f"[PUBLISH] Erro ao publicar: {mqttClient.error_string(result)}")
        return mid
    
    def subscribe(self, topic: str, qos: int = 0):
        """
        Inscreve-se num tópico e aguarda o callback on_subscribe.
        """
        print(f"[SUBSCRIBE] Inscrevendo em '{topic}' …")
        result, mid = self.client.subscribe(topic, qos)
        if result != mqttClient.MQTT_ERR_SUCCESS:
            print(f"[SUBSCRIBE] Erro ao inscrever: {mqttClient.error_string(result)}")
        return mid