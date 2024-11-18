import json

class MqttMetricsPublisher:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def calcular_velocidade(self):
        rpm = 200
        raio_roda_metros = 0.03
        return (2 * 3.14159 * raio_roda_metros * rpm) / 60

    def enviar_metricas(self):
        print("Executando enviar_metricas para enviar 'Em operação'.")
        metricas = {
            "status": "Em operação",
            "velocidade": self.calcular_velocidade()
        }
        self.mqtt_client.publicar("agv/metricas", metricas)
        print(f"Métricas enviadas no tópico agv/metricas: {metricas}")

    def enviar_status_ligado(self):
        status = {
            "status": "Ligado"
        }
        self.mqtt_client.publicar("agv/metricas", status)
        print("Status enviado no tópico agv/metricas: Ligado")
