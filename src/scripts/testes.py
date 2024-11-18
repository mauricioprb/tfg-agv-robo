import time
import pigpio
import RPi.GPIO as GPIO
from motor import Motor

# Inicialização dos motores
pi = pigpio.pi()
motor_esquerdo = Motor(pi, pino_gpio=12)
motor_direito = Motor(pi, pino_gpio=13)

def executar_sequencia():
    try:
        print("Movendo para frente por 3 segundos...")
        motor_direito.controlar(2500)
        motor_esquerdo.controlar(2500)
        time.sleep(1.7)
        
        print("Virando à direita por 0.5 segundos...")
        motor_direito.controlar(1000)
        motor_esquerdo.controlar(1600)
        time.sleep(0.42)
        
        # print("Movendo para frente por 2 segundos...")
        # motor_direito.controlar(2500)
        # motor_esquerdo.controlar(2500)
        # time.sleep(2)
        
        # print("Virando à esquerda por 0.5 segundos...")
        # motor_direito.controlar(2500)
        # motor_esquerdo.controlar(1500)
        # time.sleep(0.5)
        
        # print("Movendo para frente por 2 segundos...")
        # motor_direito.controlar(2500)
        # motor_esquerdo.controlar(2500)
        # time.sleep(2)
        
        # print("Virando à direita por 0.9 segundos...")
        # motor_direito.controlar(1500)
        # motor_esquerdo.controlar(2500)
        # time.sleep(0.9)
        
        # print("Parando os motores...")
        # motor_direito.parar()
        # motor_esquerdo.parar()
    
    finally:
        motor_direito.parar()
        motor_esquerdo.parar()
        pi.stop()
        GPIO.cleanup()
        print("\nSequência de movimentos concluída.")

# Executar a sequência de movimentos
executar_sequencia()
