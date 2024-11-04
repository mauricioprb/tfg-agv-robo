from controle_motores import ControleMotores
from sensor_monitor import SensorMonitor

if __name__ == "__main__":
    # controle = ControleMotores(motor_direito_gpio=12, motor_esquerdo_gpio=13)
    # controle.executar_movimento()
    pinos_sensor = [4, 17, 27, 22, 5, 6, 13, 19]
    monitor = SensorMonitor(pinos_sensor, intervalo=1)

    monitor.monitorar()
