
# Protótipo de detecção de anomalias — IoT Pet

## Objetivo

Analisar leituras simuladas de temperatura e atividade dos pets e
identificar valores estatisticamente atípicos.

## Funcionamento

1. Recebe um arquivo CSV com as leituras.
2. Agrupa os registros por pet e tipo de leitura.
3. Calcula a mediana e o desvio absoluto mediano (MAD).
4. Sinaliza possíveis valores atípicos quando há pelo menos cinco amostras.
5. Gera um CSV com as colunas `anomalia` e `motivo`.

## Formato de entrada

O CSV deve possuir as colunas:

- `pet_id`
- `tipo`
- `valor`
- `data_registro`

Exemplo:

```csv
pet_id,tipo,valor,data_registro
104,temperatura,30,2026-10-21 08:00:00
104,temperatura,31,2026-10-21 08:00:03
104,temperatura,30,2026-10-21 08:00:06
104,temperatura,32,2026-10-21 08:00:09
104,temperatura,100,2026-10-21 08:00:12
```

## Como executar

Na raiz do projeto:

```powershell
python .\ia\modelo_anomalias.py .\ia\dados\leituras.csv -o .\ia\dados\resultado_anomalias.csv
```

Substitua `leituras.csv` pelo CSV real exportado do banco ou preparado
para o teste.

## Testes automatizados

Na raiz do projeto:

```powershell
python -m unittest discover -s ia/tests -p "test_*.py" -v
```

## Limitações

Este é um protótipo estatístico para demonstração acadêmica. As leituras
do projeto podem ser simuladas e não representam validação clínica.
Uma anomalia estatística não confirma doença nem substitui avaliação
veterinária.
