from datetime import datetime

def alerta(ip, tentativas, nivel):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S") 
    with open("alerta.log", "a", encoding="utf-8") as file:
        file.write(f"{timestamp} - ATAQUE SUSPEITO do IP: {ip} Tentativas: {tentativas} Cor: {nivel}\n")
    msg = f"{timestamp} - 🔔 ATAQUE SUSPEITO do IP: {ip} Tentativas: {tentativas} Cor: {nivel}\n"
    if nivel == "ALTO":         
       cor = "VERMELHO"

    elif nivel == "MEDIO":
         
       cor = "AMARELO"
    else:
       cor = "ROXO"
    print(colorir(msg, cor))



def colorir(texto, cor):
        cores = {
        "VERMELHO": "\033[31m",
        "VERDE": "\033[32m",
        "AMARELO": "\033[33m",
        "AZUL": "\033[34m",
        "CIANO": "\033[36m",
        "RESET": "\033[0m"
        }
        return cores.get(cor, cores["RESET"]) + texto + cores["RESET"]