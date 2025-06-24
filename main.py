from Region_QuadTree import Region_Quad_Tree
from ponto import Ponto
from camera import Camera

a = Ponto(-128, -128)
b = Ponto(0,0)
quadrante = Region_Quad_Tree(a,256)
cam = Camera(b, 9, quadrante)
c = Ponto(100,100)
d = Ponto(10,10)

if(quadrante.check(c)):
    print("dento")
else:
    print("fora")

if(quadrante.check(d)):
    print("dento")
else:
    print("fora")
