print("Arquivo 2: carregado")

from arquivo1 import funcao_de_arquivo1

print("Arquivo 2: agora vou chamar a função do arquivo 1")
funcao_de_arquivo1()

if __name__ == "__main__":
    print("Arquivo 1: executado diretamente")
    print("Arquivo 2: executado diretamente")
