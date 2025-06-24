
class Camera:

    lista_cameras = []

    def __init__(self, _centro, _raio,  quadtree):
        self.centro = _centro
        self.raio = _raio #raio de visão da câmera
        quadtree.atualiza_quadtree(self)
        self.lista_cameras.append(self)