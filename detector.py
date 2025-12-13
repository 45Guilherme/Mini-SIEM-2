from datetime import datetime
tentativa_por_tempo_de_ip = {}

def verificar_ataque(total):
    if total >= 5:
        return "ALTO"
    elif total >= 3:
        return "MEDIO"
    else:
        return "INFO"
    
def contra_spam(ip, limite=60):
    agora = datetime.now()
    if ip not in tentativa_por_tempo_de_ip:
        tentativa_por_tempo_de_ip[ip] = agora
        return True
    
       
    ultimo_tempo = tentativa_por_tempo_de_ip[ip]
    diferenca = (agora - ultimo_tempo).total_seconds()

    if diferenca <= limite:
        return False
    else:
        tentativa_por_tempo_de_ip[ip] = agora
        return True


