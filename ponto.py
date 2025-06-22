class Ponto:
    def __init__(self, x, y):
        if x <= 128 and x >= -128 and y <= 128  and y >= -128:
            self.x = x
            self.y = y
        else:
            print("ponto inválido")
            self.x = 0
            self.y = 0

    def print_ponto(self):
        print("(", self.x, ",", self.y, ")")
