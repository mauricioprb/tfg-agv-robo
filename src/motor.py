import pigpio
import time

class Motor:
    def __init__(self, pi, pino_gpio, frequencia=50, pulso_neutro=1500, pulso_maximo=2500, pulso_minimo=1000):
        self.pi = pi
        self.pino_gpio = pino_gpio
        self.frequencia = frequencia
        self.pulso_neutro = pulso_neutro
        self.pulso_maximo = pulso_maximo
        self.pulso_minimo = pulso_minimo
        
        self.pi.set_mode(self.pino_gpio, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.pino_gpio, self.frequencia)
        self.inicializar()

    def inicializar(self):
        # Inicializa o ESC com o pulso neutro.
        self.pi.set_servo_pulsewidth(self.pino_gpio, self.pulso_neutro)
        time.sleep(1)

    def controlar(self, pulso):
        # Define o pulso do motor para controlar a velocidade.
        if self.pulso_minimo <= pulso <= self.pulso_maximo:
            self.pi.set_servo_pulsewidth(self.pino_gpio, pulso)
        else:
            raise ValueError(f"Pulso fora do intervalo permitido: {pulso}")

    def parar(self):
        # Para o motor
        self.pi.set_servo_pulsewidth(self.pino_gpio, 0)