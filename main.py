import pygame
import sys
import random
from Config import *
from Personagem import Jogador
from Carro import Carro

from Config import COR_FUNDO, FPS, LARGURA, ALTURA

# 1. INICIALIZAÇÃO
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Trabalho ADS - Atravessar a Rua")
relogio = pygame.time.Clock()
fonte_grande = pygame.font.SysFont("Arial", 60, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 25)

# 2. CARREGAR ASSETS (Imagens)
try:
    # O .convert() ajuda o jogo a rodar mais rápido
    fundo_rua = pygame.image.load("asset/rua.png").convert()
    fundo_rua = pygame.transform.scale(fundo_rua, (LARGURA, ALTURA))
except:
    fundo_rua = None  # Plano B caso a imagem não exista

# 3. CRIAÇÃO DOS GRUPOS DE SPRITES
# GroupSingle é usado para o jogador (só existe um)
grupo_jogador = pygame.sprite.GroupSingle()
jogador = Jogador()
grupo_jogador.add(jogador)

# Group guarda todos os carros
grupo_carros = pygame.sprite.Group()



def criar_carros():
    grupo_carros.empty()

    # 1. Definimos onde o asfalto começa e termina (em pixels)
    inicio_asfalto = 160
    fim_asfalto = 480

    # 2. Calculamos o espaço entre cada uma das 6 faixas
    espaco_entre_faixas = (fim_asfalto - inicio_asfalto) // 6

    for i in range(6):
        # O 'y' agora é calculado apenas dentro da zona de asfalto
        pos_y = inicio_asfalto + (i * espaco_entre_faixas)

        # Sorteia uma velocidade para cada carro
        vel = random.randint(3, 8)

        # Adiciona o carro na faixa correta
        novo_carro = Carro(pos_y, vel)
        grupo_carros.add(novo_carro)


# 4. ESTADOS DO JOGO
# Usamos strings para controlar em qual tela o jogador está
estado_jogo = "MENU"

# 5. LOOP PRINCIPAL
while True:
    # --- TRATAMENTO DE EVENTOS (Teclado e Mouse) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if estado_jogo == "MENU" or estado_jogo == "VITORIA":
                    # Reinicia o jogo
                    jogador.resetar()
                    criar_carros()
                    estado_jogo = "JOGANDO"

    # --- LÓGICA DAS TELAS ---
    if estado_jogo == "MENU":
        tela.fill((0, 0, 0))  # Fundo preto
        texto_titulo = fonte_grande.render("CROSS THE STREET", True, (255, 255, 255))
        texto_instr = fonte_pequena.render("COMANDOS: Use as SETAS para mover", True, (255, 255, 0))
        texto_start = fonte_pequena.render("Pressione ESPAÇO para Iniciar", True, (0, 255, 0))

        tela.blit(texto_titulo, (LARGURA // 2 - 250, 150))
        tela.blit(texto_instr, (LARGURA // 2 - 200, 300))
        tela.blit(texto_start, (LARGURA // 2 - 150, 400))

    elif estado_jogo == "VITORIA":
        tela.fill((20, 20, 20))
        texto_win = fonte_grande.render("VOCÊ GANHOU!", True, (0, 255, 0))
        texto_retry = fonte_pequena.render("Pressione ESPAÇO para jogar novamente", True, (255, 255, 255))

        tela.blit(texto_win, (LARGURA // 2 - 200, 200))
        tela.blit(texto_retry, (LARGURA // 2 - 200, 350))

    elif estado_jogo == "JOGANDO":
        # --- ATUALIZAÇÃO ---
        jogador.mover()  # Move o boneco
        grupo_carros.update()  # Move os carros

        # Verificação de Colisão (Bateu no carro?)
        if pygame.sprite.spritecollide(jogador, grupo_carros, False):
            jogador.resetar()  # Se bater, volta ao início (não perde o jogo)

        # Verificação de Vitória (Chegou no topo?)
        if jogador.rect.top <= 0:
            estado_jogo = "VITORIA"

        # --- DESENHO ---
        if fundo_rua:
            tela.blit(fundo_rua, (0, 0))
        else:
            tela.fill(COR_FUNDO)

        grupo_carros.draw(tela)  # Desenha carros
        grupo_jogador.draw(tela)  # Desenha o jogador por cima

    # Atualiza o ecrã e controla o FPS
    pygame.display.flip()
    relogio.tick(FPS)