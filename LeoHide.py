import pygame
import sys
from tkinter import Tk, messagebox, simpledialog

# Função para sair do jogo
def sair_jogo():
    pygame.quit()
    sys.exit()

# Função para criar botões
def criar_botao(x, y, largura, altura, texto="", acao=None, cor_botao=(128, 128, 128), cor_texto=(255, 255, 255), ordem=0):
    mouse_pos = pygame.mouse.get_pos()
    click_mouse = pygame.mouse.get_pressed()

    botao = pygame.Rect(x, y, largura, altura)

    if botao.collidepoint(mouse_pos) and ordem == 0:
        cor_botao = (0, 128, 0)  # Verde sem transparência para o estado hover
        if click_mouse[0] == 1 and acao is not None:
            acao()

    superficie_botao = pygame.Surface((largura, altura), pygame.SRCALPHA)  # Superfície com canal alfa para transparência
    superficie_botao.fill((0, 0, 0, 0))  # Preenchimento transparente
    pygame.draw.rect(superficie_botao, cor_botao, superficie_botao.get_rect(), border_radius=5)

    if texto != "":
        fonte = pygame.font.Font(None, 36)
        texto_surface = fonte.render(texto, True, cor_texto)
        texto_rect = texto_surface.get_rect(center=(largura / 2, altura / 2))
        superficie_botao.blit(texto_surface, texto_rect)

    if ordem == 0:
        tela.blit(superficie_botao, (x, y))
    else:
        tela.blit(superficie_botao, (x, y))

# Função para a tela principal
def tela_principal():
    tela.blit(imagem_carregamento, (0, 0))
    criar_botao(275, 300, 250, 45, "Iniciar Jogo", mudar_para_tela_terciaria)
    pygame.display.flip()


# Função para a tela sextenária
def tela_sextenaria():
    tela_personalizada = pygame.image.load("ranking.jpg")
    tela_personalizada = pygame.transform.scale(tela_personalizada, (largura, altura))
    tela.blit(tela_personalizada, (0, 0))

    def perguntar_usuario():
        # Inicializa o Tkinter para usar a janela de diálogo
        root = Tk()
        root.withdraw()  # Oculta a janela principal do Tkinter

        # Pergunta o email do usuário
        email = simpledialog.askstring("Pergunta", "Por favor, insira seu email:")

        # Fecha a janela do Tkinter
        root.destroy()

        if email:
            print(f"Email inserido: {email}")
        else:
            messagebox.showinfo(" ", "Você não inseriu email")

    criar_botao(250, 450, 300, 50, "Inserir Email", perguntar_usuario)

    pygame.display.flip()

# Função para mudar para a tela principal
def mudar_para_tela_principal():
    global tela_atual
    tela_atual = "principal"

# Função para mudar para a tela terciária
def mudar_para_tela_terciaria():
    global tela_atual
    tela_atual = "terciaria"

# Função para mudar para a tela sextenaria
def mudar_para_tela_sextenaria():
    global tela_atual
    tela_atual = "sextenaria"

# Inicialização do pygame
pygame.init()

largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jardim De Darwin")

imagem_carregamento = pygame.image.load("Imagem_de_carregamento.jpg")
imagem_carregamento = pygame.transform.scale(imagem_carregamento, (largura, altura))


tela_atual = "principal"

# Loop principal do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sair_jogo()

    if tela_atual == "principal":
        tela_principal()
    elif tela_atual == "sextenaria":
        tela_sextenaria()
