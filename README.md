# 🚀 IoT Pet Monitoramento Inteligente — ESP32, MQTT, Node-RED e IA

## 📌 Descrição do Projeto

O IoT Pet Monitoramento Inteligente é um projeto acadêmico que utiliza conceitos de Internet das Coisas (IoT) para monitorar dados simulados de pets.

O sistema utiliza um ESP32 simulado no Wokwi para gerar leituras de temperatura e atividade. Os dados são transmitidos por MQTT, recebidos e processados pelo Node-RED, exibidos em um dashboard e armazenados em um banco de dados MySQL.

Na Fase 1, o projeto também conta com um protótipo de análise estatística para identificar possíveis anomalias nas leituras.

> **Importante:** os dados são simulados e o protótipo de IA é experimental. Os resultados não constituem diagnóstico veterinário.

## 🎯 Objetivos

- Monitorar dados simulados de temperatura e atividade dos pets.
- Transmitir leituras utilizando o protocolo MQTT.
- Processar mensagens com o Node-RED.
- Exibir informações em um dashboard.
- Armazenar leituras e registros de saúde no MySQL.
- Preparar dados para análise estatística.
- Identificar possíveis valores atípicos com um protótipo de detecção de anomalias.
- Validar o modelo com testes automatizados.

## 🧱 Arquitetura da Solução

```text
ESP32 simulado no Wokwi
          |
          v
Broker MQTT — HiveMQ
          |
          v
       Node-RED
          |
          +------> Dashboard em tempo real
          |
          +------> MySQL
          |          |
          |          v
          |     Leituras armazenadas
          |          |
          v          v
     Preparação dos dados
               |
               v
       Protótipo de IA
               |
               v
     Possíveis anomalias
```

O protótipo de IA analisa arquivos CSV preparados a partir de leituras. A integração automática do modelo com o banco de dados deve ser considerada separadamente, caso ainda não esteja implementada.

## 🛠️ Tecnologias Utilizadas

- **ESP32 / Wokwi:** simulação do dispositivo.
- **Arduino / C++:** programação do ESP32.
- **MQTT:** comunicação entre o dispositivo e o sistema.
- **HiveMQ Public Broker:** broker MQTT público.
- **Node-RED:** recepção e processamento das mensagens.
- **Node-RED Dashboard:** visualização dos dados.
- **MySQL / XAMPP:** armazenamento das leituras.
- **Python:** análise estatística e testes automatizados.
- **unittest:** execução dos testes do protótipo.

## 🔌 Dados Monitorados

O ESP32 utiliza o identificador de pet `104` e gera valores simulados de:

- **Temperatura:** valores entre 30 °C e 45 °C.
- **Atividade:** valores entre 0 e 500, conforme a simulação implementada.

Os valores são utilizados para demonstrar a comunicação, o processamento, o armazenamento e a análise dos dados.

## 📡 Comunicação MQTT

Broker configurado:

```text
broker.hivemq.com
Porta: 1883
```

Tópicos publicados pelo ESP32:

```text
pet/104/temperatura
pet/104/atividade
```

Assinaturas utilizadas no Node-RED:

```text
pet/+/temperatura
pet/+/atividade
```

O caractere `+` permite receber mensagens de diferentes identificadores de pet no mesmo nível do tópico.

O broker é público. Não envie informações pessoais ou dados sensíveis por meio dele.

## 🗄️ Banco de Dados MySQL

O banco utilizado pelo projeto é `iot_pet`.

O script `sql/commands.sql` prepara as tabelas de armazenamento das leituras e dos registros de saúde.

### Tabela `pet_saude`

Armazena registros de saúde processados pelo fluxo, com descrição, status e data de registro.

### Tabela `leituras_pet`

Armazena leituras numéricas associadas ao pet, incluindo tipo, valor e data de registro.

### Consulta de verificação

Depois de configurar o banco e executar o fluxo, consulte as últimas leituras:

```sql
USE iot_pet;

SELECT id, pet_id, tipo, valor, data_registro
FROM leituras_pet
ORDER BY id DESC
LIMIT 20;
```

Para consultar os registros de saúde:

```sql
SELECT id, descricao, status, data_registro
FROM pet_saude
ORDER BY id DESC
LIMIT 20;
```

A estrutura efetiva das tabelas deve corresponder ao script `sql/commands.sql` do projeto.

## ⚙️ Como Executar o Projeto

### 1. Preparar o banco de dados

1. Inicie o MySQL pelo XAMPP ou pelo ambiente configurado.
2. Abra o cliente SQL ou phpMyAdmin.
3. Execute o script `sql/commands.sql`.
4. Confirme a existência do banco `iot_pet` e das tabelas necessárias.

### 2. Iniciar o Node-RED

No terminal, execute:

```powershell
node-red
```

Acesse o editor:

http://localhost:1880

### 3. Importar o fluxo

1. Abra o editor Node-RED.
2. Acesse o menu de importação.
3. Importe `node-red/flows.json`.
4. Confira as configurações MQTT e MySQL.
5. Clique em **Deploy**.

### 4. Executar a simulação ESP32

1. Abra o projeto ESP32 no Wokwi.
2. Confira a configuração de Wi-Fi `Wokwi-GUEST`.
3. Verifique o endereço do broker e os tópicos MQTT.
4. Inicie a simulação.
5. Confira se as mensagens estão sendo publicadas.

### 5. Visualizar o dashboard

Acesse:

http://localhost:1880/ui

Confira a exibição das leituras e o comportamento dos componentes configurados no fluxo.

### 6. Verificar o armazenamento

Consulte as tabelas `leituras_pet` e `pet_saude` no MySQL para confirmar se o fluxo está registrando os dados.

## 🧠 Protótipo de IA — Detecção de Anomalias

O diretório `ia/` contém um protótipo Python para analisar leituras preparadas em CSV e sinalizar valores estatisticamente atípicos.

O algoritmo agrupa os dados por identificador do pet e tipo de leitura. Quando há amostras suficientes, utiliza a mediana e o desvio absoluto mediano (MAD) para identificar valores que se afastam do comportamento observado no grupo.

### Funcionalidades

- Leitura de arquivos CSV.
- Validação das colunas obrigatórias.
- Separação dos dados por pet e tipo.
- Identificação estatística de valores atípicos.
- Geração de CSV com a classificação e o motivo.

### Colunas obrigatórias do CSV

```text
pet_id
tipo
valor
data_registro
```

### Executar o protótipo

Na raiz do projeto:

```powershell
python .\ia\modelo_anomalias.py .\ia\dados\leituras.csv -o .\ia\dados\resultado_anomalias.csv
```

O resultado será salvo em `ia/dados/resultado_anomalias.csv`.

### Resultado demonstrativo validado

No teste com cinco leituras simuladas de temperatura — `30`, `31`, `30`, `32` e `100` — o modelo analisou cinco registros e sinalizou um possível valor atípico: `100`.

Esse resultado demonstra o funcionamento do protótipo no cenário de teste, mas não representa uma avaliação clínica.

Mais informações estão disponíveis em `ia/README.md` e `ia/dados/README.md`.

## 🧪 Testes Automatizados

O arquivo de testes está em:

```text
ia/tests/test_modelo_anomalias.py
```

O protótipo possui cinco testes automatizados para verificar:

1. Identificação de um valor atípico.
2. Tratamento de amostras insuficientes.
3. Separação das leituras por pet e tipo.
4. Rejeição de valores inválidos.
5. Validação das colunas obrigatórias.

### Executar os testes

Na raiz do projeto:

```powershell
python -m unittest discover -s ia/tests -p "test_*.py" -v
```

**Resultado já obtido:** cinco testes executados, sem falhas (`OK`).

O plano de testes manuais e o registro dos resultados estão em `docs/TESTES_FASE1.md`.

## 📋 Validação Manual da Fase 1

O plano de testes contempla:

- Publicação das mensagens MQTT.
- Recepção das mensagens pelo Node-RED.
- Gravação das leituras no MySQL.
- Execução do protótipo com dados CSV.
- Tratamento de dados inválidos.
- Execução dos testes automatizados.

Os testes de integração devem ser registrados com as evidências reais de cada execução. A aprovação dos testes unitários da IA não comprova, por si só, o funcionamento de toda a cadeia IoT.

## 📁 Estrutura do Projeto

```text
IoT-Challenge/
├── esp32/
│   └── diagram.json
├── node-red/
│   └── flows.json
├── sql/
│   └── commands.sql
├── ia/
│   ├── dados/
│   │   ├── README.md
│   │   ├── leituras.csv
│   │   └── resultado_anomalias.csv
│   ├── tests/
│   │   └── test_modelo_anomalias.py
│   ├── modelo_anomalias.py
│   ├── requirements.txt
│   └── README.md
├── docs/
│   └── TESTES_FASE1.md
├── challenge-IoT.docx
└── README.md
```

Outros arquivos do projeto podem existir conforme a configuração local e a evolução da implementação.

## 🎥 Demonstração

Vídeo de demonstração:

https://www.youtube.com/watch?v=HLcUOxubbEY

## ⚠️ Limitações e Considerações

- As leituras do ESP32 são simuladas.
- O broker MQTT utilizado é público.
- O protótipo estatístico é experimental e não foi validado clinicamente.
- Uma anomalia estatística não confirma doença ou condição médica.
- O funcionamento de cada componente deve ser comprovado por testes e evidências próprias.

## Validacao com dados reais do MySQL

A integracao com o banco MySQL foi validada usando a tabela
`leituras_pet` do banco `iot_pet`.

Resultados registrados em 21/10/2026:
- 34 leituras exportadas do MySQL.
- 34 leituras analisadas pelo modelo de IA.
- 0 anomalias estatisticas identificadas nessa execucao.
- 5 testes unitarios aprovados, sem falhas.

### Reproduzir a validacao

Na raiz do projeto, com o MySQL do XAMPP em execucao:

```powershell
python .\ia\buscar_mysql.py
python .\ia\modelo_anomalias.py .\ia\dados\leituras_mysql.csv -o .\ia\dados\resultado_anomalias.csv
python -m unittest discover -s ia/tests -p "test_*.py" -v
```

Arquivos gerados:
- `ia/dados/leituras_mysql.csv`
- `ia/dados/resultado_anomalias.csv`

A ausencia de anomalias estatisticas nao garante normalidade clinica.
Este prototipo nao realiza diagnostico veterinario.

## ✅ Conclusão

O projeto demonstra um fluxo de monitoramento IoT com geração de dados simulados, comunicação MQTT, processamento no Node-RED, armazenamento no MySQL e um protótipo Python para análise estatística de possíveis anomalias.

A solução serve como demonstração acadêmica dos conceitos de IoT, integração de sistemas, persistência de dados e testes de software.
