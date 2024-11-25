import RPi.GPIO as GPIO
import time
import threading

class LEDController:
    def __init__(self, pino_vermelho=22, pino_verde=23, pino_azul=24):
        self.pino_vermelho = pino_vermelho
        self.pino_verde = pino_verde
        self.pino_azul = pino_azul
        self.piscar = False 
        self.thread_piscada = None 

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pino_vermelho, GPIO.OUT)
        GPIO.setup(self.pino_verde, GPIO.OUT)
        GPIO.setup(self.pino_azul, GPIO.OUT)

    def acender_verde(self):
        self.parar_piscada() 
        GPIO.output(self.pino_vermelho, GPIO.HIGH)
        GPIO.output(self.pino_verde, GPIO.LOW)
        GPIO.output(self.pino_azul, GPIO.HIGH)
        print("LED verde aceso.")

    def desligar_leds(self):
        GPIO.output(self.pino_vermelho, GPIO.LOW)
        GPIO.output(self.pino_verde, GPIO.LOW)
        GPIO.output(self.pino_azul, GPIO.LOW)
        print("LEDs desligados.")

    def piscada_rapida_verde(self):
        self.piscar = True
        if self.thread_piscada is None or not self.thread_piscada.is_alive():
            self.thread_piscada = threading.Thread(target=self._piscar_led)
            self.thread_piscada.start()

    def _piscar_led(self):
        while self.piscar:
            GPIO.output(self.pino_verde, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(self.pino_verde, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(self.pino_verde, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(self.pino_verde, GPIO.LOW)
            time.sleep(0.5)

    def parar_piscada(self):
        """Para a piscada do LED."""
        self.piscar = False
        if self.thread_piscada:
            self.thread_piscada.join() 
        self.desligar_leds()

    def finalizar(self):
        self.parar_piscada()
        GPIO.cleanup()
        print("GPIO limpo e LEDs desligados.")

if __name__ == "__main__":
    led_controller = LEDController()

    try:
        led_controller.acender_verde()
        input("Pressione Enter para encerrar...")  # Mantém o programa rodando até o usuário encerrar
    finally:
        led_controller.finalizar()