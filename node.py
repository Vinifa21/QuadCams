class Node:
    # 1 = ta no alcance  # 0 = fora do alcance
    def __init__(self, _top_left, _lado, _eh_preenchido=0):
        self.eh_preenchido = _eh_preenchido # NÃO BOOLEANO

        self.NE = None
        self.NW = None
        self.SW = None
        self.SE = None

        self.top_left = _top_left
        self.lado = _lado
