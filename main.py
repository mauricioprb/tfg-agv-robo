from controle_motores import ControleMotores

if __name__ == "__main__":
    controle = ControleMotores(motor_direito_gpio=12, motor_esquerdo_gpio=13)
    controle.executar_movimento()
