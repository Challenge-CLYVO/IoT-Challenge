
import unittest

from ia.modelo_anomalias import analisar_leituras


def criar_leitura(pet_id, tipo, valor, data="2026-10-21"):
    return {
        "pet_id": str(pet_id),
        "tipo": tipo,
        "valor": str(valor),
        "data_registro": data,
    }


class TestModeloAnomalias(unittest.TestCase):

    def test_identifica_valor_atipico(self):
        leituras = [
            criar_leitura(104, "temperatura", 30),
            criar_leitura(104, "temperatura", 31),
            criar_leitura(104, "temperatura", 30),
            criar_leitura(104, "temperatura", 32),
            criar_leitura(104, "temperatura", 100),
        ]

        resultado = analisar_leituras(leituras)
        atipicas = [r for r in resultado if r["anomalia"] == "sim"]

        self.assertEqual(len(atipicas), 1)
        self.assertEqual(float(atipicas[0]["valor"]), 100.0)

    def test_amostras_insuficientes(self):
        leituras = [
            criar_leitura(104, "temperatura", 30),
            criar_leitura(104, "temperatura", 45),
        ]

        resultado = analisar_leituras(leituras)

        self.assertTrue(
            all(r["anomalia"] == "nao" for r in resultado)
        )
        self.assertTrue(
            all("insuficientes" in r["motivo"] for r in resultado)
        )

    def test_separa_pets_e_tipos_de_leitura(self):
        leituras = [
            criar_leitura(104, "temperatura", 30),
            criar_leitura(104, "temperatura", 31),
            criar_leitura(104, "temperatura", 30),
            criar_leitura(104, "temperatura", 32),
            criar_leitura(104, "temperatura", 100),
            criar_leitura(205, "temperatura", 100),
        ]

        resultado = analisar_leituras(leituras)
        atipicas = [r for r in resultado if r["anomalia"] == "sim"]

        self.assertEqual(len(atipicas), 1)
        self.assertEqual(atipicas[0]["pet_id"], "104")

    def test_rejeita_valor_invalido(self):
        leituras = [criar_leitura(104, "temperatura", "abc")]

        with self.assertRaises(ValueError):
            analisar_leituras(leituras)

    def test_rejeita_coluna_obrigatoria_ausente(self):
        leituras = [{
            "pet_id": "104",
            "tipo": "temperatura",
            "valor": "30",
        }]

        with self.assertRaises(ValueError):
            analisar_leituras(leituras)


if __name__ == "__main__":
    unittest.main()
