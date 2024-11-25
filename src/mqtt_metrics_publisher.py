import json
import time

class MqttMetricsPublisher:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.current_position = None
        self.start_time = None
        self.is_moving = False
        self.route_names = {
            "DGA": "Descarga A",
            "DGB": "Descarga B",
            "ITM": "Interseção meio",
            "ITA": "Interseção A",
            "ITB": "Interseção B",
            "MNT": "Manutenção",
            "CRG": "Carga"
        }
        # Constantes para cálculo de distância
        self.RPM = 200  # Rotações por minuto
        self.DIAMETRO_RODA = 6  # 60mm em centímetros
        self.CIRCUNFERENCIA_RODA = self.DIAMETRO_RODA * 3.14159  # Perímetro da roda em cm
        
    def iniciar_timer(self):
        if not self.is_moving:
            self.start_time = time.time()
            self.is_moving = True
            
    def parar_timer(self):
        self.is_moving = False
        self.start_time = None
    
    def get_tempo_decorrido(self):
        if self.start_time is None:
            return 0
        return int(time.time() - self.start_time)
    
    def calcular_velocidade(self):
        """Calcula velocidade em centímetros por segundo"""
        # RPM * circunferência da roda = distância/minuto
        # Converte para cm/segundo
        return (self.RPM * self.CIRCUNFERENCIA_RODA) / 60
    
    def calcular_distancia(self, tempo_segundos):
        """
        Calcula a distância percorrida em centímetros
        
        Args:
            tempo_segundos (int): Tempo decorrido em segundos
        Returns:
            int: Distância em centímetros (arredondado para número inteiro)
        """
        velocidade_cms = self.calcular_velocidade()
        distancia = velocidade_cms * tempo_segundos
        return int(round(distancia))  
    
    def get_nome_rota(self, codigo_rota):
        return self.route_names.get(codigo_rota, codigo_rota)
    
    def enviar_metricas(self, status_operacao, velocidade, posicao_atual=None, chegou=False):
        if posicao_atual:
            self.current_position = posicao_atual
            
        tempo_decorrido = self.get_tempo_decorrido()
        nome_rota = self.get_nome_rota(self.current_position) if self.current_position else None
        distancia = self.calcular_distancia(tempo_decorrido) if self.is_moving else 0
            
        status = {
            "status": status_operacao,
            "velocidade": round(velocidade, 2),
            "rota": nome_rota,
            "tempo": tempo_decorrido,
            "chegou": chegou,
            "distancia": distancia  
        }
        
        self.mqtt_client.publicar("agv/metricas", status)
        print(f"Métricas enviadas: {status}")
    
    def enviar_status_ligado(self):
        status = {
            "status": "Ligado",
            "velocidade": 0,
            "rota": None,
            "tempo": 0,
            "chegou": False,
            "distancia": 0
        }
        self.mqtt_client.publicar("agv/metricas", status)
        print("Status enviado: Ligado")