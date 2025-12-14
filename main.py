from alertas import alerta, tipo_ataque, colorir
from parser import extrair_info
from detector import verificar_ataque, contra_spam
from classificar import classificar_ataque
import time
from datetime import datetime
import json
import os


def main():

    tentativas_por_ip = {}

   
    with open("server.log", "r", encoding="utf-8") as file:
        for linha in file:
            ip = extrair_info(linha)
            if ip:
                tentativas_por_ip[ip] = tentativas_por_ip.get(ip, 0) + 1

    for ip, total in tentativas_por_ip.items():
        nivel = verificar_ataque(total)
        if nivel in ["ALTO", "MEDIO"]:
            alerta(ip, total, nivel)

def monitorar():
    tentativas_por_ip = {}
    alertas = []

    try:
        with open("server.log", "r", encoding="utf-8") as file:
            file.seek(0, 2)  # Vai para o final do arquivo
            while True:
                linha = file.readline()
                

                if linha == "":
                    time.sleep(2)
                    continue 
                else:
                    ip = extrair_info(linha)  # Extrai IP da linha

                    if ip:  # Só continua se achou um IP
                        tentativas_por_ip[ip] = tentativas_por_ip.get(ip, 0) + 1
                        print(f"{ip} → {tentativas_por_ip[ip]} tentativas")
                        nivel = verificar_ataque(tentativas_por_ip[ip])
                        alerta_atual = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"ip": ip, "tentativas": tentativas_por_ip[ip],"nivel": nivel, "tipo": tipo_ataque(nivel)}
                        if nivel == "ALTO":
                            if contra_spam(ip):
                                alerta(ip, tentativas_por_ip[ip], nivel)
                                registrar(ip, tentativas_por_ip[ip], nivel)
                                print(colorir(f"{ip} → {tentativas_por_ip[ip]} tentativas - {tipo_ataque(nivel)}", "VERMELHO"))
                                salvar_csv(alerta_atual)
                        elif nivel == "MEDIO":
                            if contra_spam(ip):
                                alerta(ip, tentativas_por_ip[ip], nivel)
                                registrar(ip, tentativas_por_ip[ip], nivel)
                                print(colorir(f"{ip} → {tentativas_por_ip[ip]} tentativas - {tipo_ataque(nivel)}", "AMARELO"))
                                salvar_csv(alerta_atual)
                        elif nivel == "INFO":
                            print(colorir("Nível tranquilo", "CIANO"))
                        alertas.append(alerta_atual)
                        salvar_alertas_json(alertas)
                        print(f"{len(alertas)} alertas salvos em alertas.json")                  
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário.")

def salvar_alertas_json(alertas, arquivo="alertas.json"):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(alertas, f, indent=4)

def salvar_csv(alerta):
       csv_existe = os.path.exists("server.csv")
       with open("server.csv", "a", encoding="utf-8") as file:
              if not csv_existe:
                  file.write(f"timestamp,ip,tentativas,nivel,tipo\n")
              file.write(
            f"{alerta['timestamp']},"
            f"{alerta['ip']},"
            f"{alerta['tentativas']},"
            f"{alerta['nivel']},"
            f"{alerta['tipo']}\n"
        )



def loop():
    contador = 0
    while True:
        if contador >= 1 and contador <= 3:
            contador += 1
            time.sleep(1)
            print("Baixo nível")
        elif contador >= 4 and contador <= 6:
            contador += 2
            time.sleep(2)
            print("Médio nível")
        elif contador >= 7:
           contador += 4
           time.sleep(3)
           print("Alto nível")
        else:
            print("Nível Seguro")
            contador += 1
            time.sleep(5)

        if contador > 20:
            print("Reiniciando contador...\n")
            contador = 0

def registrar(ip, tentativas, nivel):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S") 
    with open("alerta.log", "a", encoding="utf-8") as file:
        file.write(f"{timestamp} -{tipo_ataque(nivel)} - {classificar_ataque(nivel)} {ip} fez {tentativas} tentativas, Nivel: {nivel}\n")
     

if __name__ == "__main__":
  monitorar()
