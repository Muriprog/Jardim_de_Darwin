import tkinter as tk
from PIL import Image, ImageTk
import random
from tkinter import messagebox

class JogoPerguntas:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Jogo do Pássaro e Perguntas")
        
        # Criar o canvas
        self.canvas = tk.Canvas(janela, width=800, height=600, bg="green")
        self.canvas.pack()
        
        # Iniciar o jogo do pássaro
        self.iniciar_jogo_passaro()
        
    def iniciar_jogo_passaro(self):
        # Carregar imagem do pássaro
        imagem_passaro = Image.open(r"C:\Users\24.00721-8\Downloads\passaro.png")
        imagem_passaro = imagem_passaro.resize((50, 50))
        self.passaro_img = ImageTk.PhotoImage(imagem_passaro)
        # Exibir o pássaro no canvas
        self.passaro_id = self.canvas.create_image(50, 300, anchor=tk.NW, image=self.passaro_img)
        
        # Carregar imagem dos insetos
        imagem_inseto = Image.open(r"C:\Users\24.00721-8\Downloads\insetos.png")
        tamanho_inseto = 60
        imagem_inseto = imagem_inseto.resize((tamanho_inseto, tamanho_inseto))
        self.inseto_img = ImageTk.PhotoImage(imagem_inseto)
        
        # Criar insetos
        self.insetos = []
        for _ in range(5):
            x, y = random.randint(100, 700), random.randint(0, 550)
            inseto_id = self.canvas.create_image(x, y, anchor=tk.NW, image=self.inseto_img)
            self.insetos.append(inseto_id)
        
        # Pontuação
        self.pontuacao = 0
        self.pontuacao_label = self.canvas.create_text(50, 50, anchor=tk.NW, text="Pontuação: {}".format(self.pontuacao), fill="white", font=("Arial", 15))
        
        # Configurar eventos de teclado
        self.janela.bind("<Up>", self.mover_cima)
        self.janela.bind("<Down>", self.mover_baixo)
        self.janela.bind("<Left>", self.mover_esquerda)
        self.janela.bind("<Right>", self.mover_direita)
        
        # Definir o temporizador para encerrar o jogo após 30 segundos
        self.janela.after(2000, self.mostrar_perguntas)
    
    def mostrar_perguntas(self):
        # Remover eventos de teclado do jogo do pássaro
        self.janela.unbind("<Up>")
        self.janela.unbind("<Down>")
        self.janela.unbind("<Left>")
        self.janela.unbind("<Right>")
        
        # Remover insetos do canvas
        for inseto_id in self.insetos:
            self.canvas.delete(inseto_id)
        
        # Criar o jogo de perguntas
        self.label_pergunta = tk.Label(self.canvas, text="Pergunta:\n", bg="white", font=("Arial", 12))
        self.label_pergunta.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.perguntas = [
            {
                "pergunta": "(UFMG) Desenvolvida, há 150 anos, por Charles Darwin e Alfred Wallace, a ideia da seleção natural \n"
                            "pode ser sustentada por observações científicas atuais. \n"
                            "Assinale a alternativa que contém uma informação que NÃO é sustentada pela Teoria Evolutiva por Seleção Natural.",
                "alternativas": [
                    "a) A reposição do fator de coagulação mediante transfusão de sangue \n "
                    "aumenta a adaptabilidade dos hemofílicos.", 
                    "b) Certas bactérias, em face de mudanças no ambiente, adquirem a capacidade de produzir novas substâncias.", 
                    "c) O vírus HIV pode sofrer mutações, o que dificulta o tratamento de indivíduos soropositivos.", 
                    "d) Os peixes cegos apresentam menor chance de sobrevivência em ambientes iluminados."
                ],
                "resposta": "b) Certas bactérias, em face de mudanças no ambiente, adquirem a capacidade de produzir novas substâncias."
            },
            {
                "pergunta": "(UFRS) Embriões de vertebrados tendem a ser mais similares entre si do que os adultos correspondentes. \n"
                            "Sobre esse fato, são feitas as seguintes afirmações. \n"
                            "I - As analogias observadas indicam uma origem comum. \n"
                            "II - O estudo da embriologia comparada contribui para a compreensão da evolução biológica. \n"
                            "III - Durante o desenvolvimento embrionário, os organismos passam por fases que repetem \n"
                            "estágios adultos de seus ancestrais. \n"
                            "Assinale a alternativa correta",
                "alternativas": [
                    "a) Apenas I.", 
                    "b) Apenas II.", 
                    "c) Apenas III.", 
                    "d) Apenas I e III.",
                    "e) I, II e III."
                ],
                "resposta": "b) Apenas II."
            },
            {
                "pergunta": "(UNB) - Alterada. Nos últimos anos, os Bálcãs têm sido agitados por uma série de conflitos étnicos, dos \n"
                            "quais o mais recente foi a guerra no Kosovo. Os conflitos chamam a atenção, entre tantos outros aspectos, \n" 
                            "para a questão das etnias humanas, com base nas afirmações relacionadas a conceitos de evolução e  \n"
                            "genética de populações abaixo, assinale a alternativa correta. \n"
                            "(1) Antes dos atuais conflitos, na década de 80, a distribuição de genes na população da Iugoslávia seguia \n"
                            "o equilíbrio de Hardy-Weinberg. \n"
                            "(2) Além do isolamento geográfico, aspectos culturais como os costumes e a religião influem na evolução das \n" 
                            "etnias humanas."
                            "(3) Os Bálcãs exemplificam bem que a migração aumenta a variabilidade genética."
                            "(4) É provável que a frequência de heterozigose seja semelhante na população brasileira e na população sérvia.",
                "alternativas": ["F-V-F-F",
                                "V-V-V-V", 
                                "V-V-F-V", 
                                "F-V-V-F"],
                "resposta": "F-V-F-F"
            }
        ]
        
        self.pergunta_atual = 0
        
        self.label_pergunta = tk.Label(self.canvas, text=self.perguntas[self.pergunta_atual]["pergunta"], wraplength=600)
        self.label_pergunta.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        self.resposta_selecionada = tk.StringVar()
        for alternativa in self.perguntas[self.pergunta_atual]["alternativas"]:
            tk.Radiobutton(self.canvas, text=alternativa, variable=self.resposta_selecionada, value=alternativa).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.botao_proxima = tk.Button(self.canvas, text="Próxima Pergunta", command=self.mostrar_proxima_pergunta)
        self.botao_proxima.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    
    def mostrar_proxima_pergunta(self):
        resposta_usuario = self.resposta_selecionada.get()
        resposta_correta = self.perguntas[self.pergunta_atual]["resposta"]
        
        if resposta_usuario == resposta_correta:
            messagebox.showinfo("Resposta", "Resposta correta!")
        else:
            messagebox.showinfo("Resposta", "Resposta incorreta!")
        
        self.pergunta_atual += 1
        if self.pergunta_atual < len(self.perguntas):
            self.label_pergunta.config(text=self.perguntas[self.pergunta_atual]["pergunta"])
            self.resposta_selecionada.set("")
            for widget in self.canvas.winfo_children():
                if isinstance(widget, tk.Radiobutton) or isinstance(widget, tk.Button) or isinstance(widget, tk.Label):
                    widget.destroy()
            for alternativa in self.perguntas[self.pergunta_atual]["alternativas"]:
                tk.Radiobutton(self.canvas, text=alternativa, variable=self.resposta_selecionada, value=alternativa).place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.botao_proxima = tk.Button(self.canvas, text="Próxima Pergunta", command=self.mostrar_proxima_pergunta)
            self.botao_proxima.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        else:
            messagebox.showinfo("Fim do jogo", "Fim do jogo!")
            self.exibir_perguntas_respondidas()  # Exibir as perguntas respondidas
    
    def exibir_perguntas_respondidas(self):
        # Ocultar o frame de perguntas atual
        self.label_pergunta.place_forget()
        self.resposta_selecionada.set("")  # Limpar a seleção
        
        # Criar um novo frame para exibir as perguntas respondidas
        self.frame_perguntas_respondidas = tk.Frame(self.canvas, bg="white")
        self.frame_perguntas_respondidas.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        
        # Adicionar um título
        titulo = tk.Label(self.frame_perguntas_respondidas, text="Perguntas Respondidas", bg="white", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)
        
        # Exibir as perguntas respondidas
        for i, pergunta in enumerate(self.perguntas):
            pergunta_texto = pergunta["pergunta"]
            resposta = pergunta["resposta"]
            label_pergunta = tk.Label(self.frame_perguntas_respondidas, text=f"Pergunta {i+1}: {pergunta_texto}", bg="white")
            label_resposta = tk.Label(self.frame_perguntas_respondidas, text=f"Resposta: {resposta}", bg="white", font=("Arial", 10, "italic"))
            label_pergunta.pack(anchor=tk.W)
            label_resposta.pack(anchor=tk.W)
    
    # Funções para mover o pássaro
    def mover_cima(self, event):
        self.canvas.move(self.passaro_id, 0, -10)
        self.verificar_colisao()
    
    def mover_baixo(self, event):
        self.canvas.move(self.passaro_id, 0, 10)
        self.verificar_colisao()
    
    def mover_esquerda(self, event):
        self.canvas.move(self.passaro_id, -10, 0)
        self.verificar_colisao()
    
    def mover_direita(self, event):
        self.canvas.move(self.passaro_id, 10, 0)
        self.verificar_colisao()
    
    # Função para verificar a colisão entre o pássaro e os insetos
    def verificar_colisao(self):
        passaro_bbox = self.canvas.bbox(self.passaro_id)
        for inseto_id in self.insetos:
            inseto_bbox = self.canvas.bbox(inseto_id)
            if passaro_bbox and inseto_bbox:
                x1, y1, x2, y2 = passaro_bbox
                ix1, iy1, ix2, iy2 = inseto_bbox
                if x2 > ix1 and x1 < ix2 and y2 > iy1 and y1 < iy2:
                    self.canvas.delete(inseto_id)
                    self.pontuacao += 1
                    self.canvas.itemconfig(self.pontuacao_label, text="Pontuação: {}".format(self.pontuacao))
                    x, y = random.randint(100, 700), random.randint(0, 550)
                    inseto_id = self.canvas.create_image(x, y, anchor=tk.NW, image=self.inseto_img)
                    self.insetos.append(inseto_id)

# Iniciar o jogo
if __name__ == "__main__":
    janela = tk.Tk()
    jogo = JogoPerguntas(janela)
    janela.mainloop()
