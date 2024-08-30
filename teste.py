
import re

class Destino:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def __str__(self):
        return f"Destino(nome={self.nome}, email={self.email})"

    def validar_email(self):
        padrao = r"[^@]+@[^@]+\.[^@]+"
        return re.match(padrao, self.email) is not None

# Exemplo de uso com validação
destino3 = Destino("João Pedro", "joao@exemplo.com")

destinos = {}
destinos["lbortoletti@gmail.com"] = destino3
destinos["lbortoletti2@gmail.com"] = destino3
destinos["lbortoletti3@gmail.com"] = destino3
destinos["lbortoletti4@gmail.com"] = destino3

for chave, valor in destinos.items():
    print( f"{chave} - {valor}")


