from ponto import Ponto, dist
from node import Node
from camera import Camera
class Region_Quad_Tree:


    def __init__(self, _top_left, _lado):
        self.root = Node(_top_left, _lado) # será trocado por um R_node
        self.top_left = _top_left
        self.lado = _lado

    def check(self, ponto):
        retorno = self._check(ponto, self.root)
        return retorno

#retorna se um ponto está dentro do raio de visão da camera
   # retorna 1 se está dentro, e zero se está fora
    def _check(self, ponto, current):
        if current.eh_preenchido == 1: #NÃO BOOLEANO
            return True
        elif current.eh_preenchido == 0:
            return False

        #recursão até chegar em um dos casos bases, e vai retornando
        else:
            centro = Ponto(current.top_left.x + (current.lado / 2), current.top_left.y + (current.lado / 2))

            if ponto.x >= centro.x and ponto.y < centro.y:
                retorno = self._check(ponto, current.NE)  # NE
                return retorno
            elif ponto.x < centro.x and ponto.y < centro.y:
                retorno = self._check(ponto, current.NW)  # NW
                return retorno
            elif ponto.x < centro.x and ponto.y >= centro.y:
                retorno = self._check(ponto, current.SW)  # SW
                return retorno
            elif ponto.x >= centro.x and ponto.y >= centro.y:
                retorno = self._check(ponto, current.SE)  # SE
                return retorno


        ########################A PARTIR DAQ, PODE SER DA CLASSE CAMERA ###########


    # verifica se um quadrante está 100% dentro do raio de visão da camera
    # está preenchido se a distância do ponto até a maior diagonal do quadrante é menor que o raio
    def _eh_dentro(self, cam, current):
        dist1 = dist(cam.centro.x, cam.centro.y, current.top_left.x, current.top_left.y)# canto sup_esq
        dist2 = dist(cam.centro.x, cam.centro.y, current.top_left.x + current.lado, current.top_left.y)# canto sup_dir
        dist3 = dist(cam.centro.x, cam.centro.y, current.top_left.x, current.top_left.y + current.lado)# canto inf_esq
        dist4 = dist(cam.centro.x, cam.centro.y, current.top_left.x + current.lado, current.top_left.y + current.lado)# canto inf_dir

        maior_dist = max(max(dist1, dist2), max(dist3, dist4)) # maior das 4 distancias

        if maior_dist <= cam.raio:
            return True
        return False


# retorna se um quadrante está totalmente fora do raio da camera
    def _eh_fora(self, cam, current):
        x_perto = max(current.top_left.x, min(cam.centro.x, current.top_left.x + current.lado))
        y_perto = max(current.top_left.y - current.lado, min(cam.centro.y, current.top_left.y))

        dist_minima = dist(cam.centro.x, cam.centro.y, x_perto, y_perto )

        if dist_minima > cam.raio:
            return True
        return False

    def atualiza_quadtree(self, cam):

        self._atualiza_quadtree(cam, self.root)

    def _atualiza_quadtree(self, cam, current):
        if (self._eh_fora(cam, current)):
            return
        if (self._eh_dentro(cam, current)):
            current.eh_preenchido = 1
            return
        if current.SW is None: # se um é null, já significa que é um nó_folha
            # subdivido a quadtree
            current.NW = Node(Ponto(current.top_left.x, current.top_left.y), current.lado / 2)
            current.NE = Node(Ponto(current.top_left.x + current.lado / 2, current.top_left.y), current.lado / 2)
            current.SW = Node(Ponto(current.top_left.x, current.top_left.y + current.lado / 2), current.lado / 2)
            current.SE = Node(Ponto(current.top_left.x + current.lado / 2,  current.top_left.y + current.lado / 2), current.lado / 2)

        self._atualiza_quadtree(cam, current.SW)
        self._atualiza_quadtree(cam, current.SE)
        self._atualiza_quadtree(cam, current.NW)
        self._atualiza_quadtree(cam, current.NE)