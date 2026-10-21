CREATE DATABASE IF NOT EXISTS iot_pet;

USE iot_pet;

-- Historico de eventos e classificacoes
CREATE TABLE IF NOT EXISTS pet_saude (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100),
    status VARCHAR(20),
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Leituras numericas para analise futura
CREATE TABLE IF NOT EXISTS leituras_pet (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    valor DECIMAL(8, 2) NOT NULL,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_leituras_pet_data (pet_id, data_registro),
    INDEX idx_leituras_tipo_data (tipo, data_registro)
);