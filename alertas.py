from datetime import datetime

def alerta(ip, tentativas, nivel):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S") 
    
    # Pegamos o nome correto para log
    nome_evento = tipo_ataque(nivel)

    # Determinamos a cor
    if nivel == "ALTO":         
        cor = "VERMELHO"
    elif nivel == "MEDIO":
        cor = "AMARELO"
    else:
        cor = "ROXO"

    msg = f"{timestamp} - {nome_evento} do IP: {ip} Tentativas: {tentativas} Cor: {nivel}\n"

    # Salva no arquivo
    with open("alerta.log", "a", encoding="utf-8") as file:
        file.write(msg)
    
    # Print colorido no terminal
    print(colorir(msg, cor))

def tipo_ataque(nivel):
    mapa = {
        "ALTO": "ATAQUE DETECTADO",
        "MEDIO": "ATAQUE SUSPEITO",
        "BAIXO": "INFORMATIVO",
        "INFO": "INFORMATIVO"
    }
    return mapa.get(nivel, "INFORMATIVO")




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