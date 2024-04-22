# Primeiro-Repository

import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
FPS = 60

# Inicialização da janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Seleção Natural")

# Inicialização do relógio
clock = pygame.time.Clock()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += 5

class Insect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.color = random.choice([WHITE, GREEN])  # Insetos podem ser brancos ou verdes
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH)
        self.rect.y = random.randrange(HEIGHT)

    def update(self):
        pass

# Grupos de sprites
all_sprites = pygame.sprite.Group()
insects_group = pygame.sprite.Group()

# Adiciona a ave ao grupo de sprites
bird = Bird()
all_sprites.add(bird)

# Adiciona insetos ao grupo de insetos
for _ in range(20):
    insect = Insect()
    all_sprites.add(insect)
    insects_group.add(insect)

# Loop principal do jogo
running = True
while running:
    # Processa eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza lógica do jogo
    all_sprites.update()

    # Verifica colisões (se a ave "bica" um inseto)
    hits = pygame.sprite.spritecollide(bird, insects_group, True)

    # Verifica se todos os insetos têm a mesma cor
    if all(insect.color == GREEN for insect in insects_group):
        running = False  # Todos os insetos são verdes, jogador venceu

    # Preenche a tela
    screen.fill(WHITE)

    # Desenha todos os sprites na tela
    all_sprites.draw(screen)

    # Atualiza a tela
    pygame.display.flip()

    # Define a taxa de frames por segundo
    clock.tick(FPS)

# Exibição de mensagem ao final do jogo
font = pygame.font.Font(None, 36)
if all(insect.color == GREEN for insect in insects_group):
    text = font.render("Você venceu! Todos os insetos são verdes.", True, (0, 0, 0))
else:
    text = font.render("Fim de jogo. Alguns insetos ainda estão presentes.", True, (0, 0, 0))

screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
pygame.display.flip()

# Aguarda um tempo antes de encerrar
pygame.time.wait(3000)

# Finaliza o Pygame
pygame.quit()
sys.exit()
