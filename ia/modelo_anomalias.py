
import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

COLUNAS_OBRIGATORIAS = {"pet_id", "tipo", "valor", "data_registro"}


def analisar_leituras(leituras, minimo_amostras=5, limite_z=3.5):
    """Identifica valores atípicos agrupando por pet e tipo de leitura."""
    grupos = defaultdict(list)

    for linha in leituras:
        faltantes = COLUNAS_OBRIGATORIAS - linha.keys()
        if faltantes:
            raise ValueError(
                f"Colunas ausentes: {', '.join(sorted(faltantes))}"
            )

        try:
            valor = float(linha["valor"])
        except (TypeError, ValueError):
            raise ValueError(f"Valor inválido: {linha['valor']}")

        if not math.isfinite(valor):
            raise ValueError(f"Valor não finito: {linha['valor']}")

        chave = (linha["pet_id"], linha["tipo"])
        grupos[chave].append((linha, valor))

    resultados = []

    for leituras_grupo in grupos.values():
        valores = [valor for _, valor in leituras_grupo]
        mediana = statistics.median(valores)
        desvios = [abs(valor - mediana) for valor in valores]
        mad = statistics.median(desvios)

        for linha, valor in leituras_grupo:
            anomalia = False

            if len(valores) >= minimo_amostras:
                if mad > 0:
                    z_robusto = 0.6745 * abs(valor - mediana) / mad
                    anomalia = z_robusto > limite_z
                else:
                    # Alternativa quando a maioria das leituras é igual.
                    tolerancia = max(1.0, abs(mediana) * 0.05)
                    anomalia = abs(valor - mediana) > tolerancia

            resultado = dict(linha)
            resultado["valor"] = str(valor)
            resultado["anomalia"] = "sim" if anomalia else "nao"
            resultado["motivo"] = (
                f"Valor atípico em relação ao grupo (mediana: {mediana:g})"
                if anomalia
                else (
                    "Amostras insuficientes para análise"
                    if len(valores) < minimo_amostras
                    else "Nenhuma anomalia estatística identificada"
                )
            )
            resultados.append(resultado)

    return resultados


def analisar_csv(arquivo_entrada, arquivo_saida):
    with open(arquivo_entrada, "r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        if not leitor.fieldnames:
            raise ValueError("O CSV está vazio ou não possui cabeçalho.")

        faltantes = COLUNAS_OBRIGATORIAS - set(leitor.fieldnames)
        if faltantes:
            raise ValueError(
                f"Colunas ausentes no CSV: {', '.join(sorted(faltantes))}"
            )

        leituras = list(leitor)
        campos_originais = list(leitor.fieldnames)

    resultados = analisar_leituras(leituras)
    campos_saida = campos_originais + ["anomalia", "motivo"]

    destino = Path(arquivo_saida)
    destino.parent.mkdir(parents=True, exist_ok=True)

    with open(destino, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos_saida)
        escritor.writeheader()
        escritor.writerows(resultados)

    quantidade = sum(r["anomalia"] == "sim" for r in resultados)
    print(f"Leituras analisadas: {len(resultados)}")
    print(f"Possíveis anomalias: {quantidade}")
    print(f"Arquivo gerado: {destino}")


def main():
    parser = argparse.ArgumentParser(
        description="Protótipo estatístico de detecção de leituras atípicas."
    )
    parser.add_argument("entrada", help="Caminho do CSV de leituras")
    parser.add_argument(
        "-o", "--saida", default="ia/dados/resultado_anomalias.csv",
        help="Caminho do CSV de resultado"
    )
    args = parser.parse_args()
    analisar_csv(args.entrada, args.saida)


if __name__ == "__main__":
    main()
