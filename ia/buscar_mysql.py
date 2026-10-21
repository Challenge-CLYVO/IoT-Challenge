import argparse
import csv
import os
import subprocess
import sys
from pathlib import Path

COLUNAS = ["pet_id", "tipo", "valor", "data_registro"]


def exportar_mysql(saida, banco, usuario, host, porta):
    executavel = Path(r"C:\xampp\mysql\bin\mysql.exe")

    if not executavel.exists():
        raise RuntimeError(f"Executavel MySQL nao encontrado: {executavel}")

    consulta = (
        "SELECT pet_id, tipo, valor, data_registro "
        "FROM leituras_pet "
        "ORDER BY data_registro ASC"
    )

    comando = [
        str(executavel),
        f"--host={host}",
        f"--port={porta}",
        f"--user={usuario}",
        "--database", banco,
        "--batch",
        "--raw",
        "--skip-column-names",
        "--execute", consulta,
    ]

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
            env=os.environ.copy(),
        )
    except subprocess.CalledProcessError as erro:
        detalhe = erro.stderr.strip() or "Erro nao detalhado"
        raise RuntimeError(f"Falha na consulta MySQL: {detalhe}")

    destino = Path(saida)
    destino.parent.mkdir(parents=True, exist_ok=True)

    quantidade = 0
    with destino.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(COLUNAS)

        for linha in resultado.stdout.splitlines():
            campos = linha.split("\t")
            if len(campos) == len(COLUNAS):
                escritor.writerow(campos)
                quantidade += 1

    print(f"Leituras exportadas: {quantidade}")
    print(f"Arquivo: {destino.resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="Exporta leituras_pet do MySQL para CSV."
    )
    parser.add_argument("--saida", default="ia/dados/leituras_mysql.csv")
    parser.add_argument("--banco", default="iot_pet")
    parser.add_argument("--usuario", default="root")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--porta", default="3306")
    args = parser.parse_args()

    try:
        exportar_mysql(
            args.saida, args.banco, args.usuario,
            args.host, args.porta
        )
    except RuntimeError as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
