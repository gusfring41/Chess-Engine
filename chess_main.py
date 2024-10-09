
'''

TABULEIRO : matriz de objetos

 -6, -5, -4, -3, -2, -4, -5, -6,                               
 -1, -1, -1, -1, -1, -1, -1, -1,  
  0,  0,  0,  0,  0,  0,  0,  0,  
  0,  0,  0,  0,  0,  0,  0,  0,  
  0,  0,  0,  0,  0,  0,  0,  0,  
  0,  0,  0,  0,  0,  0,  0,  0,  
  1,  1,  1,  1,  1,  1,  1,  1,  
  6,  5,  4,  3,  2,  4,  5,  6,  

a matriz serve apenas para visualização, cada peça é um objeto de uma classe denominada Peça

atributos de cada objeto:

1)tipo:
1: peão     4: bispo
2: rei      5: cavalo
3: rainha   6: torre

2)pos_in_linha e pos_in_col: indice inicial referente à linha/coluna na matriz

3)imagem: png da peça

4)roque e en passant: atributos para ajudar na programação dessas 2 regras
->se a torre e o rei ainda não tiverem se mexido, o valor de roque deles é igual a 1, ou seja, eles podem rocar, caso o contrário é igual a 0
->se o peão mover 2 casas para frente, naquele momento o seu valor de en passant passa a valer 1 e , se tiver um peão inimigo ao seu lado, ele pode comer e após o movimento do adversário, o valor de en passant volta a ser 0 para tal peão

5)promoção: se um peão chegar na última fileira, seu valor de promoção vale 1 e o programa fornece uma escolha de peça para promover

formato do movimento: [(ind. final linha - ind. inicial linha) , (ind. final coluna - ind. final coluna)]
ex: se temos uma peça na posição [6,2] e queremos mover para [6,3], o movimento deve ser [0,1]

cada peça tem uma lista de movimentos possíveis
ex: rei , pode se mover 1 casa em qualquer direção, logo sua lista de movimentos possíveis inicial é [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]

o jogo tem 3 estados: normal, xeque, xeque-mate:
->no modo normal é permitido realizar qualquer movimento desde que ele seja válido
->no modo de xeque o jogador precisa fazer uma jogada que bloqueie o ataque adversário
->no modo de xeque-mate o jogo acaba

''' 

import os
import pygame
import sys
import random

pygame.init()

# definição da classe peça
class Peca:
    def __init__(self, tipo, pos_in_linha, pos_in_col, imagem, roque, enpassant):
      self.tipo = tipo
      self.pos_in_linha = pos_in_linha
      self.pos_in_col = pos_in_col
      self.imagem = imagem
      self.roque = roque
      self.enpassant = enpassant  
    def __int__(self):
      return self.tipo
    def copy(self):
      return Peca(self.tipo, self.pos_in_linha, self.pos_in_col, self.imagem, self.roque, self.enpassant)

rei_preto = ()
rei_branco = ()
rei_preto_copia = ()
rei_branco_copia = ()

# carregando png de cada peça(todas as peças são 70x70)
# nota: fazer um dicionario com as imagens depois
def achar_imagem(tipo_peca):

  if tipo_peca > 0:
    if tipo_peca == 1:
      imagem_peca = pygame.image.load("pieces-png/white-pawn.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    elif tipo_peca == 2:
      imagem_peca = pygame.image.load("pieces-png/white-king.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    elif tipo_peca == 3:
      imagem_peca = pygame.image.load("pieces-png/white-queen.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    elif tipo_peca == 4:
      imagem_peca = pygame.image.load("pieces-png/white-bishop.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    elif tipo_peca == 5:
      imagem_peca = pygame.image.load("pieces-png/white-knight.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    else:
      imagem_peca = pygame.image.load("pieces-png/white-rook.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca

  else:
    if tipo_peca == -1:
      imagem_peca = pygame.image.load("pieces-png/black-pawn.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    elif tipo_peca == -2:
      imagem_peca = pygame.image.load("pieces-png/black-king.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    elif tipo_peca == -3:
      imagem_peca = pygame.image.load("pieces-png/black-queen.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    elif tipo_peca == -4:
      imagem_peca = pygame.image.load("pieces-png/black-bishop.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    elif tipo_peca == -5:
      imagem_peca = pygame.image.load("pieces-png/black-knight.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    else:
      imagem_peca = pygame.image.load("pieces-png/black-rook.png")
      imagem_peca = pygame.transform.smoothscale(imagem_peca ,(70, 70))
      return imagem_peca
    
# macro para limpar tela  
def limpar_tela():
  os.system('cls' if os.name == 'nt' else 'clear')

# função para veririficar se o movimento cogitado está nos limites da matriz(0 a 7) 
def verif_mov_tab(linha_peca, coluna_peca, mov):
  return 0 <= linha_peca + mov[0] <= 7 and 0 <= coluna_peca + mov[1] <= 7

# função para retornar cor da peça(1 branco 0 preto)
def cor_peca(peca):
  if(peca.tipo > 0):
    return 1
  else:
    return -1
  
# função para gerar casas (x, y) atacadas pelo inimigo/jogador após movimento
def casas_atacadas(matrizt, menor_init, maior_init, jogadort, vezt):
    
    lista_ataque_inimigo = []
    for i in range(8):
      for j in range(8):
        if(matrizt[i][j] != 0):
          if(menor_init <= matrizt[i][j].tipo <= maior_init):
            lista_ataques_peca = gerar_movimentos_possiveis_peca(matrizt, matrizt[i][j], jogadort, vezt, 1)  
            if(lista_ataques_peca is not None):
              for mov in lista_ataques_peca:
                # as casas atacadas para a lista de ataque inimigo após a sua movimentação
                if(not ((abs(matrizt[i][j].tipo) == 1) and (mov[0] != 0))):
                  lista_ataque_inimigo.append((i+mov[0], j+mov[1]))
                # se for um avanço de peão, verifica se é possível atacar as diagonais
                elif(abs(mov[0]) == 1):
                  mov_atq_peao = [[mov[0], 1],[mov[0], -1]]
                  for movs in mov_atq_peao:
                    if(verif_mov_tab(i, j, movs)):
                      lista_ataque_inimigo.append((i+movs[0], j+movs[1]))

    # algoritmo para tirar casas repetidas
    lista_ataque_inimigo = list(set(lista_ataque_inimigo))            

    if(len(lista_ataque_inimigo) > 0):
      return lista_ataque_inimigo
    else:
      return None

# verifica se, após o movimento, o rei está em xeque(caso esteja, anula o movimento), simulando em uma cópia da matriz do jogo 
def verif_xeque(matrizx, peca_movidax, movx, jogadorx, vez):

  global rei_preto_copia, rei_branco_copia, rei
  rei_preto_copia = rei_preto
  rei_branco_copia = rei_branco

  matriz_copia = []
  for linha in matrizx:
      nova_linha = []
      for item in linha:
          if isinstance(item, Peca):
              nova_linha.append(Peca(tipo = item.tipo, pos_in_linha = item.pos_in_linha, pos_in_col = item.pos_in_col, imagem = item.imagem, roque = item.roque, enpassant = item.enpassant))
          else:
              nova_linha.append(item)  # Para itens que não são peças, copie diretamente
      matriz_copia.append(nova_linha)

  if(jogadorx == 0):
    rei_jog = rei_preto_copia
    rei_ini = rei_branco_copia
    if(vez != jogadorx):
      rei = rei_ini
      menor_inix = -6
      maior_inix = -1
    else:
      rei = rei_jog
      menor_inix = 1
      maior_inix = 6
  else:
    rei_jog = rei_branco_copia
    rei_ini = rei_preto_copia
    if(vez != jogadorx):
      rei = rei_ini
      menor_inix = 1
      maior_inix = 6
    else:
      rei = rei_jog
      menor_inix = -6
      maior_inix = -1

  # realiza o movimento cogitado através de uma cópia da matriz original
  movimento_basico_copia(matriz_copia, peca_movidax, movx, jogadorx)

  lista_ataque_oposto = casas_atacadas(matriz_copia, menor_inix, maior_inix, jogadorx, vez)

  for casa in lista_ataque_oposto:
    if(casa == rei):
      print("o rei está atacado com esse movimento, posição do rei: ", rei)
      return False
  return True

# movimento básico de substituição entre 2 posições em uma matriz cópia(nota: atualizar en passant)
def movimento_basico_copia(matrizb, peca_movidab, movb, jogadorb):
    
  global rei_preto_copia, rei_branco_copia , rei
  peca_copia = peca_movidab.copy()

  # ve a linha/coluna da peça
  linha_peca = peca_copia.pos_in_linha
  coluna_peca = peca_copia.pos_in_col

  # atualiza a nova linha/coluna da peça
  peca_copia.pos_in_linha = linha_peca+movb[0]
  peca_copia.pos_in_col = coluna_peca+movb[1]

  # troca a peça de lugar na matriz, deixando o espaço onde ela estava como 0(sem peça na casa)
  peca_inimiga = matrizb[linha_peca+movb[0]][coluna_peca+movb[1]]
  matrizb[linha_peca][coluna_peca] = 0
  matrizb[linha_peca+movb[0]][coluna_peca+movb[1]] = peca_copia

  # se houve movimento, verifica se o movimento foi de uma torre, nesse caso a possibilidades de roque e grande roque são alteradas(a verificação do rei é feita na função de mov do rei)
  if(abs(peca_copia.tipo) == 6):
    peca_copia.roque = 0
  elif(abs(peca_copia.tipo) == 2):
    # como o rei se movimentou, não há mais possibilidade de roque e a sua posição é atualizada
    peca_copia.roque = 0
    if(peca_copia.tipo < 0):
      rei_preto_copia = (linha_peca+movb[0], coluna_peca+movb[1])
      rei = rei_preto_copia
    else:
      rei_branco_copia = (linha_peca+movb[0], coluna_peca+movb[1])
      rei = rei_branco_copia
    # se o movimento for um roque, também é feita uma movimentação na torre
    if(jogadorb == 0):
      if(movb == [0, 2]):
        movimento_basico_copia(matrizb, matrizb[linha_peca][coluna_peca+4], [0, -3], jogadorb)
      elif(movb == [0, -2]):
        movimento_basico_copia(matrizb, matrizb[linha_peca][coluna_peca-3], [0, 2], jogadorb)
    elif(jogadorb == 1):
      if(movb == [0, 2]):
        movimento_basico_copia(matrizb, matrizb[linha_peca][coluna_peca+3], [0, -2], jogadorb)
      elif(movb == [0, -2]):
        movimento_basico_copia(matrizb, matrizb[linha_peca][coluna_peca-4], [0, 3], jogadorb)
  elif(abs(peca_copia.tipo) == 1):
    # o peão só alcança essas linhas em caso de promoção,e quando alcançar troca a sua imagem e seu tipo
    if(peca_copia.pos_in_linha == 0) or (peca_copia.pos_in_linha == 7):
      promocao_peao(peca_copia, cor_peca(peca_copia))
    # atualiza en passant se o primeiro movimento for 2 casa para frente
    if(movb == [2,0]) or (movb == [-2,0]):
      peca_copia.enpassant = 1
    elif(movb[1] != 0) and (peca_inimiga == 0):
      # come o peão caso tenha realizado en passant
      matrizb[linha_peca][coluna_peca+movb[1]] = 0

# movimento básico de substituição entre 2 posições(nota: atualizar en passant)
def movimento_basico(matriz, peca_movida, mov, jogador):
    
  global rei_preto, rei_branco
  # ve a linha/coluna da peça
  linha_peca = peca_movida.pos_in_linha
  coluna_peca = peca_movida.pos_in_col

  # atualiza a nova linha/coluna da peça
  peca_movida.pos_in_linha = linha_peca+mov[0]
  peca_movida.pos_in_col = coluna_peca+mov[1]

  # troca a peça de lugar na matriz, deixando o espaço onde ela estava como 0(sem peça na casa)
  peca_inimiga = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
  matriz[linha_peca][coluna_peca] = 0
  matriz[linha_peca+mov[0]][coluna_peca+mov[1]] = peca_movida

  # se houve movimento, verifica se o movimento foi de uma torre, nesse caso a possibilidades de roque e grande roque são alteradas(a verificação do rei é feita na função de mov do rei)
  if(abs(peca_movida.tipo) == 6):
    peca_movida.roque = 0
  elif(abs(peca_movida.tipo) == 2):
    # como o rei se movimentou, não há mais possibilidade de roque e a sua posição é atualizada
    peca_movida.roque = 0
    if(peca_movida.tipo < 0):
      rei_preto = (linha_peca+mov[0], coluna_peca+mov[1])
    else:
      rei_branco = (linha_peca+mov[0], coluna_peca+mov[1])
    # se o movimento for um roque, também é feita uma movimentação na torre
    if(jogador == 0):
      if(mov == [0, 2]):
        movimento_basico(matriz, matriz[linha_peca][coluna_peca+4], [0, -3], jogador)
      elif(mov == [0, -2]):
        movimento_basico(matriz, matriz[linha_peca][coluna_peca-3], [0, 2], jogador)
    elif(jogador == 1):
      if(mov == [0, 2]):
        movimento_basico(matriz, matriz[linha_peca][coluna_peca+3], [0, -2], jogador)
      elif(mov == [0, -2]):
        movimento_basico(matriz, matriz[linha_peca][coluna_peca-4], [0, 3], jogador)
  elif(abs(peca_movida.tipo) == 1):

    # o peão só alcança essas linhas em caso de promoção,e quando alcançar troca a sua imagem e seu tipo
    if(peca_movida.pos_in_linha == 0) or (peca_movida.pos_in_linha == 7):
      promocao_peao(peca_movida, cor_peca(peca_movida))
    # atualiza en passant se o primeiro movimento for 2 casa para frente
    if(mov == [2,0]) or (mov == [-2,0]):
      peca_movida.enpassant = 1
    elif(mov[1] != 0) and (peca_inimiga == 0):
      # come o peão caso tenha realizado en passant
      matriz[linha_peca][coluna_peca+mov[1]] = 0

# gera todos os movimentos possíveis de todas as peças da cor em questão para a IA(formato: [i_peca, j_peca, mov[0], mov[1]])
def gerar_todos_movimentos_possiveis(matrizg, menor_inig, maior_inig, jogadorg, vez_jogg):
    lista_todos_mov = []
    for i in range(8):
      for j in range(8):
        if(matrizg[i][j] != 0):
          if(menor_inig <= matrizg[i][j].tipo <= maior_inig):
            lista_movimentos_peca = gerar_movimentos_possiveis_peca(matrizg, matrizg[i][j], jogadorg, vez_jogg, 0)
            if(lista_movimentos_peca is not None):
              for mov in lista_movimentos_peca:
                # adiciona os movimentos possíveis pra a lista de mov adversário
                lista_todos_mov.append([i, j, mov[0], mov[1]])
    
    if(len(lista_todos_mov) > 0):
      return lista_todos_mov
    else:
      return None

# gera todos os movimentos possíveis para a peça da cor em questão
def gerar_movimentos_possiveis_peca(matriz, peca_movida, jogador, vez_jog, verif_ini):
    
  # ve a linha/coluna da peça
  lista_mov_possiveis = []
  linha_peca = peca_movida.pos_in_linha
  coluna_peca = peca_movida.pos_in_col 
  cor = cor_peca(peca_movida)

  if abs(peca_movida.tipo) == 1:      # peão

    # movimentos iniciais possiveis para um peão(pra frente e pra diagonal) 

    if(jogador == 0):  
      mov_possiveis_iniciais_preto = [[-1,0],[-1,1],[-1,-1]]
      mov_possiveis_iniciais_branco = [[1,0],[1,1],[1,-1]]
    else:
      mov_possiveis_iniciais_preto = [[1,0],[1,1],[1,-1]]
      mov_possiveis_iniciais_branco =  [[-1,0],[-1,1],[-1,-1]]

    if(cor == 1):                     # peão branco

      # se estiver na linha inicial e estiver vazio  na frente, pode pular 2 casas
      if((linha_peca == 6) and (jogador == 1) and (matriz[linha_peca-1][coluna_peca] == 0)):
        mov_possiveis_iniciais_branco.append([-2,0])
      elif((linha_peca == 1) and (jogador == 0) and (matriz[linha_peca+1][coluna_peca] == 0)):
        mov_possiveis_iniciais_branco.append([2,0])
      
      for mov in mov_possiveis_iniciais_branco:
        
        if(verif_mov_tab(linha_peca, coluna_peca, mov)):
          
          # se ele não move na coluna, então ele está indo para frente e verificamos se o espaço está vazio para passar
          if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] == 0 and mov[1] == 0):
            lista_mov_possiveis.append(mov)
          # se ele move, então é um movimento de captura e verificamos se o espaço está ocupado por uma peça inimiga ou se é um en pssant
          elif(mov[1] != 0):
            if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] != 0):
              peca_diagonal = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
              cor_peca_diagonal = cor_peca(peca_diagonal)
              if(cor_peca_diagonal != cor):
                lista_mov_possiveis.append(mov)
            elif(matriz[linha_peca][coluna_peca+mov[1]] !=  0) and (matriz[linha_peca][coluna_peca+mov[1]].enpassant == 1):
              peca_lateral = matriz[linha_peca][coluna_peca+mov[1]]
              cor_peca_lateral = cor_peca(peca_lateral)
              if(cor_peca_lateral != cor):
                lista_mov_possiveis.append(mov)

    else:                               # peão preto
      
      # se estiver na linha inicial e estiver vazio na frente, pode pular 2 casas
      if((linha_peca == 6) and (jogador == 0) and (matriz[linha_peca-1][coluna_peca] == 0)):
        mov_possiveis_iniciais_preto.append([-2,0])
      elif((linha_peca == 1) and (jogador == 1) and (matriz[linha_peca+1][coluna_peca] == 0)):
        mov_possiveis_iniciais_preto.append([2,0])

      for mov in mov_possiveis_iniciais_preto:
          
        if(verif_mov_tab(linha_peca, coluna_peca, mov)):

          # se ele não move na coluna, então ele está indo para frente e verificamos se o espaço está vazio para passar
          if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] == 0 and mov[1] == 0):
            lista_mov_possiveis.append(mov)
          # se ele move, então é um movimento de captura e verificamos se o espaço está ocupado por uma peça inimiga ou se é um en pssant
          elif(mov[1] != 0):
            if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] != 0):
              peca_diagonal = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
              cor_peca_diagonal = cor_peca(peca_diagonal)
              if(cor_peca_diagonal != cor):
                lista_mov_possiveis.append(mov)
            elif(matriz[linha_peca][coluna_peca+mov[1]] !=  0) and (matriz[linha_peca][coluna_peca+mov[1]].enpassant == 1):
              peca_lateral = matriz[linha_peca][coluna_peca+mov[1]]
              cor_peca_lateral = cor_peca(peca_lateral)
              if(cor_peca_lateral != cor):
                lista_mov_possiveis.append(mov)   

  elif abs(peca_movida.tipo) == 2:       # rei

    # movimentos iniciais possiveis para um rei(1 casa em qualquer direção, ataca nessas casas também)
    movimentos_iniciais_rei = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]

    for mov in movimentos_iniciais_rei:

      if(verif_mov_tab(linha_peca, coluna_peca, mov)):

        if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] == 0):
          lista_mov_possiveis.append(mov)
        else:
          peca_alvo = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
          cor_peca_alvo = cor_peca(peca_alvo)
          if(cor_peca_alvo != cor):
              lista_mov_possiveis.append(mov)

    # verificação do roque e do grande roque

    movimentos_roque = [[0,2], [0, -2]]

    if(verif_ini == 0):
  
      for mov_roq in movimentos_roque:
        if(verif_mov_tab(linha_peca, coluna_peca, mov_roq)):

          # veririfica se o rei já moveu e se as casas ao seu lado estão vazias

          if(matriz[linha_peca][coluna_peca+(1*mov_roq[1]//2)] == 0) and (matriz[linha_peca][coluna_peca+(2*mov_roq[1]//2)] == 0) and (peca_movida.roque == 1):
            # se a torre estiver no canto do tabuleiro e não tiver se movido ainda e as casas que o rei vai andar não estiverem atacadas(em xeque), o roque é possível
            # a verificação da casa (0, 2) é feita mais tarde no código a partir do ataque das casas inimigas
            if(jogador == 0):
              if(mov_roq[1] == 2):
                if(matriz[linha_peca][7] != 0) and (abs(matriz[linha_peca][7].tipo) == 6) and (matriz[linha_peca][7].roque == 1) and (matriz[linha_peca][coluna_peca+3] == 0):
                  if(verif_xeque(matriz, matriz[linha_peca][coluna_peca], (0, 0), jogador, vez_jog)) and (verif_xeque(matriz, matriz[linha_peca][coluna_peca], (0, 1), jogador, vez_jog)):
                    print("roque grande adicionado, o rei do", jogador, vez_jog,"esta tranquilo nessas casa", linha_peca, coluna_peca, linha_peca, coluna_peca+1)
                    lista_mov_possiveis.append(mov_roq)
              elif(mov_roq[1] == -2):
                if(matriz[linha_peca][0] != 0) and (abs(matriz[linha_peca][0].tipo) == 6) and (matriz[linha_peca][0].roque == 1):
                  if(verif_xeque(matriz, matriz[linha_peca][coluna_peca], (0, 0), jogador, vez_jog)) and (verif_xeque(matriz, matriz[linha_peca][coluna_peca], (0, -1), jogador, vez_jog)):
                    print("roque pequeno adicionado, o rei do", jogador, vez_jog,"esta tranquilo nessas casas", linha_peca, coluna_peca, linha_peca, coluna_peca-1)
                    lista_mov_possiveis.append(mov_roq)
            else:
              if(mov_roq[1] == 2):
                if(matriz[linha_peca][7] != 0) and (abs(matriz[linha_peca][7].tipo) == 6) and (matriz[linha_peca][7].roque == 1):
                  if(verif_xeque(matriz, matriz[linha_peca][coluna_peca], (0, 0), jogador, vez_jog)) and (verif_xeque(matriz, matriz[linha_peca][coluna_peca], (0, 1), jogador, vez_jog)):
                    print("roque pequeno adicionado, o rei do", jogador, vez_jog,"esta tranquilo nessas casas", linha_peca, coluna_peca, linha_peca, coluna_peca+1)
                    lista_mov_possiveis.append(mov_roq)
              elif(mov_roq[1] == -2):
                if(matriz[linha_peca][0] != 0) and (abs(matriz[linha_peca][0].tipo) == 6) and (matriz[linha_peca][0].roque == 1) and (matriz[linha_peca][coluna_peca-3] == 0):
                  if(verif_xeque(matriz, matriz[linha_peca][coluna_peca], (0, 0), jogador, vez_jog)) and (verif_xeque(matriz, matriz[linha_peca][coluna_peca], (0, -1), jogador, vez_jog)):
                    print("roque grande adicionado, o rei do", jogador, vez_jog,"esta tranquilo nessas casas", linha_peca, coluna_peca, linha_peca, coluna_peca-1)
                    lista_mov_possiveis.append(mov_roq)
  
  elif abs(peca_movida.tipo) == 3:        # rainha
    
    # movimentos iniciais possiveis para uma rainha(ao longo da sua diagonal e na vertical/horizontal, ataca nessas casas também)
    movimentos_iniciais_dama = [[[ 1, 1],[ 2, 2],[ 3, 3],[ 4, 4],[ 5, 5],[ 6, 6],[ 7, 7]],
                                [[ 1,-1],[ 2,-2],[ 3,-3],[ 4,-4],[ 5,-5],[ 6,-6],[ 7,-7]],
                                [[-1, 1],[-2, 2],[-3, 3],[-4, 4],[-5, 5],[-6, 6],[-7, 7]],
                                [[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]],
                                [[ 0, 1],[ 0, 2],[ 0, 3],[ 0, 4],[ 0, 5],[ 0, 6],[ 0, 7]],
                                [[ 1, 0],[ 2, 0],[ 3, 0],[ 4, 0],[ 5, 0],[ 6, 0],[ 7, 0]],
                                [[-1, 0],[-2, 0],[-3, 0],[-4, 0],[-5, 0],[-6, 0],[-7, 0]],
                                [[ 0,-1],[ 0,-2],[ 0,-3],[ 0,-4],[ 0,-5],[ 0,-6],[ 0,-7]]]
    
    for linha in movimentos_iniciais_dama:
      # para cada linha, ele vai verificar até achar uma peça no meio do caminho da dama e vai dar brake, já que a dama não pula peças
      for mov in linha:
        if(verif_mov_tab(linha_peca, coluna_peca, mov)):

          if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] == 0):
            lista_mov_possiveis.append(mov)

          else:
            peca_alvo = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
            cor_peca_alvo = cor_peca(peca_alvo)
            if(cor_peca_alvo != cor):
                lista_mov_possiveis.append(mov)
            break
        else:
          break

  elif abs(peca_movida.tipo) == 4:        # bispo

    # movimentos iniciais possiveis para um bispo(ao longo da sua diagonal, ataca nessas casas também)
    movimentos_iniciais_bispo = [[[ 1, 1],[ 2, 2],[ 3, 3],[ 4, 4],[ 5, 5],[ 6, 6],[ 7, 7]],
                                 [[ 1,-1],[ 2,-2],[ 3,-3],[ 4,-4],[ 5,-5],[ 6,-6],[ 7,-7]],
                                 [[-1, 1],[-2, 2],[-3, 3],[-4, 4],[-5, 5],[-6, 6],[-7, 7]],
                                 [[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]]]
    
    for diagonal in movimentos_iniciais_bispo:
      # para cada diagonal, ele vai verificar até achar uma peça no meio do caminho do bispo e vai dar brake, já que o bispo não pula peças
      for mov in diagonal:
        if(verif_mov_tab(linha_peca, coluna_peca, mov)):

          if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] == 0):
            lista_mov_possiveis.append(mov)

          else:
            peca_alvo = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
            cor_peca_alvo = cor_peca(peca_alvo)
            if(cor_peca_alvo != cor):
                lista_mov_possiveis.append(mov)
            break
        else:
          break

  elif abs(peca_movida.tipo) == 5:        # cavalo
    # movimentos iniciais possiveis para um cavalo(L, ataca nessas casas também, além de poder pular as casas)
    movimentos_iniciais_cavalo = [[1,2], [1,-2], [-1,2], [-1,-2], [2,1], [2,-1], [-2,1], [-2,-1]]

    for mov in movimentos_iniciais_cavalo:
      if(verif_mov_tab(linha_peca, coluna_peca, mov)):
        
        if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] == 0):
          lista_mov_possiveis.append(mov)

        else:
          peca_alvo = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
          cor_peca_alvo = cor_peca(peca_alvo)
          if(cor_peca_alvo != cor):
              lista_mov_possiveis.append(mov)


  elif abs(peca_movida.tipo) == 6:        # torre

    # movimentos iniciais possiveis para um torre(ao longo da vertical/horizontal, ataca nessas casas também)
    movimentos_iniciais_torre = [[[ 0, 1],[ 0, 2],[ 0, 3],[ 0, 4],[ 0, 5],[ 0, 6],[ 0, 7]],
                                 [[ 1, 0],[ 2, 0],[ 3, 0],[ 4, 0],[ 5, 0],[ 6, 0],[ 7, 0]],
                                 [[-1, 0],[-2, 0],[-3, 0],[-4, 0],[-5, 0],[-6, 0],[-7, 0]],
                                 [[ 0,-1],[ 0,-2],[ 0,-3],[ 0,-4],[ 0,-5],[ 0,-6],[ 0,-7]]]
    
    for reta in movimentos_iniciais_torre:
      # para cada reta, ele vai verificar até achar uma peça no meio do caminho do bispo e vai dar brake, já que o bispo não pula peças
      for mov in reta:
        if(verif_mov_tab(linha_peca, coluna_peca, mov)):

          if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] == 0):
            lista_mov_possiveis.append(mov)

          else:
            peca_alvo = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
            cor_peca_alvo = cor_peca(peca_alvo)
            if(cor_peca_alvo != cor):
                lista_mov_possiveis.append(mov)
            break
        else:
          break

  if(len(lista_mov_possiveis) > 0):
    return lista_mov_possiveis
  else:
    return None
  
def promocao_peao(peao, cor_do_peao):
  peao.tipo = cor_do_peao*3
  peao.imagem = achar_imagem(peao.tipo)

# menu screen
pygame.display.set_caption("menu")
menu = pygame.display.set_mode((600, 600))
menu_rodando = True
opcao_jogador = None

while(menu_rodando):

  menu.fill((255, 255, 255))
  offset_yt = -75

  for i in range (8):
    offset_xt = 0
    offset_yt += 75
    for j in range (8):
      if((i+j)%2 == 0):
        pygame.draw.rect(menu, (255, 255, 255), (offset_xt, offset_yt, 75, 75))
      else:
        pygame.draw.rect(menu, (150 , 50, 205), (offset_xt, offset_yt, 75, 75))
      offset_xt += 75

  rei_branco = pygame.image.load("pieces-png/white-king.png")
  rei_branco = pygame.transform.smoothscale(rei_branco ,(70, 70))
  rei_preto = pygame.image.load("pieces-png/black-king.png")
  rei_preto = pygame.transform.smoothscale(rei_preto ,(70, 70))

  menu.blit(rei_branco, (300, 300))
  menu.blit(rei_preto, (225, 225))

  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = pygame.mouse.get_pos()

      if(225 <= mouse_x <= 300) and (225 <= mouse_y <= 300):
        opcao_jogador = 0
      elif(300 <= mouse_x <= 375) and (300 <= mouse_y <= 375):
        opcao_jogador = 1

    elif event.type == pygame.MOUSEBUTTONUP:
      menu_rodando = False

    elif event.type == pygame.QUIT:
      sys.exit()

  pygame.display.flip()

# incializa a matriz_tabuleiro fora do loop do jogo e dos objetos
if(opcao_jogador == 0):
  matriz_tabuleiro_int =  [[ 6,  5,  4,  2,  3,  4,  5,  6],                               
                           [ 1,  1,  1,  1,  1,  1,  1,  1],  
                           [ 0,  0,  0,  0,  0,  0,  0,  0],  
                           [ 0,  0,  0,  0,  0,  0,  0,  0],  
                           [ 0,  0,  0,  0,  0,  0,  0,  0],  
                           [ 0,  0,  0,  0,  0,  0,  0,  0],  
                           [-1, -1, -1, -1, -1, -1, -1, -1],  
                           [-6, -5, -4, -2, -3, -4, -5, -6]] 
  # contém a casa de inicio do rei brnco e do rei preto(importante par verificar cheque etc.)
  rei_preto = (7, 3)
  rei_branco = (0, 3)
else:
  matriz_tabuleiro_int =  [[-6, -5, -4, -3, -2, -4, -5, -6],                               
                           [-1, -1, -1, -1, -1, -1, -1, -1],  
                           [ 0,  0,  0,  0,  0,  0,  0,  0],  
                           [ 0,  0,  0,  0,  0,  0,  0,  0],  
                           [ 0,  0,  0,  0,  0,  0,  0,  0],  
                           [ 0,  0,  0,  0,  0,  0,  0,  0],  
                           [ 1,  1,  1,  1,  1,  1,  1,  1],  
                           [ 6,  5,  4,  3,  2,  4,  5,  6]]
  # contém a casa de inicio do rei brnco e do rei preto(importante par verificar cheque etc.)
  rei_preto = (0, 4)
  rei_branco = (7, 4)

matriz_tabuleiro_obj = []

# transforma a matriz de inteiros em uma matriz de objetos da classe Peca
for i in range(8):
  linha = []
  for j in range(8):
    if(matriz_tabuleiro_int[i][j] != 0):
      linha.append(Peca(tipo = matriz_tabuleiro_int[i][j], pos_in_linha = i, pos_in_col = j, imagem = achar_imagem(matriz_tabuleiro_int[i][j]) , roque = 1, enpassant = 0))
    else:
      linha.append(0)
  matriz_tabuleiro_obj.append(linha)

# play screen
pygame.display.set_caption("chess")
acabou = False
tabuleiro_xadrez = pygame.display.set_mode((600, 600))

# contém a peca selecionada e a lista de mov possiveis da peça selecionada pelo jogador
peca_selecionada = None 
lista_mov_possiveis_jog = []
lista_mov_adv = []
turno = 1

while(not acabou):

  tabuleiro_xadrez.fill((255,255,255))
  offset_yt = -75

  for i in range (8):
    offset_xt = 0
    offset_yt += 75
    for j in range (8):
      if((i+j)%2 == 0):
        pygame.draw.rect(tabuleiro_xadrez, (255, 255, 255), (offset_xt, offset_yt, 75, 75))
      else:
        pygame.draw.rect(tabuleiro_xadrez, (150 , 50, 205), (offset_xt, offset_yt, 75, 75))
      offset_xt += 75

  for i in range(8):
    for j in range(8):
      if(matriz_tabuleiro_obj[i][j] != 0):
        peca = matriz_tabuleiro_obj[i][j]
        tabuleiro_xadrez.blit(peca.imagem, (peca.pos_in_col*75, -73 + 75*(peca.pos_in_linha+1)))

  if len(lista_mov_possiveis_jog) > 0 and len(peca_selecionada) > 0:

    pontos = [(peca_selecionada[1] * 75, peca_selecionada[0] * 75),  
              (peca_selecionada[1] * 75 + 75, peca_selecionada[0] * 75),  
              (peca_selecionada[1] * 75 + 75, peca_selecionada[0] * 75 + 75),  
              (peca_selecionada[1] * 75, peca_selecionada[0] * 75 + 75)]
    pygame.draw.polygon(tabuleiro_xadrez, (0 , 0, 0), pontos, 3)

    for mov in lista_mov_possiveis_jog:
      pontos = [((peca_selecionada[1]+mov[1])*75, (peca_selecionada[0]+mov[0])*75),  
                ((peca_selecionada[1]+mov[1])*75 + 75, (peca_selecionada[0]+mov[0])*75),  
                ((peca_selecionada[1]+mov[1])*75 + 75, (peca_selecionada[0]+mov[0])*75 + 75),  
                ((peca_selecionada[1]+mov[1])*75, (peca_selecionada[0]+mov[0])*75 + 75)]
      pygame.draw.polygon(tabuleiro_xadrez, (0 ,0, 0),  pontos, 3)

  if(turno == opcao_jogador):
    
    for event in pygame.event.get():
    
      if event.type == pygame.MOUSEBUTTONDOWN:

        mouse_x, mouse_y = pygame.mouse.get_pos()
        peca_movida_linha = int(mouse_y/75)
        peca_movida_coluna = int(mouse_x/75)
        peca_selecionada = [peca_movida_linha, peca_movida_coluna]

        lista_mov_possiveis_jog = []

        if(matriz_tabuleiro_obj[peca_movida_linha][peca_movida_coluna] != 0):
          if((opcao_jogador == 1) and (matriz_tabuleiro_obj[peca_movida_linha][peca_movida_coluna].tipo > 0)) or ((opcao_jogador == 0) and (matriz_tabuleiro_obj[peca_movida_linha][peca_movida_coluna].tipo < 0)):
            lista_mov_possiveis_jog = gerar_movimentos_possiveis_peca(matriz_tabuleiro_obj, matriz_tabuleiro_obj[peca_movida_linha][peca_movida_coluna], opcao_jogador, turno, 0)
            if(lista_mov_possiveis_jog is not None):
              for mov_jog in lista_mov_possiveis_jog[:]:
                if(not verif_xeque(matriz_tabuleiro_obj, matriz_tabuleiro_obj[peca_movida_linha][peca_movida_coluna], (mov_jog[0], mov_jog[1]), opcao_jogador, turno)):
                  lista_mov_possiveis_jog.remove(mov_jog)
                  print("mov removido jog:")
                  print(mov_jog)
            else:
              lista_mov_possiveis_jog = []
              peca_selecionada = []
          else:
            lista_mov_possiveis_jog = []
            peca_selecionada = []
        else:
          lista_mov_possiveis_jog = []
          peca_selecionada = []

      elif event.type == pygame.MOUSEBUTTONUP:

        print("lista de moves possiveis jog:")
        print(lista_mov_possiveis_jog)
        
        pode_movimentar = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        linha_casa = int(mouse_y/75)
        coluna_casa = int(mouse_x/75)
        movimento_ate_casa = [linha_casa-peca_movida_linha, coluna_casa-peca_movida_coluna]

        if lista_mov_possiveis_jog is not None:
          for op_mov_jog in lista_mov_possiveis_jog:
            if(op_mov_jog == movimento_ate_casa):
              pode_movimentar = 1
              break
          
        if(pode_movimentar):
            print("mov final jogador:")
            print(op_mov_jog)
            movimento_basico(matriz_tabuleiro_obj, matriz_tabuleiro_obj[peca_movida_linha][peca_movida_coluna], movimento_ate_casa, opcao_jogador)
            turno = 1 - turno

        peca_selecionada = []
        lista_mov_possiveis = []
      
      elif event.type == pygame.QUIT:
        acabou = True

  else:

    lista_mov_adv = []

    # ve quais são os valores da peça adversária e o rei adversário
    if(opcao_jogador == 0):
      menor_ini = 1
      maior_ini = 6
      rei_ini = rei_branco
      menor_jog = -6
      maior_jog = -1
      rei_jog = rei_preto
    else:
      menor_ini = -6
      maior_ini = -1
      rei_ini = rei_preto
      menor_jog = 1
      maior_jog = 6
      rei_jog = rei_branco

    # gera todos os movimentos possiveis para todas as peças da IA e seleciona um aleatoriamente
    lista_mov_adv = gerar_todos_movimentos_possiveis(matriz_tabuleiro_obj, menor_ini, maior_ini, opcao_jogador, turno)
    print("lista de moves possiveis adv(desconsiderando xeque):")
    print(lista_mov_adv)

    if(lista_mov_adv is not None):
      for mov_adv in lista_mov_adv[:]:
        if(not verif_xeque(matriz_tabuleiro_obj, matriz_tabuleiro_obj[mov_adv[0]][mov_adv[1]], (mov_adv[2], mov_adv[3]), opcao_jogador, turno)):
          lista_mov_adv.remove(mov_adv)
          print("mov adv removido:")
          print(mov_adv)
    else:
      # não tem nenhum movimento disponível(?)
      break
    
    # verifica após a remoção dos movimentos com xeque se ainda tem movimento, se não tiver o rei tomo xeque-mate ou foi afogado(empate)
    if(len(lista_mov_adv) == 0):
      if(not verif_xeque(matriz_tabuleiro_obj, matriz_tabuleiro_obj[rei_ini[0]][rei_ini[1]], (0, 0), opcao_jogador, turno)):
        print("mate no adv")
      else:
        print("afogamento")
      acabou = True
      break

    index_aleatorio = random.randint(0, len(lista_mov_adv)-1)
    op_mov_adv = lista_mov_adv[index_aleatorio]
    print("mov final adv:")
    print(op_mov_adv)
    movimento_basico(matriz_tabuleiro_obj, matriz_tabuleiro_obj[op_mov_adv[0]][op_mov_adv[1]], [op_mov_adv[2], op_mov_adv[3]], opcao_jogador)
    turno = 1 - turno

    # verificação de xeque-mate do jogador(está dentro da movimentação do inimigo para não rodar em loop)
    
    lista_mov_possiveis_jogador = gerar_todos_movimentos_possiveis(matriz_tabuleiro_obj, menor_jog, maior_jog, opcao_jogador, turno)
    print("movs possiveis jogador(proxima rodada)(considerando xeque somente no roque):")
    print(lista_mov_possiveis_jogador)

    if(lista_mov_possiveis_jogador is not None):
      for mov_jogador in lista_mov_possiveis_jogador[:]:
        if(not verif_xeque(matriz_tabuleiro_obj, matriz_tabuleiro_obj[mov_jogador[0]][mov_jogador[1]], (mov_jogador[2], mov_jogador[3]), opcao_jogador, turno)):
          lista_mov_possiveis_jogador.remove(mov_jogador)
          print("mov removido(proxima rodada):")
          print(mov_jogador)
    else:
      # não tem nenhum movimento disponivel(?)
      break

    # verifica após a remoção dos movimentos com xeque se ainda tem movimento, se não tiver o rei tomo xeque-mate ou foi afogado(empate)
    if(len(lista_mov_possiveis_jogador) == 0):
      if(not verif_xeque(matriz_tabuleiro_obj, matriz_tabuleiro_obj[rei_jog[0]][rei_jog[1]], (0, 0), opcao_jogador, turno)):
        print("mate no jog")
      else:
        print("afogamento")
      acabou = True
      break
      
  pygame.display.flip()

pygame.quit()
sys.exit()