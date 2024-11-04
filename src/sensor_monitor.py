import RPi.GPIO as GPIO
import time

class SensorMonitor:
    def __init__(self, pinos_sensor, intervalo=1):
        self.pinos_sensor = pinos_sensor
        self.intervalo = intervalo
        GPIO.setmode(GPIO.BCM)
        
        for pino in self.pinos_sensor:
            GPIO.setup(pino, GPIO.IN)
    
    def monitorar(self):
        print("Monitorando o sensor...")
        
        try:
            while True:
                valores = [GPIO.input(pino) for pino in self.pinos_sensor]
                print("Valores do sensor:", valores)
                
                time.sleep(self.intervalo)

        except KeyboardInterrupt:
            print("Monitoramento interrompido.")

        finally:
            GPIO.cleanup()
            print("GPIO cleanup.")