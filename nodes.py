class R_node:
    # 1 = ta no alcance  # 0 = fora do alcance
    def __init__(self, _retangulo, _eh_preenchido=0, _eh_folha=False):
        self.eh_folha = _eh_folha
        self.eh_preenchido = _eh_preenchido # NÃO BOOLEANO

        self.NE = None
        self.NW = None
        self.SW = None
        self.SE = None
