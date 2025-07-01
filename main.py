import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math
from quadtree import Ponto, Circulo, Retangulo, QuadTree

def desenhar_quadtree(ax, nos_folha, circulos, pontos):
    """
    Plota os nós folha da quadtree, círculos e pontos, colorindo as sobreposições.
    """
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 200)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title("Plotagem da Quadtree") # Particionamento Quadtree para Múltiplas Fronteiras de Círculos

    # Define cores para diferentes níveis de sobreposição
    cores_sobreposicao = ['none', 'lightblue', 'cornflowerblue', 'royalblue', 'darkblue']

    # Plota os nós folha
    for no in nos_folha:
        fronteira = no.fronteira
        
        # Conta em quantos círculos a fronteira deste nó está totalmente contida
        contagem_contidos = 0
        for circulo in circulos:
            if fronteira.esta_totalmente_contido_no_circulo(circulo):
                contagem_contidos += 1
        
        # Limita a contagem ao número de cores disponíveis
        indice_cor = min(contagem_contidos, len(cores_sobreposicao) - 1)
        cor_preenchimento = cores_sobreposicao[indice_cor]

        retangulo_patch = patches.Rectangle(
            (fronteira.x - fronteira.w, fronteira.y - fronteira.h), # Canto inferior esquerdo
            fronteira.w * 2,               # Largura
            fronteira.h * 2,               # Altura
            facecolor=cor_preenchimento,
            edgecolor='black',
            linewidth=0.5
        )
        ax.add_patch(retangulo_patch)
        
    # Plota os pontos aleatórios
    for ponto in pontos:
        ax.plot(ponto.x, ponto.y, 'gx', markersize=8, markeredgewidth=2) # 'x' verde para os pontos

    # Plota os círculos por cima para maior clareza
    for circulo in circulos:
        circulo_patch = patches.Circle((circulo.x, circulo.y), circulo.raio, facecolor='none', edgecolor='red', linewidth=2, alpha=0.8)
        ax.add_patch(circulo_patch)


if __name__ == '__main__':
    # 1. Define a fronteira principal de todo o espaço
    # É uma região de 200x200 com seu centro em (100, 100)
    fronteira_principal = Retangulo(100, 100, 100, 100)

    # 2. Cria a raiz da QuadTree
    # Uma profundidade_maxima maior torna as caixas de fronteira mais precisas.
    arvore_quad = QuadTree(fronteira_principal, profundidade_maxima=8)

    # 3. Define uma lista de círculos aleatórios para particionar ao redor
    formas_circulo = []
    num_circulos = 3
    for i in range(num_circulos):
        x_aleatorio = random.randint(50, 150)
        y_aleatorio = random.randint(50, 150)
        raio_aleatorio = random.randint(20, 45)
        formas_circulo.append(Circulo(x_aleatorio, y_aleatorio, raio_aleatorio))

    # 4. Refina a QuadTree
    # A árvore se subdividirá onde quer que cruze com a fronteira de qualquer círculo.
    arvore_quad.refinar(formas_circulo)

    # 5. Obtém todos os nós folha finais da árvore
    nos_folha = arvore_quad.obter_nos_folha()

    # 6. Gera pontos aleatórios e os verifica
    pontos_para_verificar = []
    num_pontos = 5
    print("-" * 40)
    for i in range(num_pontos):
        ponto = Ponto(random.randint(0, 200), random.randint(0, 200))
        pontos_para_verificar.append(ponto)
        
        print(f"\nVerificando Ponto {i+1} em ({ponto.x:.2f}, {ponto.y:.2f})")

        esta_contido = False
        for j, circulo in enumerate(formas_circulo):
            if circulo.contem_ponto(ponto):
                print(f"  -> Contido no Círculo {j+1}")
                esta_contido = True
        
        if not esta_contido:
            print("  -> Não contido em nenhum círculo.")

    # 7. Plota os resultados
    fig, ax = plt.subplots(figsize=(10, 10))
    desenhar_quadtree(ax, nos_folha, formas_circulo, pontos_para_verificar)
    plt.show()