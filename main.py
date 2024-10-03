
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

3)roque e en passant: atributos para ajudar na programação dessas 2 regras
->se a torre e o rei ainda não tiverem se mexido, o valor de roque deles é igual a 1, ou seja, eles podem rocar, caso o contrário é igual a 0
->se o peão mover 2 casas para frente, naquele momento o seu valor de en passant passa a valer 1 e , se tiver um peão inimigo ao seu lado, ele pode comer e após o movimento do adversário, o valor de en passant volta a ser 0 para tal peão

4)promoção: se um peão chegar na última fileira, seu valor de promoção vale 1 e o programa fornece uma escolha de peça para promover

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

# definição da classe peça
class Peca:
    def __init__(self, tipo, pos_in_linha, pos_in_col, roque, enpassant):
      self.tipo = tipo
      self.pos_in_linha = pos_in_linha
      self.pos_in_col = pos_in_col
      self.roque = roque
      self.enpassant = enpassant  
    def __int__(self):
      return self.tipo
    
# macro para limpar tela  
def limpar_tela():
  os.system('cls' if os.name == 'nt' else 'clear')
    
# função para retornar cor da peça(1 branco 0 preto)
def cor_peca(peca):
  if(peca.tipo > 0):
    return 1
  else:
    return 0

# função para veririficar se o movimento cogitado está nos limites da matriz(0 a 7) 
def verif_mov(linha_peca, coluna_peca, mov):
  return 0 <= linha_peca + mov[0] <= 7 and 0 <= coluna_peca + mov[1] <= 7

# movimento básico de substituição entre 2 posições
def movimento_basico(matriz, peca_movida, lista_mov):
    
  # ve a linha/coluna da peça
  linha_peca = peca_movida.pos_in_linha
  coluna_peca = peca_movida.pos_in_col

  # atualiza a nova linha/coluna da peça
  peca_movida.pos_in_linha = linha_peca+lista_mov[0]
  peca_movida.pos_in_col = coluna_peca+lista_mov[1]

  # troca a peça de lugar na matriz, deixando o espaço onde ela estava como 0(sem peça na casa)
  matriz[linha_peca][coluna_peca] = 0
  matriz[linha_peca+lista_mov[0]][coluna_peca+lista_mov[1]] = peca_movida

# gera todos os movimentos possíveis para a peça em questão
# por enquanto trata-se dos movimentos desconsiderando o xeque, o mate e as regras adicionais de movimento
def gerar_movimentos_possiveis(matriz, peca_movida):
    
  # ve a linha/coluna da peça
  linha_peca = peca_movida.pos_in_linha
  coluna_peca = peca_movida.pos_in_col 
  peca_movida = matriz[linha_peca][coluna_peca]

  # inicializa a lista de movimentos possiveis
  lista_mov_possiveis = []

  cor = cor_peca(peca_movida)

  if abs(peca_movida.tipo) == 1:      # peão

    # movimentos iniciais possiveis para um peão(pra frente e pra diagonal)   
    mov_possiveis_iniciais_preto = [[1,0],[1,1],[1,-1]]
    mov_possiveis_iniciais_branco =  [[-1,0],[-1,1],[-1,-1]]

    if(cor == 1):                     # peão branco

      # se estiver na linha inicial, pode pular 2 casas
      if(linha_peca == 6):
        mov_possiveis_iniciais_branco.append([-2,0])
      
      for mov in mov_possiveis_iniciais_branco:
        
        if(verif_mov(linha_peca, coluna_peca, mov)):
          
          # se ele não move na coluna, então ele está indo para frente e verificamos se o espaço está vazio para passar
          if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] == 0 and mov[1] == 0):
            lista_mov_possiveis.append(mov)
          # se ele move, então é um movimento de captura e verificamos se o espaço está ocupado por uma peça inimiga
          elif(mov[1] != 0):
            if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] != 0):
              peca_diagonal = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
              cor_peca_diagonal = cor_peca(peca_diagonal)
              if(cor_peca_diagonal != cor):
                lista_mov_possiveis.append(mov)   

    else:                               # peão preto
      
      # se estiver na linha inicial, pode pular 2 casas
      if(linha_peca == 1):
          mov_possiveis_iniciais_preto.append([2,0])

      for mov in mov_possiveis_iniciais_preto:
          
        if(verif_mov(linha_peca, coluna_peca, mov)):

          # se ele não move na coluna, então ele está indo para frente e verificamos se o espaço está vazio para passar
          if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] == 0 and mov[1] == 0):
            lista_mov_possiveis.append(mov)
          # se ele move, então é um movimento de captura e verificamos se o espaço está ocupado por uma peça inimiga
          elif(mov[1] != 0):
            if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] != 0):
              peca_diagonal = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
              cor_peca_diagonal = cor_peca(peca_diagonal)
              if(cor_peca_diagonal != cor):
                lista_mov_possiveis.append(mov)   

  

  
  elif abs(peca_movida.tipo) == 2:       # rei

    # movimentos iniciais possiveis para um rei(1 casa em qualquer direção, ataca nessas casas também)
    movimentos_iniciais_rei = [[0,1], [0,-1], [1,0], [-1,0], [1,1], [1,-1], [-1,1], [-1,-1]]

    for mov in movimentos_iniciais_rei:

      if(verif_mov(linha_peca, coluna_peca, mov)):

        if(matriz[linha_peca+mov[0]][coluna_peca+mov[1]] == 0):
          lista_mov_possiveis.append(mov)

        else:
          peca_alvo = matriz[linha_peca+mov[0]][coluna_peca+mov[1]]
          cor_peca_alvo = cor_peca(peca_alvo)
          if(cor_peca_alvo != cor):
              lista_mov_possiveis.append(mov)
  
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
        if(verif_mov(linha_peca, coluna_peca, mov)):

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
        if(verif_mov(linha_peca, coluna_peca, mov)):

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
      if(verif_mov(linha_peca, coluna_peca, mov)):
        
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
        if(verif_mov(linha_peca, coluna_peca, mov)):

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

# incializa a matriz_tabuleiro fora do loop do jogo e dos objetos

matriz_tabuleiro_int =  [[-6, -5, -4, -3, -2, -4, -5, -6],                               
                        [-1, -1, -1, -1, -1, -1, -1, -1],  
                        [0, 0, 0, 0, 0, 0, 0, 0],  
                        [0, 0, 0, 0, 0, 0, 0, 0],  
                        [0, 0, 0, 0, 0, 0, 0, 0],  
                        [0, 0, 0, 0, 0, 0, 0, 0],  
                        [1, 1, 1, 1, 1, 1, 1, 1],  
                        [6, 5, 4, 3, 2, 4, 5, 6]] 

matriz_tabuleiro_obj = []

# transforma a matriz de inteiros em uma matriz de objetos da classe Peca
for i in range(8):
  linha = []
  for j in range(8):
    if(matriz_tabuleiro_int[i][j] != 0):
      linha.append(Peca(tipo = matriz_tabuleiro_int[i][j], pos_in_linha = i, pos_in_col = j, roque = 1, enpassant = 0))
    else:
      linha.append(0)
  matriz_tabuleiro_obj.append(linha)

acabou = 0

while(not acabou):

  for linha in matriz_tabuleiro_obj:
    print(", ".join(f"{int(peca):2}" if isinstance(peca, Peca) else f"{peca:2}" for peca in linha))

  peca_movida_linha = int(input("Digite a linha da peça que deseja mover(começando do 0): "))
  peca_movida_coluna = int(input("Digite a coluna da peça que deseja mover(começando do 0): "))

  lista_mov = gerar_movimentos_possiveis(matriz_tabuleiro_obj, matriz_tabuleiro_obj[peca_movida_linha][peca_movida_coluna])

  if lista_mov != None:

    print("Lista de movimentos possiveis: ")

    for mov in lista_mov:
      print(mov)

    print("Digite o movimento desejado da lista(começando do 0): ")
    indice_mov = int(input())

    # terá uma função aqui para verificar se houve um movimento que muda a dinâmica do tabuleiro(promoção, xeque, xeque_mate), nesse caso o movimento básico não servirá
    
    movimento_basico(matriz_tabuleiro_obj, matriz_tabuleiro_obj[peca_movida_linha][peca_movida_coluna], lista_mov[indice_mov])

    print("\nTabuleiro após movimento:\n")

    for linha in matriz_tabuleiro_obj:
      print(", ".join(f"{int(peca):2}" if isinstance(peca, Peca) else f"{peca:2}" for peca in linha))

    input("\npressione enter para continuar:")
    limpar_tela()

  else:
    print("\nNão há movimento válido para esta peça")
    input("\npressione enter para continuar:")
    limpar_tela()
