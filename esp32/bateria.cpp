#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

const char* ssid = "SSID";
const char* senhaWiFi = "SENHA";

const char* mqttServer = "BROKER";
const int mqttPort = 0000;
const char* mqttUser = "USER";
const char* mqttPassword = "SENHA";

const int led = 8;
const int sensor = 1;
WiFiClientSecure clienteWiFi;
PubSubClient mqttClient(clienteWiFi);
unsigned long tempoAnterior = 0;
const long intervalo = 1000;

void configurarWiFi() {
  WiFi.begin(ssid, senhaWiFi);
  Serial.println("Tentando conectar ao WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado ao WiFi");
}

void conectarMQTT() {
  clienteWiFi.setInsecure();
  mqttClient.setServer(mqttServer, mqttPort);
  Serial.println("Conectando ao MQTT...");

  if (mqttClient.connect("ESP32Client", mqttUser, mqttPassword)) {
    Serial.println("Conectado ao Broker MQTT");
  } else {
    Serial.println("Falha ao conectar ao MQTT, rc=");
    Serial.println(mqttClient.state());
  }
}

void reconectarMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Tentando reconectar ao MQTT...");
    if (mqttClient.connect("ESP32Client", mqttUser, mqttPassword)) {
      Serial.println("Conectado ao Broker MQTT");
    } else {
      Serial.println("Falha na reconexão ao MQTT, rc=");
      Serial.println(mqttClient.state());
      delay(5000);
    }
  }
}

void publicarDadosBateria() {
  int valorBateriaCru = analogRead(sensor);
  char mensagem[50];
  snprintf(mensagem, sizeof(mensagem), "{\"bateria\": %d}", valorBateriaCru);

  if (mqttClient.connected()) {
    mqttClient.publish("esp32/bateria", mensagem);
  }
}

void piscarLED() {
  unsigned long tempoAtual = millis();
  if (tempoAtual - tempoAnterior >= intervalo) {
    tempoAnterior = tempoAtual;
    digitalWrite(led, !digitalRead(led));
  }
}

void setup() {
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  Serial.begin(115200);

  configurarWiFi();
  digitalWrite(led, HIGH);
  conectarMQTT();
}

void loop() {
  if (!mqttClient.connected()) {
    reconectarMQTT();
  }

  publicarDadosBateria();
  piscarLED();

  mqttClient.loop();
  delay(5000);
}
