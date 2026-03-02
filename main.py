import pygame
import sys
import random
from Config import *
from Personagem import Jogador
from Carro import Carro

# 1. INICIALIZAÇÃO
pygame.init()
pygame.mixer.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Trabalho ADS - Atravessar a Rua")
relogio = pygame.time.Clock()

fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)
fonte_texto = pygame.font.SysFont("Arial", 30)

# 2. CARREGAR ASSETS
try:
    fundo_rua = pygame.image.load("asset/rua.png").convert()
    fundo_rua = pygame.transform.scale(fundo_rua, (LARGURA, ALTURA))
    som_batida = pygame.mixer.Sound("asset/batida.mp3")
    som_vitoria = pygame.mixer.Sound("asset/vitoria.mp3")
    pygame.mixer.music.load("asset/transito.mp3")
except Exception as e:
    print(f"Erro nos assets: {e}")
    fundo_rua = None
    som_batida = som_vitoria = None

# 3. CONFIGURAÇÃO DE OBJETOS
jogador = Jogador()
grupo_jogador = pygame.sprite.GroupSingle(jogador)
grupo_carros = pygame.sprite.Group()

def criar_frota():
    grupo_carros.empty()
    inicio_asfalto = 150
    fim_asfalto = 480
    num_faixas = 6
    espaco_faixa = (fim_asfalto - inicio_asfalto) // num_faixas

    for i in range(num_faixas): # Loop das faixas
        y_atual = inicio_asfalto + (i * espaco_faixa)
        for c in range(3): # 3 carros por faixa para ser movimentado
            vel = random.randint(3, 6)
            direcao = 1 if i % 2 == 0 else -1
            novo_carro = Carro(y_atual, vel * direcao)
            grupo_carros.add(novo_carro)

estado = "MENU"

# 5. LOOP PRINCIPAL
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if estado != "JOGANDO":
                    jogador.resetar()
                    criar_frota()
                    estado = "JOGANDO"
                    if fundo_rua:
                        pygame.mixer.music.play(-1)

    # --- LÓGICA DE EXIBIÇÃO ---
    if estado == "MENU":
        tela.fill((30, 30, 30))
        txt_t = fonte_titulo.render("ATRAVESSE A RUA", True, BRANCO)
        txt_i = fonte_texto.render("SETAS: Mover | ESPAÇO: Iniciar", True, AMARELO)
        tela.blit(txt_t, (LARGURA//2 - txt_t.get_width()//2, 200))
        tela.blit(txt_i, (LARGURA//2 - txt_i.get_width()//2, 350))

    elif estado == "VITORIA":
        tela.fill((0, 0, 0))
        txt_v = fonte_titulo.render("VOCÊ GANHOU!", True, (0, 255, 0))
        txt_r = fonte_texto.render("Pressione ESPAÇO para reiniciar", True, BRANCO)
        tela.blit(txt_v, (LARGURA//2 - txt_v.get_width()//2, 200))
        tela.blit(txt_r, (LARGURA//2 - txt_r.get_width()//2, 350))

    elif estado == "JOGANDO":
        jogador.mover()
        grupo_carros.update()

        if pygame.sprite.spritecollide(jogador, grupo_carros, False):
            if som_batida: som_batida.play()
            jogador.resetar()

        # Condição de Vitória (Chegou na calçada de cima)
        if jogador.rect.top <= 120:
            if som_vitoria: som_vitoria.play()
            pygame.mixer.music.stop()
            estado = "VITORIA"

        if fundo_rua:
            tela.blit(fundo_rua, (0, 0))
        else:
            tela.fill(COR_FUNDO)

        grupo_carros.draw(tela)
        grupo_jogador.draw(tela)

    pygame.display.flip()
    relogio.tick(FPS)