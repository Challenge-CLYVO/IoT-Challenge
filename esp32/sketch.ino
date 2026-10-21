
#include <WiFi.h>
#include <PubSubClient.h>

// =========================
// CONFIGURACOES DO PET
// =========================
const int ID_PET = 104;

// =========================
// WIFI - WOKWI
// =========================
const char *WIFI_SSID = "Wokwi-GUEST";
const char *WIFI_PASSWORD = "";

// =========================
// MQTT - HIVEMQ
// =========================
const char *MQTT_BROKER = "broker.hivemq.com";
const int MQTT_PORT = 1883;

// Topicos MQTT
String topicTemperatura = "pet/" + String(ID_PET) + "/temperatura";
String topicAtividade = "pet/" + String(ID_PET) + "/atividade";

// Clientes
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// Intervalo de envio
unsigned long ultimoEnvio = 0;
const unsigned long INTERVALO_ENVIO = 3000;

// =========================
// CONECTAR AO WIFI
// =========================
void conectarWiFi()
{
  if (WiFi.status() == WL_CONNECTED)
  {
    return;
  }

  Serial.print("Conectando ao WiFi...");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long inicio = millis();

  while (WiFi.status() != WL_CONNECTED &&
         millis() - inicio < 20000)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED)
  {
    Serial.println("WiFi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  }
  else
  {
    Serial.println(
        "ERRO: falha no WiFi. Tentaremos novamente.");
  }
}

// =========================
// CONECTAR AO MQTT
// =========================
void conectarMQTT()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    return;
  }

  while (!mqttClient.connected())
  {
    Serial.print("Conectando ao MQTT... ");

    String clientId = "esp32-pet-" + String(ID_PET) + "-";
    clientId += String((uint32_t)ESP.getEfuseMac(), HEX);
    clientId += "-";
    clientId += String(random(0xffff), HEX);

    if (mqttClient.connect(clientId.c_str()))
    {
      Serial.println("CONECTADO!");

      Serial.print("Client ID: ");
      Serial.println(clientId);
    }
    else
    {
      Serial.print("FALHOU. Estado MQTT: ");
      Serial.println(mqttClient.state());

      Serial.println("Nova tentativa em 3 segundos...");
      delay(3000);

      if (WiFi.status() != WL_CONNECTED)
      {
        return;
      }
    }
  }
}

// =========================
// PUBLICAR DADOS
// =========================
void publicarDados()
{
  if (!mqttClient.connected())
  {
    Serial.println(
        "ERRO: MQTT desconectado. Dados nao publicados.");
    return;
  }

  // Valores simulados para demonstracao.
  // Nao representam medidas clinicas reais.
  float temperatura = random(300, 451) / 10.0;
  int atividade = random(0, 501);

  String temperaturaStr = String(temperatura, 1);
  String atividadeStr = String(atividade);

  bool temperaturaOK = mqttClient.publish(
      topicTemperatura.c_str(),
      temperaturaStr.c_str());

  bool atividadeOK = mqttClient.publish(
      topicAtividade.c_str(),
      atividadeStr.c_str());

  Serial.println("========================================");

  Serial.print("Pet ID: ");
  Serial.println(ID_PET);

  Serial.print("Topico temperatura: ");
  Serial.println(topicTemperatura);

  Serial.print("Temperatura: ");
  Serial.print(temperaturaStr);
  Serial.println(" C");

  Serial.print("Publicacao temperatura: ");
  Serial.println(temperaturaOK ? "OK" : "FALHOU");

  Serial.print("Topico atividade: ");
  Serial.println(topicAtividade);

  Serial.print("Atividade: ");
  Serial.println(atividadeStr);

  Serial.print("Publicacao atividade: ");
  Serial.println(atividadeOK ? "OK" : "FALHOU");

  if (temperaturaOK && atividadeOK)
  {
    Serial.println(
        "As duas chamadas publish() foram aceitas.");
  }
  else
  {
    Serial.println(
        "ATENCAO: verifique a conexao MQTT.");
  }

  Serial.println("========================================");
}

// =========================
// SETUP
// =========================
void setup()
{
  Serial.begin(115200);
  delay(100);

  randomSeed(micros());

  mqttClient.setServer(
      MQTT_BROKER,
      MQTT_PORT);

  mqttClient.setKeepAlive(60);
  mqttClient.setSocketTimeout(10);

  Serial.println();
  Serial.println("Iniciando monitoramento IoT do pet...");

  Serial.print("Broker: ");
  Serial.print(MQTT_BROKER);
  Serial.print(":");
  Serial.println(MQTT_PORT);

  Serial.print("Topico temperatura: ");
  Serial.println(topicTemperatura);

  Serial.print("Topico atividade: ");
  Serial.println(topicAtividade);

  conectarWiFi();
  conectarMQTT();
}

// =========================
// LOOP
// =========================
void loop()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    conectarWiFi();
  }

  if (WiFi.status() == WL_CONNECTED &&
      !mqttClient.connected())
  {
    conectarMQTT();
  }

  mqttClient.loop();

  unsigned long agora = millis();

  if (agora - ultimoEnvio >= INTERVALO_ENVIO)
  {
    ultimoEnvio = agora;
    publicarDados();
  }
}
