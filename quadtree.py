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

    def contem_ponto(self, ponto):
        """Verifica se um ponto está dentro deste retângulo."""
        return (self.x - self.w <= ponto.x < self.x + self.w and
                self.y - self.h <= ponto.y < self.y + self.h)

    def intersecta_circulo(self, circulo):
        """
        Verifica se o retângulo cruza com um determinado círculo.
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
        """
        cantos = [
            (self.x + self.w, self.y + self.h), (self.x - self.w, self.y + self.h),
            (self.x + self.w, self.y - self.h), (self.x - self.w, self.y - self.h)
        ]
        for canto_x, canto_y in cantos:
            dist_quadrada = (canto_x - circulo.x)**2 + (canto_y - circulo.y)**2
            if dist_quadrada >= circulo.raio_ao_quadrado:
                return False
        return True

    def intersecta_retangulo(self, outro):
        """Verifica se este retângulo se cruza com outro retângulo."""
        # Não há sobreposição se um retângulo estiver à esquerda do outro
        if self.x + self.w < outro.x - outro.w or self.x - self.w > outro.x + outro.w:
            return False
        # Não há sobreposição se um retângulo estiver acima do outro
        if self.y + self.h < outro.y - outro.h or self.y - self.h > outro.y + outro.h:
            return False
        return True
        
    def contem_retangulo(self, outro):
        """Verifica se este retângulo contém totalmente outro retângulo."""
        return (self.x - self.w <= outro.x - outro.w and
                self.x + self.w >= outro.x + outro.w and
                self.y - self.h <= outro.y - outro.h and
                self.y + self.h >= outro.y + outro.h)


class QuadTree:
    """
    A classe QuadTree.
    """
    def __init__(self, fronteira, profundidade_maxima=8, profundidade=0):
        self.fronteira = fronteira
        self.profundidade_maxima = profundidade_maxima
        self.profundidade = profundidade
        self.filhos = []
        self.e_folha = True

    def subdividir(self):
        """
        Divide o nó atual em quatro quadrantes (filhos) iguais.
        """
        centro_x, centro_y = self.fronteira.x, self.fronteira.y
        nova_largura, nova_altura = self.fronteira.w / 2, self.fronteira.h / 2
        proxima_profundidade = self.profundidade + 1

        # Cria os quatro filhos
        ne = Retangulo(centro_x + nova_largura, centro_y + nova_altura, nova_largura, nova_altura)
        self.filhos.append(QuadTree(ne, self.profundidade_maxima, proxima_profundidade))
        
        no = Retangulo(centro_x - nova_largura, centro_y + nova_altura, nova_largura, nova_altura)
        self.filhos.append(QuadTree(no, self.profundidade_maxima, proxima_profundidade))

        se = Retangulo(centro_x + nova_largura, centro_y - nova_altura, nova_largura, nova_altura)
        self.filhos.append(QuadTree(se, self.profundidade_maxima, proxima_profundidade))

        so = Retangulo(centro_x - nova_largura, centro_y - nova_altura, nova_largura, nova_altura)
        self.filhos.append(QuadTree(so, self.profundidade_maxima, proxima_profundidade))
        
        self.e_folha = False

    def refinar(self, formas):
        """
        Refina recursivamente a quadtree com base na interseção com as fronteiras de uma lista de formas (círculos ou retângulos).
        """
        if self.profundidade >= self.profundidade_maxima:
            return

        deve_subdividir = False
        for forma in formas:
            intersecta = False
            # Lógica de refinamento: subdividir se a fronteira do nó da árvore
            # cruza a borda de uma forma (i.e., intersecta mas não está totalmente contida)
            if isinstance(forma, Circulo):
                if self.fronteira.intersecta_circulo(forma) and not self.fronteira.esta_totalmente_contido_no_circulo(forma):
                    deve_subdividir = True
                    break
            elif isinstance(forma, Retangulo):
                # Para retângulos, subdividimos se a fronteira do nó cruza a construção
                # e a construção não contém completamente o nó (ou seja, cruza a borda).
                if self.fronteira.intersecta_retangulo(forma) and not forma.contem_retangulo(self.fronteira):
                    deve_subdividir = True
                    break
        
        if deve_subdividir:
            self.subdividir()
            for filho in self.filhos:
                filho.refinar(formas)

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