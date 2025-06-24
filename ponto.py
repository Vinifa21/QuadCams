class Ponto:
    def __init__(self, x, y):
        if x <= 128 and x >= -128 and y <= 128  and y >= -128: # considerando lado = 256
            self.x = x
            self.y = y
        else:
            print("ponto inválido")
            self.x = 0
            self.y = 0

    def print_ponto(self):
        print("(", self.x, ",", self.y, ")")


def dist(x1, x2, y1, y2):
    return pow((pow(x1-x2, 2) + pow(y1-y2, 2)), 0.5)
