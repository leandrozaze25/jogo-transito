import pygame
import random
from Config import *

from Config import LARGURA


class Carro(pygame.sprite.Sprite):
    def __init__(self, y_pos, velocidade):
        super().__init__()
        # Sorteia uma cor de carro
        cor = random.choice(["azul", "amarelo"])
        try:
            self.image = pygame.image.load(f"asset/carro_{cor}.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (70, 35))
        except:
            self.image = pygame.Surface((70, 35))
            self.image.fill((255, 0, 0)) # Vermelho se falhar imagem

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-200, -50) # Começa fora do ecrã
        self.rect.y = y_pos
        self.velocidade = velocidade

    def update(self):
        self.rect.x += self.velocidade
        # Se sair pelo lado direito, volta para a esquerda
        if self.rect.left > LARGURA:
            self.rect.right = 0