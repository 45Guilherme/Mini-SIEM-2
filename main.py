from alertas import alerta
from parser import extrair_info
from detector import verificar_ataque

def main():
    linha = "Nov 12 14:33:01 server sshd[1201]: Failed password for root from 177.233.10.45 port 45821 ssh2"

    ip = extrair_info(linha)

    tentativas = 7

    if verificar_ataque(tentativas):
        alerta(ip, tentativas)


if __name__ == "__main__":
    main()
