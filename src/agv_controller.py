import time
import json
import pigpio
import RPi.GPIO as GPIO
import mfrc522 as MFRC522
from motor import Motor

class AGVController:
    def __init__(self, leitor_rfid, pi, pino_motor_esquerdo, pino_motor_direito, led_controller, mqtt_publisher, arquivo_dados_rfid='tags_rfid.json'):
        self.leitor_rfid = leitor_rfid
        self.pi = pi
        self.motor_esquerdo = Motor(self.pi, pino_gpio=pino_motor_esquerdo)
        self.motor_direito = Motor(self.pi, pino_gpio=pino_motor_direito)
        self.arquivo_dados_rfid = arquivo_dados_rfid
        self.dados = self.carregar_dados()
        self.caminho_retorno = False
        self.visitados_ida = set()
        self.visitados_volta = set()
        self.destino = None
        self.rota = []
        self.sensor = UltrassonicoController(trigger_pin=19, echo_pin=18)
        self.led_controller = led_controller
        self.mqtt_publisher = mqtt_publisher
        self.executando = True
        self.current_position = None

    def carregar_dados(self):
        try:
            with open(self.arquivo_dados_rfid, 'r') as arquivo:
                return json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def definir_rota(self, destino):
        if destino == "DGA":
            self.rota = ["CRG", "ITM", "ITA", "DGA", "#"]
        elif destino == "DGB":
            self.rota = ["CRG", "ITM", "ITB", "DGB", "#"]
        else:
            raise ValueError("Destino inválido! Use 'DGA' ou 'DGB'.")
        self.destino = destino

    def ler_uid(self):
        status, tipo_tag = self.leitor_rfid.MFRC522_Request(self.leitor_rfid.PICC_REQIDL)
        if status == self.leitor_rfid.MI_OK:
            status, uid = self.leitor_rfid.MFRC522_Anticoll()
            if status == self.leitor_rfid.MI_OK:
                return ':'.join(['%X' % x for x in uid])
        return None

    def parar_movimento(self):
        """Para imediatamente o movimento do AGV"""
        self.executando = False
        self.motor_direito.parar()
        self.motor_esquerdo.parar()
        self.led_controller.acender_vermelho()
        self.mqtt_publisher.parar_timer()
        self.mqtt_publisher.enviar_metricas(
            "Parado por comando",
            0,
            self.current_position,
            chegou=False
        )
        print("AGV parado por comando")

    def movimentar_agv(self):
        if not self.rota:
            raise ValueError("Rota não definida. Use 'definir_rota' para definir o destino.")
        
        self.executando = True
        self.motor_direito.controlar(2500)
        self.motor_esquerdo.controlar(2500)
        self.led_controller.acender_verde()
        self.mqtt_publisher.iniciar_timer()
        
        while self.executando:
            if self.sensor.check_obstacle():
                self.motor_direito.parar()
                self.motor_esquerdo.parar()
                self.led_controller.acender_vermelho()
                self.mqtt_publisher.parar_timer()
                time.sleep(0.1)
                continue
            
            if not self.executando:
                break
                
            self.led_controller.acender_verde()
            self.mqtt_publisher.iniciar_timer()
                
            uid = self.ler_uid()
            if uid:
                posicao_atual = self.dados.get(uid)
                self.current_position = posicao_atual
                if not self.caminho_retorno:
                    self.movimento_ida(posicao_atual)
                else:
                    self.movimento_volta(posicao_atual)
                time.sleep(1)
            else:
                if self.executando:
                    self.motor_direito.controlar(2500)
                    self.motor_esquerdo.controlar(2500)
                time.sleep(0.1)

    def movimento_ida(self, posicao_atual):
        if posicao_atual and posicao_atual not in self.visitados_ida:
            print(f"Posição atual (ida): {posicao_atual}")
            self.visitados_ida.add(posicao_atual)
            
            self.mqtt_publisher.enviar_metricas(
                "Em operação",
                self.mqtt_publisher.calcular_velocidade(),
                posicao_atual,
                chegou=False
            )

            if posicao_atual == "ITM":
                if self.destino == "DGA":
                    self.ajustar_motores(1000, 2500, 0.5)
                elif self.destino == "DGB":
                    self.ajustar_motores(2500, 1000, 0.5)
                self.ajustar_motores(2500, 2500)

            elif posicao_atual == "ITA" and self.destino == "DGA":
                self.ajustar_motores(2500, 1000, 0.5)
                self.ajustar_motores(2500, 2500)

            elif posicao_atual == "ITB" and self.destino == "DGB":
                self.ajustar_motores(1000, 2500, 0.5)
                self.ajustar_motores(2500, 2500)

            elif posicao_atual in ["CRG", "CMC", "CMM"]:
                self.ajustar_motores(2500, 2500)

            elif posicao_atual == self.destino:
                self.alcancar_destino()

            else:
                self.parar_para_ajuste()

    def movimento_volta(self, posicao_atual):
        if posicao_atual and posicao_atual not in self.visitados_volta:
            print(f"Posição atual (volta): {posicao_atual}")
            self.visitados_volta.add(posicao_atual)
            
            self.mqtt_publisher.enviar_metricas(
                "Retornando",
                self.mqtt_publisher.calcular_velocidade(),
                posicao_atual,
                chegou=False
            )

            if posicao_atual == "DGA":
                self.ajustar_motores(2500, 1000, 1)
                self.ajustar_motores(2500, 2500)
                
            elif posicao_atual == "DGB":
                self.ajustar_motores(1000, 2500, 1)
                self.ajustar_motores(2500, 2500)

            elif posicao_atual == "ITA":
                self.ajustar_motores(2500, 1000, 0.5)
                self.ajustar_motores(2500, 2500)

            elif posicao_atual == "ITB":
                self.ajustar_motores(1000, 2500, 0.5)
                self.ajustar_motores(2500, 2500)

            elif posicao_atual == "ITM":
                self.ajustar_motores(1000, 2500, 0.5)
                self.ajustar_motores(2500, 2500)

            elif posicao_atual == "CRG":
                print("Retorno ao ponto inicial CRG.")
                self.motor_direito.parar()
                self.motor_esquerdo.parar()
                self.mqtt_publisher.enviar_metricas(
                    "Retorno completo",
                    0,
                    posicao_atual,
                    chegou=True
                )
                self.caminho_retorno = False
                return

            else:
                self.parar_para_ajuste()

    def ajustar_motores(self, vel_motor_esquerdo, vel_motor_direito, duracao=None):
        if self.executando:
            self.motor_esquerdo.controlar(vel_motor_esquerdo)
            self.motor_direito.controlar(vel_motor_direito)
            if duracao:
                time.sleep(duracao)
                if self.executando:
                    self.motor_direito.controlar(2500)
                    self.motor_esquerdo.controlar(2500)

    def parar_para_ajuste(self):
        self.motor_direito.parar()
        self.motor_esquerdo.parar()
        time.sleep(1)

    def alcancar_destino(self):
        print(f"Destino {self.destino} alcançado!")        
        self.mqtt_publisher.enviar_metricas(
            "Destino alcançado",
            0, 
            self.destino, 
            chegou=True 
        )
        
        self.motor_direito.controlar(1000)
        self.motor_esquerdo.controlar(2500)
        time.sleep(1)
        self.motor_direito.controlar(1500)
        self.motor_esquerdo.controlar(1500)
        time.sleep(5)
        self.caminho_retorno = True

    def finalizar(self):
        self.executando = False
        self.motor_direito.parar()
        self.motor_esquerdo.parar()
        self.led_controller.finalizar()
        self.sensor.cleanup()
        self.mqtt_publisher.parar_timer()
        self.pi.stop()
        GPIO.cleanup()