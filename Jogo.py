import tkinter as tk
from PIL import Image, ImageTk
import random

# Função para mover o pássaro para cima
def mover_cima(event):
    canvas.move(passaro_id, 0, -10)  # Mover o pássaro para cima

# Função para mover o pássaro para baixo
def mover_baixo(event):
    canvas.move(passaro_id, 0, 10)   # Mover o pássaro para baixo

# Função para mover o pássaro para esquerda
def mover_esquerda(event):
    canvas.move(passaro_id, -10, 0)  # Mover o pássaro para esquerda

# Função para mover o pássaro para direita
def mover_direita(event):
    canvas.move(passaro_id, 10, 0)   # Mover o pássaro para direita

# Função para encerrar o jogo
def encerrar_jogo():
    janela.destroy()

# Função principal
def jogo():
    global canvas, passaro_id, pontuacao_label, pontuacao, insetos, besouros, janela
    
    # Inicializar a janela
    janela = tk.Tk()
    janela.title("Jogo do Pássaro")

    # Criar o canvas
    canvas = tk.Canvas(janela, width=800, height=600, bg="green")
    canvas.pack()
    
    # Carregar imagem do pássaro
    imagem_passaro = Image.open(r"D:\Downloads\Tentilhao.png")

    # Substitua "passaro.png" pelo caminho da sua imagem de pássaro
    imagem_passaro = imagem_passaro.resize((100, 100))  # Redimensionar a imagem conforme necessário
    passaro_img = ImageTk.PhotoImage(imagem_passaro)

    # Carregar imagem dos insetos
    imagem_inseto = Image.open(r"D:\Downloads\insetos.png")

    # Substitua "inseto.png" pelo caminho da sua imagem de inseto
    tamanho_inseto = 80
    imagem_inseto = imagem_inseto.resize((tamanho_inseto, tamanho_inseto))  # Redimensionar a imagem conforme necessário
    inseto_img = ImageTk.PhotoImage(imagem_inseto)
    
    # Carregar imagem dos besouros
    imagem_besouro = Image.open(r"D:\Downloads\besouro.png")

    # Substitua "besouro.png" pelo caminho da sua imagem de besouro
    tamanho_besouro = 80
    imagem_besouro = imagem_besouro.resize((tamanho_besouro, tamanho_besouro))  # Redimensionar a imagem conforme necessário
    besouro_img = ImageTk.PhotoImage(imagem_besouro)

    # Criar insetos e besouros
    insetos = []
    besouros = []

    for _ in range(4):
        # Gerar novas coordenadas para insetos
        x, y = random.randint(100, 700), random.randint(0, 550)

        # Verificar a distância dos insetos existentes
        while any(abs(x - canvas.coords(inseto_id)[0]) < 100 and abs(y - canvas.coords(inseto_id)[1]) < 100 for inseto_id in insetos):
            x, y = random.randint(100, 700), random.randint(0, 550)

        inseto_id = canvas.create_image(x, y, anchor=tk.NW, image=inseto_img)
        insetos.append(inseto_id)

        # Gerar novas coordenadas para besouros
        x, y = random.randint(100, 700), random.randint(0, 550)

        # Verificar a distância dos besouros existentes e dos insetos
        while any(abs(x - canvas.coords(besouro_id)[0]) < 100 and abs(y - canvas.coords(besouro_id)[1]) < 100 for besouro_id in besouros) \
                or any(abs(x - canvas.coords(inseto_id)[0]) < 100 and abs(y - canvas.coords(inseto_id)[1]) < 100 for inseto_id in insetos):
            x, y = random.randint(100, 700), random.randint(0, 550)

        besouro_id = canvas.create_image(x, y, anchor=tk.NW, image=besouro_img)
        besouros.append(besouro_id)

    # Exibir o pássaro no canvas e armazenar o identificador do objeto do pássaro
    passaro_id = canvas.create_image(50, 300, anchor=tk.NW, image=passaro_img)

    # Pontuação
    pontuacao = 0
    pontuacao_label = canvas.create_text(50, 50, anchor=tk.NW, text="Pontuação: {}".format(pontuacao), fill="white", font=("Arial", 15))

    # Configurar eventos de teclado
    janela.bind("<Up>", mover_cima)
    janela.bind("<Down>", mover_baixo)
    janela.bind("<Left>", mover_esquerda)
    janela.bind("<Right>", mover_direita)

    # Definir o temporizador para encerrar o jogo após 30 segundos (30000 milissegundos)
    janela.after(10000, encerrar_jogo)

    # Loop principal do jogo
    flag = True 

    while flag:
        passaro_bbox = canvas.bbox(passaro_id)  # Obtém as coordenadas do retângulo delimitador do pássaro
        for inseto_id in insetos:
            inseto_bbox = canvas.bbox(inseto_id)  # Obtém as coordenadas do retângulo delimitador do inseto
            if passaro_bbox and inseto_bbox:
                passaro_x1, passaro_y1, passaro_x2, passaro_y2 = passaro_bbox
                inseto_x1, inseto_y1, inseto_x2, inseto_y2 = inseto_bbox
                if passaro_x2 > inseto_x1 and passaro_x1 < inseto_x2 and passaro_y2 > inseto_y1 and passaro_y1 < inseto_y2:
                    canvas.delete(inseto_id)
                    pontuacao += 1
                    canvas.itemconfig(pontuacao_label, text="Pontuação: {}".format(pontuacao))
                    x = random.randint(100, 700)
                    y = random.randint(0, 550)
                    inseto_id = canvas.create_image(x, y, anchor=tk.NW, image=inseto_img)
                    insetos.append(inseto_id)
        janela.update_idletasks()
        janela.update()
    flag = False

# Iniciar o jogo
if __name__ == "__main__":
    jogo()
    
    