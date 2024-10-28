from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

try:
    print("Aproxime a tag RFID...")
    id = reader.read_id()
    print(f"ID da Tag: {id}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    GPIO.cleanup()