

def extrair_info(linha):
        partes = linha.split()
        for i, parte in enumerate(partes):            
            if parte == "from" and i + 1 < len(partes):                 
               return partes[i + 1]
            

    
    

