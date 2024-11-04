import time
import pigpio
from motor import Motor

class ControleMotores:
    def __init__(self, motor_direito_gpio, motor_esquerdo_gpio):
        self.pi = pigpio.pi()
        self.motor_direito = Motor(self.pi, motor_direito_gpio)
        self.motor_esquerdo = Motor(self.pi, motor_esquerdo_gpio)

    def executar_movimento(self):
        # Controla os motores para realizar um movimento.
        try:
            while True:
                self.motor_direito.controlar(self.motor_direito.pulso_maximo)
                self.motor_esquerdo.controlar(self.motor_esquerdo.pulso_maximo)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Movimento interrompido pelo usuário.")
        finally:
            self.parar()
            self.pi.stop()

    def parar(self):
        # Para ambos os motores
        self.motor_direito.parar()
        self.motor_esquerdo.parar()
