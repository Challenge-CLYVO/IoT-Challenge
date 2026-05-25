# 🚀 IoT Pet Monitoramento Inteligente (ESP32 + MQTT + Node-RED)

## 📌 Descrição do Projeto

Este projeto tem como objetivo desenvolver um sistema de monitoramento inteligente para pets utilizando conceitos de Internet das Coisas (IoT).

O sistema realiza a coleta de dados simulados de um dispositivo ESP32, enviando informações via protocolo MQTT. Esses dados são processados no Node-RED, exibidos em tempo real em um dashboard e armazenados em um banco de dados MySQL.

---

## 🎯 Objetivo

Criar um sistema completo de monitoramento IoT que contemple:

- 🐾 Monitoramento de atividade do pet  
- 🌡️ Leitura de temperatura  
- 📡 Comunicação via MQTT  
- 🔄 Processamento com Node-RED  
- 📊 Visualização em dashboard  
- 🗄️ Armazenamento em banco de dados  

---

## 🧱 Arquitetura da Solução

ESP32 (Wokwi)  
↓  
MQTT (broker.hivemq.com)  
↓  
Node-RED  
↓  
Dashboard em tempo real  
↓  
MySQL (armazenamento)  

---

## 🛠️ Tecnologias Utilizadas

- ESP32 (simulado no Wokwi)  
- MQTT (HiveMQ Public Broker)  
- Node-RED  
- MySQL  
- Arduino IDE / Wokwi Simulator  

---

## 🔌 Dados Monitorados

- 🌡️ Temperatura do ambiente/pet  
- 🐾 Nível de atividade do pet (simulado)  

---

## 📡 Tópicos MQTT

- `pet/temperatura`  
- `pet/atividade`  

---

## 🗄️ Banco de Dados

### 📌 Script SQL

CREATE DATABASE iot_pet;

USE iot_pet;

CREATE TABLE pet_saude (
  id INT AUTO_INCREMENT PRIMARY KEY,
  descricao VARCHAR(50),
  status VARCHAR(20),
  data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

---

## ⚙️ Como Executar o Projeto

### 1. Configurar o banco de dados

- Abrir o XAMPP  
- Iniciar o MySQL  
- Executar o script SQL (`commands.sql`)  
- Criar o banco `iot_monitoramento`  

---

### 2. Rodar o Node-RED

node-red

Acesse:

http://localhost:1880

---

### 3. Importar o fluxo

- Abrir Node-RED  
- Menu → Import  
- Selecionar `flows.json`  

---

### 4. Configurar MQTT

Broker:

broker.hivemq.com  

Tópicos:

- pet/temperatura  
- pet/atividade  

---

### 5. Executar o ESP32 (Wokwi)

- Abrir o projeto no Wokwi  
- Conectar na rede: `Wokwi-GUEST`  
- Iniciar simulação  
- O ESP32 começará a enviar dados via MQTT  

---

### 6. Visualizar o sistema

Node-RED Dashboard:

http://localhost:1880/ui  

---

## 📊 Funcionalidades

- Leitura automática de sensores (simulados)  
- Envio de dados via MQTT  
- Processamento em tempo real no Node-RED  
- Dashboard interativo  
- Armazenamento no MySQL  
- Monitoramento contínuo do estado do pet  

---

## 🧠 Fluxo do Sistema

ESP32 gera dados (temperatura e atividade)  
↓  
Publica via MQTT  
↓  
Node-RED recebe os dados  
↓  
Processa e exibe no dashboard  
↓  
Salva no MySQL  

---

## 📁 Estrutura do Projeto

IoT-Challenge/  
├── esp32/  
│   ├── sketch.ino  
│   └── diagram.json  
├── node-red/  
│   └── flows.json  
├── sql/  
│   └── commands.sql  
├── README.md  

---

## 🎥 Demonstração

https://www.youtube.com/watch?v=HLcUOxubbEY
