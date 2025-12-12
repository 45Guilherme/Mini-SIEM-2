from alertas import alerta
from parser import extrair_info
from detector import verificar_ataque

def main():

    log = ["Dec 12 10:02:12 server sshd[1111]: Failed password for root from 123.123.123.1 port 44222\n", 
           "Nov 12 14:34:05 server sshd[1202]: Accepted password for user1 from 192.168.0.10 port 52345 ssh2\n", 
           "Nov 12 14:36:50 server sshd[1205]: Failed password for root from 10.0.0.5 port 50231 ssh2\n"]
    
    for linha in log:
        ip = extrair_info(linha)

    tentativas = 7

    if verificar_ataque(tentativas):
        alerta(ip, tentativas)


if __name__ == "__main__":
    main()
