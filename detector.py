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
        agora = tentativa_por_tempo_de_ip
        return True

