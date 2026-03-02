import pygame
from Config import LARGURA, ALTURA

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("asset/personagem.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
        except:
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 255, 0))  # Verde caso a imagem falte

        self.rect = self.image.get_rect()
        self.resetar()
        self.velocidade = 5

    def mover(self):
        # Verifica quais teclas estão a ser pressionadas para mover o boneco
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTURA:
            self.rect.y += self.velocidade
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < LARGURA:
            self.rect.x += self.velocidade

    def resetar(self):
        # Reposiciona o jogador na calçada inferior (início)
        self.rect.centerx = LARGURA // 2
        self.rect.bottom = ALTURA - 20 # Ajustado para não começar em cima da calçada