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

# musicas
## musica de fundo
musica_fundo = pygame.mixer.music.load('BoxCat Games - Inspiration.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.15)

## barulho de colisão
barulho_de_colisao = pygame.mixer.Sound('smw_1-up.wav') 
barulho_de_colisao.set_volume(0.05)

## game over som
fim_de_jogo = pygame.mixer.Sound('smw_game_over.wav') 
fim_de_jogo.set_volume(0.15)

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

# varivel de morte
morreu = False

# lista que pega cada posição em que a cabeça da cobra já esteve
lista_cobra = []

# função que desenha a cobra na tela
def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 40, 40))

# funçao que quando chamada reinicia o jogo
def reinicia_jogo():
    global x_cobra, y_cobra, x_maca, y_maca, tamanho_inicial, velocidade, x_controle, y_controle, pontos, morreu, lista_cabeca, lista_cobra
    x_cobra = largaura/2
    y_cobra = altura/2
    x_maca = randint(40, 760)
    y_maca = randint(50, 550)
    tamanho_inicial = 5
    velocidade = 10
    x_controle = velocidade
    y_controle = 0
    pontos = 0
    lista_cobra = []
    lista_cabeca = []
    morreu = False
    pygame.mixer.music.play(-1)


# loop principal
while True:

    # fps 2
    relogio.tick(75)

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

    # faz com que a cobra reapareça ao sumir da tela
    if x_cobra > largaura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largaura
    if y_cobra > altura:
        y_cobra = 0
    if y_cobra < 0:
        y_cobra = altura

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

    # verificar se a cobra encostou no corpo
        if lista_cobra.count(lista_cabeca) > 1:
            pygame.mixer.music.stop()
            morreu = True
            texto2 = fonte.render('Game Over! Pressione a tecla R para jogar novamente', True, (0, 0, 0))
            fim_de_jogo.play()
            while morreu:
                tela.fill((255, 255, 255))
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN:
                        if event.key == K_r:
                            reinicia_jogo()
                tela.blit(texto2, (32, 290))
                pygame.display.flip()

    # chamando a função que vai desenhar o corpo da cobra
    aumenta_cobra(lista_cobra)

    # colisão
    # maçã recebe um novo spawn, contador de pontos é atualizado, cobra aumenta de tamanho (lá eler)
    if ret_cobra.colliderect(ret_maca):
        x_maca = randint(40, 760)
        y_maca = randint(50, 550)
        pontos += 1
        tamanho_inicial += 1
        barulho_de_colisao.play()

    # exibi o contador de pontos
    tela.blit(texto, (630, 40))

    # atualiza a informações na tela
    pygame.display.flip()
