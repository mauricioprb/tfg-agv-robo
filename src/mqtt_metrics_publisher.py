import json
from mqtt_client import MQTTClient


class MqttMetricsPublisher:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def calcular_velocidade(self):
        rpm = 200
        raio_roda_metros = 0.03
        return (2 * 3.14159 * raio_roda_metros * rpm) / 60

    def enviar_metricas(self, status_operacao, velocidade):
        status = {
            "status": status_operacao,
            "velocidade": velocidade
        }
        mqtt_client.publicar("agv/teste", {"status": "TESTE"})
        print(f"Métricas enviadas no tópico agv/teste: {status}")

    def enviar_status_ligado(self):
        status = {
            "status": "Ligado"
        }
        self.mqtt_client.publicar("agv/metricas", status)
        print("Status enviado no tópico agv/metricas: Ligado")
