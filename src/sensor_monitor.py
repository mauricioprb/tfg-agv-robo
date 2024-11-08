import RPi.GPIO as GPIO
import time

class SensorMonitor:
    def __init__(self, pinos_sensor, pino_alimentacao=11, intervalo=1):
        self.pinos_sensor = pinos_sensor
        self.pino_alimentacao = pino_alimentacao
        self.intervalo = intervalo

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.pino_alimentacao, GPIO.OUT)
        GPIO.output(self.pino_alimentacao, GPIO.HIGH)

    def configurar_saida(self):
        for pino in self.pinos_sensor:
            GPIO.setup(pino, GPIO.OUT)
            GPIO.output(pino, GPIO.HIGH)

    def configurar_entrada(self):
        for pino in self.pinos_sensor:
            GPIO.setup(pino, GPIO.IN)

    def monitorar(self):
        print("Monitorando o sensor...")

        try:
            while True:
                self.configurar_saida()
                time.sleep(0.5)

                self.configurar_entrada()

                valores = []
                for pino in self.pinos_sensor:
                    count = 0
                    while GPIO.input(pino) == GPIO.HIGH and count < 250:
                        count += 1
                    valores.append(count)

                print("Valores do sensor:", valores)

                time.sleep(self.intervalo)

        except KeyboardInterrupt:
            print("Monitoramento interrompido.")

        finally:
            GPIO.output(self.pino_alimentacao, GPIO.LOW)
            GPIO.cleanup()
            print("GPIO cleanup.")
