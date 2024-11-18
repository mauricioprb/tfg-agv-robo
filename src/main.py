import time
import pigpio
import RPi.GPIO as GPIO
import mfrc522 as MFRC522
from agv_controller import AGVController
from mqtt_metrics_publisher import MqttMetricsPublisher
from mqtt_client import MQTTClient
from led_controller import LEDController
from agv_operation_manager import AGVOperationManager
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    pi = pigpio.pi()
    leitor_rfid = MFRC522.MFRC522()
    led_controller = LEDController()
    led_controller.acender_verde()

    agv_controller = AGVController(leitor_rfid, pi, pino_motor_esquerdo=12, pino_motor_direito=13)

    broker_url = os.getenv("MQTT_BROKER_URL")
    broker_port = int(os.getenv("MQTT_BROKER_PORT"))
    username = os.getenv("MQTT_USERNAME")
    password = os.getenv("MQTT_PASSWORD")

    mqtt_client = MQTTClient(broker_url, broker_port, username, password)
    mqtt_metrics_publisher = MqttMetricsPublisher(mqtt_client)
    
    mqtt_client.set_on_connect_callback(mqtt_metrics_publisher.enviar_status_ligado)
    
    agv_operation_manager = AGVOperationManager(agv_controller, mqtt_metrics_publisher, mqtt_client)

    try:
        mqtt_client.iniciar()
        agv_operation_manager.iniciar()
        print("Aguardando comandos...")

        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Encerrando o programa")

    finally:
        mqtt_client.finalizar()
        agv_controller.finalizar()
        print("\nPrograma encerrado")
