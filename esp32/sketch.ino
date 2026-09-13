#include <WiFi.h>
#include <PubSubClient.h>

// =========================
// CONFIGURAÇÕES DO PET
// =========================
const int ID_PET = 104;

// =========================
// WIFI - WOKWI
// =========================
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";

// =========================
// MQTT - HIVEMQ
// =========================
const char* MQTT_BROKER = "broker.hivemq.com";
const int MQTT_PORT = 1883;

// Tópicos MQTT
String topicTemperatura = "pet/" + String(ID_PET) + "/temperatura";
String topicAtividade = "pet/" + String(ID_PET) + "/atividade";

// =========================
// CLIENTES
// =========================
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// =========================
// CONTROLE DE TEMPO
// =========================
unsigned long ultimoEnvio = 0;
const unsigned long INTERVALO_ENVIO = 3000;

// =========================
// CONECTAR AO WIFI
// =========================
void conectarWiFi() {
  Serial.print("Conectando ao WiFi");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

// =========================
// CONECTAR AO MQTT
// =========================
void conectarMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Conectando ao MQTT... ");

    String clientId = "esp32-pet-" + String(ID_PET) + "-";
    clientId += String(random(0xffff), HEX);

    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("conectado!");
    } else {
      Serial.print("falhou, estado = ");
      Serial.println(mqttClient.state());

      Serial.println("Tentando novamente em 2 segundos...");
      delay(2000);
    }
  }
}

// =========================
// PUBLICAR DADOS
// =========================
void publicarDados() {

  // Simulação de temperatura entre 30.0 e 45.0 °C
  float temperatura = random(300, 451) / 10.0;

  // Simulação de atividade entre 0 e 500
  int atividade = random(0, 501);

  String temperaturaStr = String(temperatura, 1);
  String atividadeStr = String(atividade);

  mqttClient.publish(
    topicTemperatura.c_str(),
    temperaturaStr.c_str()
  );

  mqttClient.publish(
    topicAtividade.c_str(),
    atividadeStr.c_str()
  );

  Serial.println("================================");

  Serial.print("PET: ");
  Serial.println(ID_PET);

  Serial.print("Tópico temperatura: ");
  Serial.println(topicTemperatura);

  Serial.print("Temperatura: ");
  Serial.print(temperaturaStr);
  Serial.println(" °C");

  Serial.print("Tópico atividade: ");
  Serial.println(topicAtividade);

  Serial.print("Atividade: ");
  Serial.println(atividadeStr);

  Serial.println("Dados publicados no MQTT!");

  Serial.println("================================");
}

// =========================
// SETUP
// =========================
void setup() {

  Serial.begin(115200);

  randomSeed(micros());

  conectarWiFi();

  mqttClient.setServer(
    MQTT_BROKER,
    MQTT_PORT
  );

  conectarMQTT();

  Serial.println();

  Serial.println(
    "Sistema IoT veterinário iniciado."
  );

  Serial.print("PET monitorado: ");
  Serial.println(ID_PET);

  Serial.print("Temperatura -> ");
  Serial.println(topicTemperatura);

  Serial.print("Atividade -> ");
  Serial.println(topicAtividade);
}

// =========================
// LOOP
// =========================
void loop() {

  if (WiFi.status() != WL_CONNECTED) {
    conectarWiFi();
  }

  if (!mqttClient.connected()) {
    conectarMQTT();
  }

  mqttClient.loop();

  unsigned long agora = millis();

  if (agora - ultimoEnvio >= INTERVALO_ENVIO) {

    ultimoEnvio = agora;

    publicarDados();
  }
}
