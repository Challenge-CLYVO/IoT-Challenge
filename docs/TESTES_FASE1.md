
# Plano de testes — IoT Pet — Fase 1

## 1. Objetivo

Verificar o funcionamento do fluxo de monitoramento simulado de pets:
publicação de leituras pelo ESP32 no Wokwi, transmissão por MQTT,
recepção pelo Node-RED, gravação no MySQL e análise estatística de dados.

## 2. Escopo dos testes

- Publicação de temperatura e atividade pelo ESP32 simulado.
- Recepção das mensagens MQTT pelo Node-RED.
- Persistência das leituras no banco MySQL.
- Preparação dos dados para análise.
- Execução do protótipo de detecção de anomalias.
- Execução dos testes automatizados do protótipo.

## 3. Casos de teste manuais

### CT01 — Publicação MQTT

**Objetivo:** verificar se o ESP32 publica leituras no broker MQTT.

**Dados de entrada:** pet ID 104; temperatura e atividade simuladas.

**Procedimento:**
1. Iniciar a simulação ESP32 no Wokwi.
2. Conferir o endereço do broker e os tópicos configurados.
3. Observar as mensagens publicadas.

**Resultado esperado:** mensagens nos tópicos `pet/104/temperatura` e
`pet/104/atividade`, de acordo com a configuração do código.

### CT02 — Recepção no Node-RED

**Objetivo:** verificar a recepção das mensagens MQTT.

**Dados de entrada:** mensagens publicadas nos tópicos do pet 104.

**Procedimento:**
1. Abrir o editor Node-RED.
2. Conferir as assinaturas `pet/+/temperatura` e `pet/+/atividade`.
3. Clicar em Deploy.
4. Iniciar ou manter a simulação ESP32.

**Resultado esperado:** o Node-RED recebe mensagens de temperatura e
atividade e encaminha os valores para o fluxo de processamento.

### CT03 — Persistência no MySQL

**Objetivo:** verificar a gravação das leituras.

**Dados de entrada:** mensagens recebidas pelo Node-RED.

**Procedimento:**
1. Confirmar que o banco `iot_pet` existe.
2. Conferir a tabela `leituras_pet`.
3. Consultar os registros após a execução do fluxo.

**Resultado esperado:** novas leituras são gravadas com identificação do pet,
tipo, valor e data de registro.

Consulta de verificação:

```sql
USE iot_pet;

SELECT id, pet_id, tipo, valor, data_registro
FROM leituras_pet
ORDER BY id DESC
LIMIT 20;
```

### CT04 — Detecção de valor atípico

**Objetivo:** verificar se o protótipo sinaliza uma leitura estatisticamente
atípica.

**Dados de entrada:** cinco leituras de temperatura para o pet 104:
30, 31, 30, 32 e 100.

**Procedimento:**
1. Salvar as leituras em um arquivo CSV com o cabeçalho exigido.
2. Executar o script `ia/modelo_anomalias.py`.
3. Abrir o CSV de resultado.

**Resultado esperado:** a leitura 100 é sinalizada como possível anomalia
em relação às demais leituras do mesmo pet e tipo.

### CT05 — Validação de dados inválidos

**Objetivo:** verificar a rejeição de valores não numéricos.

**Dados de entrada:** uma leitura com `valor=abc`.

**Procedimento:**
1. Executar o teste automatizado correspondente.
2. Conferir o resultado apresentado pelo Python.

**Resultado esperado:** o código gera `ValueError` ao receber um valor inválido.

## 4. Testes automatizados

Arquivo: `ia/tests/test_modelo_anomalias.py`

Os testes verificam:
- Identificação de valor atípico.
- Tratamento de amostras insuficientes.
- Separação de grupos por pet.
- Rejeição de valores inválidos.
- Rejeição de colunas obrigatórias ausentes.

Comando para executar na raiz do projeto:

```powershell
python -m unittest discover -s ia/tests -p "test_*.py" -v
```

**Critério de aprovação:** todos os testes automatizados terminam com
`OK`, sem erros ou falhas.

## 5. Registro dos resultados

| Caso | Resultado real | Status |
|---|---|---|
| CT01 — Publicação MQTT | Recepção de mensagens de temperatura e atividade observada durante a validação da integração. | Validado na integração |
| CT02 — Recepção Node-RED | Leituras processadas pelo fluxo e dashboard funcionando, conforme validação anterior. | Validado na integração |
| CT03 — Persistência MySQL | 34 leituras exportadas da tabela `leituras_pet`. | Aprovado |
| CT04 — Detecção de anomalia | Modelo executado sobre 34 leituras; zero anomalias estatísticas identificadas. Teste unitário de valor atípico aprovado. | Aprovado nos testes executados |
| CT05 — Dados inválidos | Entrada `abc` rejeitada com `ValueError: Valor inválido: abc`. | Aprovado — teste negativo manual |

Os status distinguem a validação da integração, os testes automatizados e os testes manuais. A aprovação de um teste unitário não substitui um teste manual de ponta a ponta.
### Evidência manual do CT05 — dados inválidos

**Entrada:** arquivo `ia/dados/teste_dados_invalidos.csv`, com `abc` no campo `valor`.

**Resultado observado:** o modelo rejeitou a entrada e apresentou `ValueError: Valor inválido: abc`. A análise foi interrompida e não foi gerado arquivo CSV de saída.

**Conclusão:** teste negativo manual aprovado. O modelo não aceitou o valor textual como número válido.

## 6. Validação da IA com dados reais do MySQL

**Data da execucao:** 21/10/2026

### Objetivo
Validar a exportacao de leituras da tabela `leituras_pet` do banco
`iot_pet` e a analise dessas leituras pelo modelo de deteccao de anomalias.

### Teste de integracao com o banco
- Banco: `iot_pet`
- Tabela: `leituras_pet`
- Identificador do pet: `104`
- Registros exportados: 34
- Arquivo de entrada: `ia/dados/leituras_mysql.csv`
- Resultado: aprovado. A exportacao foi concluida com sucesso.

### Teste do modelo de IA
- Arquivo de saida: `ia/dados/resultado_anomalias.csv`
- Leituras analisadas: 34
- Possiveis anomalias estatisticas identificadas: 0
- Resultado: execucao concluida sem erros.

**Observacao:** a ausencia de anomalias estatisticas nao comprova
que todas as leituras estejam clinicamente normais. A avaliacao
estatistica e os limites clinicos devem ser considerados separadamente.

### Testes unitarios
Comando executado:

```powershell
python -m unittest discover -s ia/tests -p "test_*.py" -v
```

Resultado: 5 testes aprovados, 0 falhas.

Casos validados:
1. Tratamento de amostras insuficientes.
2. Identificacao de valor atipico.
3. Rejeicao de coluna obrigatoria ausente.
4. Rejeicao de valor invalido.
5. Separacao dos grupos por pet e tipo de leitura.

### Evidencias geradas
- `ia/dados/leituras_mysql.csv`
- `ia/dados/resultado_anomalias.csv`
- `ia/tests/test_modelo_anomalias.py`

### Conclusao
A exportacao dos dados reais do MySQL, a execucao do modelo
e os cinco testes unitarios foram concluidos com sucesso.
A validacao documenta o funcionamento tecnico do prototipo,
sem afirmar diagnostico veterinario.

## 7. Limitações
O ambiente utiliza leituras simuladas e um método estatístico simples.
Os resultados demonstram o funcionamento técnico do protótipo, mas não
comprovam precisão clínica, diagnóstico ou previsão de doenças.
