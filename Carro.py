import pygame
import random
from Config import LARGURA

class Carro(pygame.sprite.Sprite):
    def __init__(self, y_pos, velocidade):
        super().__init__()
        # Escolhe uma cor aleatória para o carro
        cor = random.choice(["azul", "amarelo"])
        try:
            self.image = pygame.image.load(f"asset/carro_{cor}.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (70, 35))
            # Se a velocidade for negativa, vira a imagem para a esquerda
            if velocidade < 0:
                self.image = pygame.transform.flip(self.image, True, False)
        except:
            self.image = pygame.Surface((70, 35))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.y = y_pos
        self.velocidade = velocidade
        # Define uma posição X inicial aleatória para não começarem todos juntos
        self.rect.x = random.randint(0, LARGURA)

    def update(self):
        self.rect.x += self.velocidade

        # Retorna para o início ao sair da tela mantendo o fluxo
        if self.velocidade > 0 and self.rect.left > LARGURA:
            self.rect.right = 0
        elif self.velocidade < 0 and self.rect.right < 0:
            self.rect.left = LARGURA