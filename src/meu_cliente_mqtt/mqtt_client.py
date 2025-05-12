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

        self._connected_event = threading.Event()
        self._subscribed_event = threading.Event()
        self._published_event = threading.Event()  
        self._mensage_event = threading.Event()                         
        #self.client.enable_logger()            #ajuda no debug
       
        # Configuração de reconexão automática
        # Define um intervalo entre tentativas de reconexão, 
        #com crescimento exponencial entre 1s e 60s se a conexão cair.
        self.client.reconnect_delay_set(min_delay=1, max_delay=60)

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
        self._connected_event.clear()
        
        if rc != 0:
            print("[DISCONNECT] Tentando reconectar...")

    def _on_publish(self, client, userdata, mid):
        print(f"[ON_PUBLISH] Mensagem publicada, message-id: {mid}")
        self._published_event.set()

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        print(f"[ON_SUBSCRIBE] Inscrito! message-id: {mid}, QoS concedido: {granted_qos}")
        self._subscribed_event.set()

    def _on_message(self, client, userdata, msg):
        print(f"[ON_MESSAGE] {msg.topic}: {msg.payload.decode()}")
        self._mensage_event.set()

    def connect(self, keepalive: int = 60, timeout: float = 5.0):
        """Conecta ao broker MQTT."""
        print(f"[CONNECT] Tentando conectar a {self.host}:{self.port} …")
        # Garante que estamos esperando uma nova confirmação
        self._connected_event.clear() 
        self.client.connect_async(self.host, self.port, keepalive)
        # Inicia o loop em background para processar callbacks
        self.client.loop_start()

        # Espera até confirmar conexão
        if not self._connected_event.wait(timeout=5):
            raise TimeoutError("[CONNECT] Timeout: conexão não foi estabelecida.")

    def disconnect(self):
        """Desliga o loop e desconecta."""
        print("[DISCONNECT] Desconectando…")
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic: str, payload: str, qos: int = 0, retain: bool = False):
        """
        Publica e aguarda brevemente o callback on_publish e o callback on_mensage
        com a mensagem publicada naquele topico.
        """
        if not self._connected_event.wait(timeout=5):
            print("[WARN] Cliente desconectado. Aguardando reconexão para publicar...")
            return

        print(f"[PUBLISH] Publicando em '{topic}': {payload}")
        # Garante que estamos esperando uma nova confirmação
        self._published_event.clear()
        self._mensage_event.clear()
        result, mid = self.client.publish(topic, payload, qos, retain)
        if result != mqttClient.MQTT_ERR_SUCCESS:
            print(f"[PUBLISH] Erro ao publicar: {mqttClient.error_string(result)}")

        if not self._published_event.wait(timeout=5):
            print(f"[PUBLISH] Timeout: não houve confirmação de publicação" \
                                "da mensagem '{payload}' no tópico '{topic}'.")
            return
        self._mensage_event.wait()

        return mid
    
    def subscribe(self, topic: str, qos: int = 0):
        """
        Inscreve-se num tópico e aguarda os callbacks on_subscribe e on_mensage,
        com a ultima mensagem retida naquele tópico.
        """
        print(f"[SUBSCRIBE] Inscrevendo em '{topic}' …")
        # Garante que estamos esperando uma nova confirmação
        self._subscribed_event.clear()
        self._mensage_event.clear()
        result, mid = self.client.subscribe(topic, qos)
        if result != mqttClient.MQTT_ERR_SUCCESS:
            print(f"[SUBSCRIBE] Erro ao inscrever: {mqttClient.error_string(result)}")
    
        if not self._subscribed_event.wait(timeout=5):
            raise TimeoutError(f"[SUBSCRIBE] Timeout: não houve confirmação de inscrição" /
                                "no tópico '{topic}'.")
        self._mensage_event.wait()
        
        return mid