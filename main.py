import pigpio
import time

pi = pigpio.pi()

MOTOR_DIREITO_GPIO = 12  
MOTOR_ESQUERDO_GPIO = 13

PWM_FREQUENCIA = 50       
PULSO_NEUTRO = 1500       
PULSO_MAXIMO = 2500       
PULSO_MINIMO = 1000        

def configurar_esc(pino_gpio):
    pi.set_mode(pino_gpio, pigpio.OUTPUT)               
    pi.set_PWM_frequency(pino_gpio, PWM_FREQUENCIA)      

def inicializar_esc(pino_gpio):
    pi.set_servo_pulsewidth(pino_gpio, PULSO_NEUTRO)     
    time.sleep(1)                                        

def configurar_motores():
    configurar_esc(MOTOR_DIREITO_GPIO)
    configurar_esc(MOTOR_ESQUERDO_GPIO)
    inicializar_esc(MOTOR_DIREITO_GPIO)
    inicializar_esc(MOTOR_ESQUERDO_GPIO)

def controlar_motor(pino_gpio, pulso):
    pi.set_servo_pulsewidth(pino_gpio, pulso)

def executar_movimento():
    configurar_motores()
    
    try:
        while True:
            controlar_motor(MOTOR_DIREITO_GPIO, PULSO_MAXIMO)  
            controlar_motor(MOTOR_ESQUERDO_GPIO, PULSO_MAXIMO)
            time.sleep(0.1) 

    except KeyboardInterrupt:
        print("Movimento interrompido pelo usuário.")

    finally:
        controlar_motor(MOTOR_DIREITO_GPIO, 0)
        controlar_motor(MOTOR_ESQUERDO_GPIO, 0)
        pi.stop()

if __name__ == "__main__":
    executar_movimento()
