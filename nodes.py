from ponto import Ponto
class Node_interno:
    def __init__(self, top_left= Ponto(-128, 128), lado=256): # não contém key, só 4 filhos
        # usar o valor padrão qnd é criado o pirmeiro node_interno
        self.NE = None
        self.NW = None
        self.SW = None
        self.SE = None
        # usados para decidir para qual quadrante vou andar (na real, não sei nem se precisaria)
        self.top_left = top_left #
        self.lado = lado

class Node_folha:
    def __init__(self, p):  # armazena um ponto p
        self.ponto = p


