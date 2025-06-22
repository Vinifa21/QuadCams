#PR QUAD-TREE:
#   CHAVES SÓ ESTÃO GUARDADAS NAS FOLHAS
#   TAMANHO DO "PLANO" DEVE ESTAR DEFINIDO (256x256)?
#   representacao diferente de internal Node e leaf node

from ponto import Ponto
from nodes import Node_folha, Node_interno
class Quad_Tree:
    def __init__(self, top_left = Ponto(-128, 128), lado = 256):
        #definem limites do plano
        self.top_left = top_left
        self.lado = lado
        self.root = None

    def add_ponto(self, ponto): # método público (que chamaremos na main)
        current = self.root

        self.root = self.add_ponto_recursivo(ponto, current, Ponto(-128, 128), 256)


# preciso descobrir como fazer a comparação em add_ponto_recursivo (decidir p/ qual quadrante vou)

    def add_ponto_recursivo(self, ponto, c, top_left, lado):  # método private( chamado internamete para realizar a recursão)
        current = c
        # caso base: acho um node_interno vazio (com None) para inserir o ponto
        # caso recursivo: de acordo com as coordenadas, ando para próximo node
            # OU acho node vazio (caso base)
            # OU acho Node Interno (escolho uma direção)
            # OU, acho um Node Folha (o troco por um interno, e re-insiro o ponto antigo e o novo ponto)

        if current is None:  # achei lugar para inserir o ponto!
            current = Node_folha(ponto)
            return current # retorna minha folha recém-criada

        elif isinstance(current, Node_interno):  # current é um node interno?
            mid_x = top_left.x + (lado / 2)
            mid_y = top_left.y + (lado / 2)  # <<-- SEMPRE SOMANDO!

            # verifico para qual quadrante eu vou (facil de entender if's com desenho da tree)
            if (ponto.x >= mid_x and ponto.y < mid_y ):
                novo_top_left = Ponto(mid_x, top_left.y) # y se mantém
                novo_lado = lado / 2
                current.NE = self.add_ponto_recursivo(ponto, current.NE, novo_top_left, novo_lado)
                #current.NE salva qual é o filho à Nordeste (caso lá já seja None) (caso não seja None, retorna seu atual filho NE msm)

            elif (ponto.x < mid_x and ponto.y < mid_y ):
                novo_top_left = top_left  # top_left se mantém
                novo_lado = lado / 2
                current.NW = self.add_ponto_recursivo(ponto, current.NW, novo_top_left, novo_lado)

            elif (ponto.x < mid_x and ponto.y >= mid_y ):
                # x se mantém
                novo_top_left = Ponto(top_left.x, mid_y)
                novo_lado = lado / 2
                current.SW = self.add_ponto_recursivo(ponto, current.SW, novo_top_left, novo_lado)

            elif (ponto.x >= mid_x and ponto.y >= mid_y ):
                novo_top_left = Ponto(mid_x, mid_y)
                novo_lado = lado / 2
                current.SE = self.add_ponto_recursivo(ponto, current.SE, novo_top_left, novo_lado)

        elif isinstance(current, Node_folha):  # current é um Node_folha (possui uma key)
            ponto_existente = current.ponto
            novo_node_interno = Node_interno(top_left, lado)

            self.add_ponto_recursivo(ponto_existente, novo_node_interno, top_left, lado)# re-insiro meu ponto antigo
            self.add_ponto_recursivo(ponto, novo_node_interno, top_left, lado) # insiro meu ponto novo

            return novo_node_interno # vai ser pego pelo current.NE = (ISSO)



            # preciso transforma-lo num nó intermediário e reinserir sua chave(temp)+ a nova chave
            temp = current.key
            current = Node_interno()
            self.add_ponto_recursivo(temp, current, top_left, lado)  # adicono ponto antigo
            self.add_ponto_recursivo(ponto, current, top_left, lado)  # adiciono meu novo ponto

        return current # novo node inserido, retorno a root atualizada para a função add_ponto
##########


