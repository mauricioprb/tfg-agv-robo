class AGVOperationManager:
    def __init__(self, agv_controller, mqtt_metrics_publisher, mqtt_client):
        self.agv_controller = agv_controller
        self.mqtt_metrics_publisher = mqtt_metrics_publisher
        self.mqtt_client = mqtt_client
        self.pronto_para_novo_destino = True

    def iniciar_movimento_agv(self, destino):
        if not self.pronto_para_novo_destino:
            print("AGV ainda não está pronto para um novo destino.")
            return

        try:
            print(f"Destino recebido: {destino}")
            self.agv_controller.definir_rota(destino)
            self.pronto_para_novo_destino = False

            # Log para depuração antes de enviar métricas
            print("Iniciando o envio do status 'Em operação' para agv/metricas.")

            # Enviar status "Em operação" ao iniciar o percurso
            self.mqtt_metrics_publisher.enviar_metricas()

            # Iniciar o movimento do AGV
            print("Movimento do AGV iniciado.")
            self.agv_controller.movimentar_agv()

        except ValueError as e:
            print(f"Erro ao definir rota: {e}")
            self.pronto_para_novo_destino = True

        if self.agv_controller.ponto_atual == "ponto_inicial":
            print("AGV retornou ao ponto inicial.")
            self.pronto_para_novo_destino = True
            print("AGV pronto para novo destino.")

    def iniciar(self):
        self.mqtt_client.registrar_topico(
            "transporte/iniciar",
            lambda destino: self.iniciar_movimento_agv(destino)
        )
        self.mqtt_client.iniciar()
