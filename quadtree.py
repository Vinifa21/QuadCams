import numpy as np

class Ponto:
    """
    Representa um único ponto com coordenadas x e y.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circulo:
    """
    Representa um círculo com um centro (x, y) e um raio.
    """
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.raio = r
        self.raio_ao_quadrado = self.raio**2

    def contem_ponto(self, ponto):
        """Verifica se um ponto está dentro deste círculo."""
        dist_quadrada = (ponto.x - self.x)**2 + (ponto.y - self.y)**2
        return dist_quadrada < self.raio_ao_quadrado

class Retangulo:
    """
    Representa uma caixa delimitadora alinhada aos eixos (AABB) com um centro (x, y),
    largura (w) e altura (h).
    """
    def __init__(self, x, y, w, h):
        self.x = x  # Centro x
        self.y = y  # Centro y
        self.w = w  # Meia-largura
        self.h = h  # Meia-altura

    def intersecta_circulo(self, circulo):
        """
        Verifica se o retângulo cruza com um determinado círculo.

        Args:
            circulo (Circulo): O círculo para verificar a interseção.

        Returns:
            bool: True se eles se cruzam, False caso contrário.
        """
        # Encontra o ponto mais próximo no retângulo ao centro do círculo
        x_mais_proximo = np.clip(circulo.x, self.x - self.w, self.x + self.w)
        y_mais_proximo = np.clip(circulo.y, self.y - self.h, self.y + self.h)

        # Calcula a distância entre o centro do círculo e este ponto mais próximo
        dist_x = circulo.x - x_mais_proximo
        dist_y = circulo.y - y_mais_proximo

        # Se a distância for menor que o raio do círculo, eles se cruzam
        distancia_quadrada = (dist_x**2) + (dist_y**2)
        return distancia_quadrada < circulo.raio_ao_quadrado

    def esta_totalmente_contido_no_circulo(self, circulo):
        """
        Verifica se o retângulo está totalmente contido dentro de um determinado círculo.
        Isso é verdade se todos os quatro cantos do retângulo estiverem dentro do círculo.
        """
        cantos = [
            (self.x + self.w, self.y + self.h), # Canto superior direito
            (self.x - self.w, self.y + self.h), # Canto superior esquerdo
            (self.x + self.w, self.y - self.h), # Canto inferior direito
            (self.x - self.w, self.y - self.h)  # Canto inferior esquerdo
        ]

        for canto_x, canto_y in cantos:
            # Calcula a distância ao quadrado do canto ao centro do círculo
            dist_quadrada = (canto_x - circulo.x)**2 + (canto_y - circulo.y)**2
            # Se algum canto estiver fora ou na borda do círculo, ele não está totalmente contido
            if dist_quadrada >= circulo.raio_ao_quadrado:
                return False
        
        # Se todos os cantos estiverem dentro, o retângulo está totalmente contido
        return True

class QuadTree:
    """
    A classe QuadTree.
    Cada nó na árvore representa uma região retangular.
    """
    def __init__(self, fronteira, profundidade_maxima=8, profundidade=0):
        """
        Inicializa um nó QuadTree.

        Args:
            fronteira (Retangulo): A fronteira retangular deste nó da quadtree.
            profundidade_maxima (int): A profundidade máxima para subdividir.
            profundidade (int): A profundidade atual deste nó na árvore.
        """
        self.fronteira = fronteira
        self.profundidade_maxima = profundidade_maxima
        self.profundidade = profundidade

        self.filhos = [] # Contém os quatro nós filhos da QuadTree
        self.e_folha = True

    def subdividir(self):
        """
        Divide o nó atual em quatro quadrantes (filhos) iguais.
        """
        # Obtém as dimensões para os novos quadrantes
        centro_x = self.fronteira.x
        centro_y = self.fronteira.y
        nova_largura = self.fronteira.w / 2
        nova_altura = self.fronteira.h / 2
        proxima_profundidade = self.profundidade + 1

        # Cria os quatro filhos
        # Nordeste
        ne = Retangulo(centro_x + nova_largura, centro_y + nova_altura, nova_largura, nova_altura)
        self.filhos.append(QuadTree(ne, self.profundidade_maxima, proxima_profundidade))

        # Noroeste
        no = Retangulo(centro_x - nova_largura, centro_y + nova_altura, nova_largura, nova_altura)
        self.filhos.append(QuadTree(no, self.profundidade_maxima, proxima_profundidade))

        # Sudeste
        se = Retangulo(centro_x + nova_largura, centro_y - nova_altura, nova_largura, nova_altura)
        self.filhos.append(QuadTree(se, self.profundidade_maxima, proxima_profundidade))

        # Sudoeste
        so = Retangulo(centro_x - nova_largura, centro_y - nova_altura, nova_largura, nova_altura)
        self.filhos.append(QuadTree(so, self.profundidade_maxima, proxima_profundidade))

        self.e_folha = False

    def refinar(self, formas):
        """
        Refina recursivamente a quadtree com base na interseção com as fronteiras de uma lista de formas.
        Um nó é subdividido se cruzar a fronteira de QUALQUER uma das formas na lista.
        """
        deve_subdividir = False
        # Verifica se a fronteira deste nó cruza a fronteira de algum círculo
        for forma in formas:
            if self.fronteira.intersecta_circulo(forma) and not self.fronteira.esta_totalmente_contido_no_circulo(forma):
                deve_subdividir = True
                break  # Encontrou um motivo para subdividir, não precisa verificar outros

        if deve_subdividir and self.profundidade < self.profundidade_maxima:
            self.subdividir()
            for filho in self.filhos:
                filho.refinar(formas) # Passa a lista de formas para os filhos

    def obter_nos_folha(self):
        """
        Percorre a árvore e retorna todos os nós folha.
        """
        if self.e_folha:
            return [self]
        else:
            nos = []
            for filho in self.filhos:
                nos.extend(filho.obter_nos_folha())
            return nos