import threading
import time

class AGVOperationManager:
    def __init__(self, agv_controller, mqtt_metrics_publisher, mqtt_client):
        self.agv_controller = agv_controller
        self.mqtt_metrics_publisher = mqtt_metrics_publisher
        self.mqtt_client = mqtt_client
        self.pronto_para_novo_destino = True
        self.monitorando_operacao = False
        self.executando = True 
        
    def parar_agv(self, mensagem):
        """
        Callback para o comando de parada via MQTT
        """
        if mensagem == "Parar":
            print("Comando de parada recebido")
            self.executando = False
            self.agv_controller.parar_movimento()
            self.monitorando_operacao = False
            self.mqtt_metrics_publisher.enviar_metricas(
                "Parado por comando",
                0,
                self.agv_controller.current_position,
                chegou=False
            )

    def monitorar_operacao(self):
        self.monitorando_operacao = True
        while self.monitorando_operacao:
            try:
                status_operacao = "Em operação"
                velocidade = self.agv_controller.simular_velocidade()
                print(f"Monitorando operação: Status = {status_operacao}, Velocidade = {velocidade:.2f} m/s")
                self.mqtt_metrics_publisher.enviar_metricas(status_operacao, velocidade)
                time.sleep(1)
            except Exception as e:
                print(f"Erro no monitoramento da operação: {e}")
                self.monitorando_operacao = False

    def iniciar_movimento_agv(self, destino):
        if not self.pronto_para_novo_destino:
            print("AGV ainda não está pronto para um novo destino.")
            return

        try:
            print(f"Destino recebido: {destino}")
            self.agv_controller.definir_rota(destino)
            self.pronto_para_novo_destino = False
            self.executando = True 

            thread_monitoramento = threading.Thread(target=self.monitorar_operacao, daemon=True)
            thread_monitoramento.start()

            print("Movimento do AGV iniciado.")
            self.agv_controller.movimentar_agv(self) 

        except ValueError as e:
            print(f"Erro ao definir rota: {e}")
            self.pronto_para_novo_destino = True

        if self.agv_controller.ponto_atual == "ponto_inicial":
            print("AGV retornou ao ponto inicial.")
            self.monitorando_operacao = False
            self.pronto_para_novo_destino = True
            print("AGV pronto para novo destino.")

    def iniciar(self):
        self.mqtt_client.registrar_topico(
            "transporte/iniciar",
            lambda destino: self.iniciar_movimento_agv(destino)
        )
        self.mqtt_client.registrar_topico(
            "agv/parar",
            self.parar_agv
        )
        self.mqtt_client.iniciar()