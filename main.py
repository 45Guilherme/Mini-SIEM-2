from alertas import alerta, tipo_ataque, colorir
from parser import extrair_info
from detector import verificar_ataque, contra_spam
from classificar import classificar_ataque
import time
from datetime import datetime
import json
import os

# Função principal de monitoramento
def monitorar():
    tentativas_por_ip = {}
    alertas = []
    salvar = input("Deseja salvar alertas em CSV? (s/n): ").upper()

    try:
        with open("server.log", "r", encoding="utf-8") as file:
            # 1️⃣ Processa todas as linhas já existentes
            linhas_existentes = file.readlines()
            for linha in linhas_existentes:
                processar_linha(linha, tentativas_por_ip, alertas, salvar)

            # 2️⃣ Move para o final do arquivo e monitora novas linhas
            file.seek(0, 2)
            while True:
                linha = file.readline()
                if not linha:
                    time.sleep(2)
                    continue
                processar_linha(linha, tentativas_por_ip, alertas, salvar)

    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário.")

# Função para processar cada linha do log
def processar_linha(linha, tentativas_por_ip, alertas, salvar):
    ip = extrair_info(linha)
    if not ip:
        return  # ignora linhas sem IP

    # Atualiza número de tentativas
    tentativas_por_ip[ip] = tentativas_por_ip.get(ip, 0) + 1
    total_tentativas = tentativas_por_ip[ip]
    nivel = verificar_ataque(total_tentativas)

    alerta_atual = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": ip,
        "tentativas": total_tentativas,
        "nivel": nivel,
        "tipo": tipo_ataque(nivel)
    }

    # Se o ataque for alto ou médio, gera alerta e registra
    if nivel in ["ALTO", "MEDIO"] and contra_spam(ip):
        alerta(ip, total_tentativas, nivel)
        registrar(ip, total_tentativas, nivel)
        cor = "VERMELHO" if nivel == "ALTO" else "AMARELO"
        print(colorir(f"{ip} → {total_tentativas} tentativas - {tipo_ataque(nivel)}", cor))

        if salvar == "S":
            salvar_csv(alerta_atual)

    elif nivel == "INFO":
        print(colorir("Nível tranquilo", "CIANO"))

    # Salva alertas para JSON
    alertas.append(alerta_atual)
    salvar_alertas_json(alertas)
    print(f"{len(alertas)} alertas salvos em alertas.json")

# Salvar alertas em JSON
def salvar_alertas_json(alertas, arquivo="alertas.json"):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(alertas, f, indent=4)

# Salvar alertas em CSV
def salvar_csv(alerta):
    csv_existe = os.path.exists("server.csv")
    with open("server.csv", "a", encoding="utf-8") as file:
        if not csv_existe:
            # Cabeçalho
            file.write("timestamp,ip,tentativas,nivel,tipo\n")
        # Linha de dados
        file.write(
            f"{alerta['timestamp']},{alerta['ip']},{alerta['tentativas']},{alerta['nivel']},{alerta['tipo']}\n"
        )

# Registrar alerta em log
def registrar(ip, tentativas, nivel):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("alerta.log", "a", encoding="utf-8") as file:
        file.write(f"{timestamp} -{tipo_ataque(nivel)} - {classificar_ataque(nivel)} {ip} fez {tentativas} tentativas, Nivel: {nivel}\n")


if __name__ == "__main__":
    monitorar()
