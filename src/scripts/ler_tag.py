import time
import json
import RPi.GPIO as GPIO
import mfrc522 as MFRC522

LeitorRFID = MFRC522.MFRC522()

ARQUIVO_JSON = 'tags_rfid.json'

def carregar_dados():
    try:
        with open(ARQUIVO_JSON, 'r') as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {}
    return dados

def ler_uid():
    status, tag_type = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)
    if status == LeitorRFID.MI_OK:
        print('Cartão detectado!')
        status, uid = LeitorRFID.MFRC522_Anticoll()
        if status == LeitorRFID.MI_OK:
            return ':'.join(['%X' % x for x in uid])
    return None

def verificar_tag(uid, dados):
    if uid in dados:
        print(f"UID: {uid} - Nome: {dados[uid]}")
    else:
        print(f"UID {uid} não registrado.")

try:
    print("Aproxime uma tag RFID para leitura.")
    dados_registrados = carregar_dados()

    while True:
        uid = ler_uid()
        if uid:
            verificar_tag(uid, dados_registrados)
            print("Aproxime outra tag RFID.")
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nPrograma encerrado.")
