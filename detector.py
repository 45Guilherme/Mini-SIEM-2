

def verificar_ataque(total):
    if total >= 5:
        return "ALTO"
    elif total >= 3:
        return "MEDIO"
    else:
        return "INFO"
