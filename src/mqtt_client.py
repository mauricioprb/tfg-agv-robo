import paho.mqtt.client as mqtt
import json  # Adicionado para conversão JSON

class MQTTClient:
    def __init__(self, broker_url, broker_port, username, password):
        self.client = mqtt.Client()
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.client.username_pw_set(username, password)

        self.client.tls_set()
        
        self.conectado = False
        self.topicos_callbacks = {}
        self.on_connect_callback = None  # Callback para execução após conexão
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker MQTT com sucesso.")
            self.conectado = True
            if self.on_connect_callback:
                self.on_connect_callback()  # Executa callback após conexão
        else:
            print(f"Falha na conexão com o broker MQTT. Código de retorno: {rc}")
        for topico in self.topicos_callbacks:
            self.client.subscribe(topico)
            print(f"Inscrito no tópico: {topico}")

    def set_on_connect_callback(self, callback):
        self.on_connect_callback = callback

    def on_message(self, client, userdata, msg):
        topico = msg.topic
        payload = msg.payload.decode()

        if topico in self.topicos_callbacks:
            print(f"Mensagem recebida no tópico {topico}: {payload}")
            self.topicos_callbacks[topico](payload)
        else:
            print(f"Tópico não registrado: {topico}")

    def registrar_topico(self, topico, callback):
        self.topicos_callbacks[topico] = callback

    def publicar(self, topico, mensagem):
        mensagem_json = json.dumps(mensagem)
        self.client.publish(topico, payload=mensagem_json)
        print(f"Mensagem publicada no tópico {topico}: {mensagem_json}")

    def iniciar(self):
        self.client.connect(self.broker_url, self.broker_port)
        self.client.loop_start()

    def finalizar(self):
        self.client.loop_stop()
        self.client.disconnect()
