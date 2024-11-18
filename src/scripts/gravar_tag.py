import time
import json
import RPi.GPIO as GPIO
import mfrc522 as MFRC522

LeitorRFID = MFRC522.MFRC522()

ARQUIVO_JSON = 'tags_rfid.json'

def ler_uid():
    status, tag_type = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)
    if status == LeitorRFID.MI_OK:
        print('Cartão detectado!')
        status, uid = LeitorRFID.MFRC522_Anticoll()
        if status == LeitorRFID.MI_OK:
            return ':'.join(['%X' % x for x in uid])
    return None

def salvar_dados(uid, nome):
    try:
        with open(ARQUIVO_JSON, 'r') as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {}

    dados[uid] = nome

    with open(ARQUIVO_JSON, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)
    print(f"Dados salvos com sucesso: UID={uid}, Nome = {nome}")

try:
    print("Aproxime uma tag RFID para registro.")
    while True:
        uid = ler_uid()
        if uid:
            print(f"UID da tag: {uid}")
            nome = input("Digite um nome para essa tag: ")
            salvar_dados(uid, nome)
            print("Aproxime outra tag RFID ou pressione Ctrl+C para encerrar.")
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nPrograma encerrado.")
