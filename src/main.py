from controle_motores import ControleMotores
from sensor_monitor import SensorMonitor

if __name__ == "__main__":
    controle = ControleMotores(motor_direito_gpio=12, motor_esquerdo_gpio=13)
    pinos_sensor = [4, 17, 27, 22, 5, 6, 13, 19]
    monitor = SensorMonitor(pinos_sensor, intervalo=1)
    pista = [sign(i) for i in monitor.monitorar()]

    index = pista.find(1)
    quantidade = pista.count(1)
    movimento = {
        (3, 2):(2500, 2500)
    }

    try:
        velocidades = movimento[(index, quantidade)]

    except:
        velocidades = (0, 0)
    controle.executar_movimento(velocidades[0], velocidades[1])
