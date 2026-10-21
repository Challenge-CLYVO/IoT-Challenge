import json
from pathlib import Path

arquivo = Path("node-red/flows.json")
fluxo = json.loads(arquivo.read_text(encoding="utf-8-sig"))

if not isinstance(fluxo, list):
    raise SystemExit("ERRO: o fluxo não é uma lista JSON. Arquivo preservado.")

nos = {n.get("id"): n for n in fluxo}

necessarios = [
    "66dd1c238c2735a6",
    "3b0e361622634654",
    "0ae4e392a620d882",
    "87c6820adf2cf68d",
    "a6a47ed5023dc746",
    "459fdba4e6383ee6",
]

if any(i not in nos for i in necessarios):
    raise SystemExit("ERRO: faltam nós esperados. Arquivo não alterado.")

# Criar backup válido antes de modificar
backup = Path("node-red/flows.backup.estrutura_valida.json")
backup.write_text(
    json.dumps(fluxo, ensure_ascii=False, indent=4),
    encoding="utf-8"
)

# Corrigir inscrições MQTT
nos["66dd1c238c2735a6"]["topic"] = "pet/+/temperatura"
nos["3b0e361622634654"]["topic"] = "pet/+/atividade"

# Função de temperatura
nos["0ae4e392a620d882"]["func"] = r"""
const temp = Number(msg.payload);
const match = (msg.topic || "").match(/^pet\/(\d+)\/temperatura$/);

if (!match || !Number.isFinite(temp) || temp < 30 || temp > 45) {
    node.warn("Temperatura inválida ou fora da escala.");
    return null;
}

const petId = Number(match[1]);
let descricao, status;

if (temp >= 39.5) {
    descricao = "Febre alta detectada"; status = "critico";
} else if (temp >= 39.1) {
    descricao = "Temperatura levemente elevada"; status = "alerta";
} else if (temp >= 37.5) {
    descricao = "Temperatura normal"; status = "ok";
} else if (temp >= 36.0) {
    descricao = "Temperatura baixa (hipotermia leve)"; status = "alerta";
} else {
    descricao = "Hipotermia grave"; status = "critico";
}

const msgSql = {
    topic: `INSERT INTO pet_saude (descricao, status) VALUES ('${descricao} - ${temp} C', '${status}')`
};
const msgDash = {
    payload: descricao,
    statusCode: status,
    value: temp
};
const msgLeitura = {
    topic: `INSERT INTO leituras_pet (pet_id, tipo, valor) VALUES (${petId}, 'temperatura', ${temp})`
};

return [msgSql, msgDash, msgLeitura];
""".strip()

# Função de atividade
nos["87c6820adf2cf68d"]["func"] = r"""
const atividade = Number(msg.payload);
const match = (msg.topic || "").match(/^pet\/(\d+)\/atividade$/);

if (!match || !Number.isFinite(atividade) || atividade < 0 || atividade > 500) {
    node.warn("Atividade inválida ou fora da escala.");
    return null;
}

const petId = Number(match[1]);
let descricao, status;

if (atividade <= 10) {
    descricao = "Em repouso"; status = "ok";
} else if (atividade <= 50) {
    descricao = "Movimento leve"; status = "ok";
} else if (atividade <= 150) {
    descricao = "Atividade moderada"; status = "alerta";
} else {
    descricao = "Atividade excessiva"; status = "critico";
}

const msgSql = {
    topic: `INSERT INTO pet_saude (descricao, status) VALUES ('${descricao} - ${atividade}', '${status}')`
};
const msgDash = {
    payload: descricao,
    descricao: descricao,
    status: status
};
const msgLeitura = {
    topic: `INSERT INTO leituras_pet (pet_id, tipo, valor) VALUES (${petId}, 'atividade', ${atividade})`
};

return [msgSql, msgDash, msgLeitura];
""".strip()

# Três saídas: histórico, dashboard e leituras numéricas.
# Os nós MySQL existentes são reutilizados.
temp = nos["0ae4e392a620d882"]
temp["outputs"] = 3
temp["wires"] = [
    [nos["a6a47ed5023dc746"]["id"]],
    ["c5e46c3ac4483f4d"],
    [nos["a6a47ed5023dc746"]["id"]]
]

ativ = nos["87c6820adf2cf68d"]
ativ["outputs"] = 3
ativ["wires"] = [
    [nos["459fdba4e6383ee6"]["id"]],
    ["fe40b60cbfc2d9c4"],
    [nos["459fdba4e6383ee6"]["id"]]
]

# Salvar e reler para validar
conteudo = json.dumps(fluxo, ensure_ascii=False, indent=4)
json.loads(conteudo)
arquivo.write_text(conteudo, encoding="utf-8")

# Verificação final
conferido = json.loads(arquivo.read_text(encoding="utf-8"))
assert isinstance(conferido, list)
assert nos["66dd1c238c2735a6"]["topic"] == "pet/+/temperatura"
assert nos["3b0e361622634654"]["topic"] == "pet/+/atividade"
assert temp["outputs"] == 3 and ativ["outputs"] == 3

print("SUCESSO: JSON válido, tópicos corrigidos e três saídas configuradas.")
print(f"Backup: {backup}")
