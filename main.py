import pygame
from pygame.locals import *
from sys import exit
from random import randint

# iniciando a fução
pygame.init()

# configrurando tela
largaura = 800
altura = 600
tela = pygame.display.set_mode((largaura, altura))

# FPS
relogio = pygame.time.Clock()

# spawn da cobra e maca
x_cobra = largaura/2
y_cobra = altura/2
x_maca = randint(40, 760)
y_maca = randint(50, 550)
tamanho_inicial = 5

# variaveis de controle
velocidade = 10
x_controle = velocidade
y_controle = 0

# confugruração inicial do contador de pontos
pontos = 0
fonte = pygame.font.SysFont('play', 40, False, False)
pygame.display.set_caption('Jogo da cobrinha')


# função que desenha a cobra na tela 
lista_cobra = []
def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        pygame.draw.rect(tela, (0,255,0), (XeY[0], XeY[1], 40, 40))

# loop principal
while True:

    # fps 2
    relogio.tick(60)

    # deixar a tela branca
    tela.fill((255, 255, 255))

    # texto do placar de pontos
    texto = fonte.render(f'Pontos: {pontos}', True, (0, 0, 0))
    
    # verifica os eventos que ocorreram durante a iteração
    for event in pygame.event.get():
        
        # verifica se o jogo foi fechado
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # controla a cobra
        # é feito dessa maneira para que a cobra ande somente de forma reta 
        if event.type == KEYDOWN:
            
            # se a tecla apertada for 'a' e a cobra estiver indo pra direita o comando não poderá ser executado
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = -velocidade
            if event.key == K_s:
                if y_controle == -velocidade:
                    pass
                else:
                    x_controle = 0
                    y_controle = velocidade
    
    # faz com a cobra ande continuamente
    x_cobra += x_controle
    y_cobra += y_controle

    # desenha a cabeça da cobra e a maçã
    ret_cobra = pygame.draw.rect(tela, (0, 255, 0), (x_cobra, y_cobra, 40, 40))
    ret_maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 40, 40))

    # lista da cabeça da cobra
    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)

    # copia a cabeca da cobra para formar o corpo
    lista_cobra.append(lista_cabeca)
    if len(lista_cobra) > tamanho_inicial:
        del lista_cobra[0]

    #chamando a função que vai desenharo o corpo da cobra
    aumenta_cobra(lista_cobra)

    # colisão
    ## maçã recebe um novo spawn, contador de pontos é atualizado, cobra aumenta de tamanho (lá eler)
    if ret_cobra.colliderect(ret_maca):
        x_maca = randint(40, 760)
        y_maca = randint(50, 550)
        pontos += 1
        tamanho_inicial += 1

    # exibi o contador de pontos
    tela.blit(texto, (450,40))

    # atualiza a informações na tela
    pygame.display.flip()
