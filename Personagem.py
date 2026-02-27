import pygame
from Config import *

from Config import ALTURA, LARGURA


class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            # Tenta carregar a imagem. Se não existir, cria um quadrado
            self.image = pygame.image.load("asset/personagem.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 40))
        except:
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 255, 0))  # Verde

        self.rect = self.image.get_rect()
        self.resetar()
        self.velocidade = 5

    def mover(self):
        # Captura as teclas pressionadas
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
        # Coloca o jogador na posição inicial (meio da base)
        self.rect.centerx = LARGURA // 2
        self.rect.bottom = ALTURA - 10