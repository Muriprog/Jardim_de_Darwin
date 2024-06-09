import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame

class QuizApp:
    def __init__(self, master, jogo):
        self.master = master
        self.jogo = jogo
        self.frame = tk.Frame(self.master, bg="white")
        self.frame.pack()

        self.categories = {
            "Pergunta 1": {
                "pergunta": "Assinale a alternativa que contém uma informação que NÃO é sustentada pela Teoria Evolutiva por Seleção Natural",
                "opcoes": [
                    "A) A reposição do fator de coagulação mediante transfusão de sangue aumenta a adaptabilidade dos hemofílicos.",
                    "B) Certas bactérias, em face de mudanças no ambiente, adquirem a capacidade de produzir novas substâncias.",
                    "C) O vírus HIV pode sofrer mutações, o que dificulta o tratamento de indivíduos soropositivos.",
                    "D) Os peixes cegos apresentam menor chance de sobrevivência em ambientes iluminados."
                ],
                "resposta": "B) Certas bactérias, em face de mudanças no ambiente, adquirem a capacidade de produzir novas substâncias."
            },
            "Pergunta 2": {
                "pergunta": "Embriões de vertebrados tendem a ser mais similares entre si do que os adultos correspondentes. Sobre esse fato, são feitas as seguintes afirmações",
                "opcoes": [
                    "I - As analogias observadas indicam uma origem comum.",
                    "II - O estudo da embriologia comparada contribui para a compreensão da evolução biológica.",
                    "III - Durante o desenvolvimento embrionário, os organismos passam por fases que repetem.",
                    "IV - As fases embrionárias dos vertebrados são sempre iguais."
                ],
                "resposta": "II - O estudo da embriologia comparada contribui para a compreensão da evolução biológica."
            },
            "Pergunta 3": {
                "pergunta": "Assinale a alternativa correta.",
                "opcoes": [
                    "I - Antes dos atuais conflitos, na década de 80, a distribuição de genes na população da Iugoslávia seguia o equilíbrio de Hardy-Weinberg.",
                    "II - Além do isolamento geográfico, aspectos culturais como os costumes e a religião influem na evolução das etnias humanas.",
                    "III - Os Bálcãs exemplificam bem que a migração aumenta a variabilidade genética.",
                    "IV - É provável que a frequência de heterozigose seja semelhante na população brasileira e na população sérvia."
                ],
                "resposta": "III - Os Bálcãs exemplificam bem que a migração aumenta a variabilidade genética."
            }
        }

        self.current_category = ""
        self.current_question_index = 0
        self.round_questions = []

        self.label_pergunta = tk.Label(self.frame, text="", font=("Arial", 14), bg="white")
        self.label_pergunta.pack(pady=10)

        self.opcoes_var = tk.StringVar(self.frame)
        self.opcoes_var.set("Selecione uma opção")
        self.opcoes_menu = tk.OptionMenu(self.frame, self.opcoes_var, "")
        self.opcoes_menu.pack(pady=10)

        self.botao_responder = tk.Button(self.frame, text="Responder", command=self.responder_pergunta, bg="#4CAF50", fg="white")
        self.botao_responder.pack(pady=5)

        self.botao_nova_rodada = tk.Button(self.frame, text="Nova Rodada", command=self.jogo.reiniciar_jogo, bg="#007BFF", fg="white")
        self.botao_nova_rodada.pack(pady=5)

        self.mostrar_nova_rodada()

    def mostrar_nova_rodada(self):
        self.current_category = random.choice(list(self.categories.keys()))
        self.round_questions = [self.categories[self.current_category]]
        self.current_question_index = 0
        self.mostrar_pergunta_atual()

    def mostrar_pergunta_atual(self):
        if self.current_question_index < len(self.round_questions):
            pergunta_atual = self.round_questions[self.current_question_index]
            self.label_pergunta.config(text=f"Pergunta: {pergunta_atual['pergunta']}")
            self.opcoes_menu["menu"].delete(0, "end")
            for opcao in pergunta_atual["opcoes"]:
                self.opcoes_menu["menu"].add_command(label=opcao, command=tk._setit(self.opcoes_var, opcao))
        else:
            messagebox.showinfo("Fim da Rodada", f"Fim da rodada! Sua pontuação: {self.jogo.pontuacao}")

    def responder_pergunta(self):
        resposta_usuario = self.opcoes_var.get()
        resposta_correta = self.round_questions[self.current_question_index]["resposta"]
        if resposta_usuario == resposta_correta:
            self.jogo.pontuacao += 1
            messagebox.showinfo("Resposta Correta", "Parabéns! Sua resposta está correta!")
        else:
            messagebox.showerror("Resposta Incorreta", f"A resposta correta era: {resposta_correta}")
            self.jogo.reiniciar_jogo()  # Reiniciar o jogo se a resposta estiver incorreta

        self.current_question_index += 1
        self.mostrar_pergunta_atual()

        # Checa se todas as perguntas foram respondidas e fecha a janela do quiz
        if self.current_question_index >= len(self.round_questions):
            self.master.destroy()
            self.jogo.mostrar_segunda_fase()

class Jogo:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo e Quiz")
        self.master.state('zoomed')  # Define a janela para abrir maximizada

        self.master = master
        self.master.title("Jogo e Quiz")
        self.master.state('zoomed')  # Define a janela para abrir maximizada
        
        self.canvas = tk.Canvas(self.master, bg="green")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.pontuacao = 0
        self.quiz_aberto = False
        self.imortal = False  # Variável para controlar o estado de imortalidade do tentilhão

        self.botao_iniciar = tk.Button(self.master, text="INICIAR", command=self.iniciar_jogo, bg="#007BFF", fg="white", font=("Arial", 24))
        self.botao_iniciar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.canvas.focus_set()
        self.canvas.bind("<Up>", self.mover_cima)
        self.canvas.bind("<Down>", self.mover_baixo)
        self.canvas.bind("<Left>", self.mover_esquerda)
        self.canvas.bind("<Right>", self.mover_direita)

        self.canvas.bind("w", self.mover_cima)
        self.canvas.bind("s", self.mover_baixo)
        self.canvas.bind("a", self.mover_esquerda)
        self.canvas.bind("d", self.mover_direita)

        self.master.bind("<Configure>", self.on_resize)

        self.tentilhao_posicao = (0, 0)

    def iniciar_jogo(self):
        self.botao_iniciar.destroy()
        self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, text="PRIMEIRA FASE", font=("Arial", 30), fill="white")
        self.desativar_imortalidade()  # Desativa a imortalidade imediatamente ao começar uma fase
        self.remover_texto_e_comecar_jogo()  # Chama diretamente a função para remover o texto e começar o jogo

    def remover_texto_e_comecar_jogo(self):
        self.canvas.delete("all")
        self.desenhar_grama()
        self.desenhar_animais()

    def reiniciar_jogo(self):
        self.canvas.delete("all")
        self.pontuacao = 0  # Reinicia a pontuação
        self.quiz_aberto = False
        self.imortal = False  # Desativa a imortalidade
        self.desenhar_grama()
        self.desenhar_animais()

    def iniciar_nova_fase(self):
        self.quiz_aberto = False
        self.desenhar_grama()
        self.desenhar_animais()
        self.desativar_imortalidade()  # Desativa a imortalidade imediatamente ao começar uma fase

    def desenhar_grama(self):
        self.canvas.delete("grama")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        for y in range(0, canvas_height, 10):
            for x in range(0, canvas_width, 10):
                if random.random() < 0.5:
                    cor = "#006400"  # Verde escuro
                else:
                    cor = "#008000"  # Verde claro
                self.canvas.create_rectangle(x, y, x+10, y+10, fill=cor, outline="", tags="grama")

    def desenhar_animais(self):
        self.imagem_inseto = Image.open("insetos.png").resize((60, 60))
        self.inseto_img = ImageTk.PhotoImage(self.imagem_inseto)

        self.imagem_besouro = Image.open("besouro.png").resize((60, 60))
        self.besouro_img = ImageTk.PhotoImage(self.imagem_besouro)

        self.imagem_passaro = Image.open("Tentilhao.png").resize((75, 75))
        self.passaro = ImageTk.PhotoImage(self.imagem_passaro)

        self.pontuacao_label = self.canvas.create_text(50, 50, anchor=tk.NW, text="Pontuação: {}".format(self.pontuacao), fill="white", font=("Arial", 15))

        self.insetos = []
        self.besouros = []

        # Posição inicial do pássaro
        x_passaro, y_passaro = random.randint(200, self.canvas.winfo_width() - 200), random.randint(200, self.canvas.winfo_height() - 200)

        for _ in range(5):
            x, y = random.randint(0, self.canvas.winfo_width() - 60), random.randint(0, self.canvas.winfo_height() - 60)
            while abs(x - x_passaro) < 100 and abs(y - y_passaro) < 100:
                x, y = random.randint(0, self.canvas.winfo_width() - 60), random.randint(0, self.canvas.winfo_height() - 60)
            inseto_id = self.canvas.create_image(x, y, anchor=tk.NW, image=self.inseto_img)
            self.insetos.append({"id": inseto_id, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])})

        for _ in range(5):
            x, y = random.randint(0, self.canvas.winfo_width() - 60), random.randint(0, self.canvas.winfo_height() - 60)
            while abs(x - x_passaro) < 100 and abs(y - y_passaro) < 100:
                x, y = random.randint(0, self.canvas.winfo_width() - 60), random.randint(0, self.canvas.winfo_height() - 60)
            besouro_id = self.canvas.create_image(x, y, anchor=tk.NW, image=self.besouro_img)
            self.besouros.append({"id": besouro_id, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])})

        self.passaro_id = self.canvas.create_image(x_passaro, y_passaro, anchor=tk.NW, image=self.passaro)
        self.tentilhao_posicao = (x_passaro, y_passaro)

        self.move_animais()

    def ativar_imortalidade(self):
        self.imortal = True
        self.master.after(3000, self.desativar_imortalidade)  # Desativa a imortalidade após 3 segundos

    def desativar_imortalidade(self):
        self.imortal = False

    def mover_cima(self, event):
        if not self.imortal:  # Verifica se o tentilhão não está imortal
            self.canvas.move(self.passaro_id, 0, -25)
            self.tentilhao_posicao = self.canvas.coords(self.passaro_id)[:2]
            self.verificar_colisao()

    def mover_baixo(self, event):
        if not self.imortal:
            self.canvas.move(self.passaro_id, 0, 25)
            self.tentilhao_posicao = self.canvas.coords(self.passaro_id)[:2]
            self.verificar_colisao()

    def mover_esquerda(self, event):
        if not self.imortal:
            self.canvas.move(self.passaro_id, -25, 0)  # Movendo o pássaro para a esquerda
            self.tentilhao_posicao = self.canvas.coords(self.passaro_id)[:2]
            self.verificar_colisao()  # Verificando colisão após o movimento

    def mover_direita(self, event):
        if not self.imortal:
            self.canvas.move(self.passaro_id, 25, 0)
            self.tentilhao_posicao = self.canvas.coords(self.passaro_id)[:2]
            self.verificar_colisao()

    def verificar_colisao(self):
        passaro_coords = self.canvas.bbox(self.passaro_id)
        insetos_a_remover = []
        for inseto in self.insetos:
            inseto_coords = self.canvas.bbox(inseto["id"])
            if self.is_collision(passaro_coords, inseto_coords):
                self.pontuacao += 1
                self.canvas.delete(inseto["id"])
                insetos_a_remover.append(inseto)
                self.canvas.itemconfig(self.pontuacao_label, text="Pontuação: {}".format(self.pontuacao))
        
        for inseto in insetos_a_remover:
            self.insetos.remove(inseto)
        
        # Checar se todos os insetos foram comidos e abrir o quiz
        if not self.insetos and not self.quiz_aberto:
            self.quiz_aberto = True
            self.abrir_quiz()

        for besouro in self.besouros:
            besouro_coords = self.canvas.bbox(besouro["id"])
            if self.is_collision(passaro_coords, besouro_coords):
                if not self.quiz_aberto:  # Verifica se o quiz não está aberto antes de mostrar o fim de jogo
                    messagebox.showinfo("Fim de Jogo", "Você perdeu o jogo!")
                    self.reiniciar_jogo()

    def is_collision(self, bbox1, bbox2):
        return not (bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3])

    def move_animais(self):
        for inseto in self.insetos:
            self.canvas.move(inseto["id"], inseto["dx"], inseto["dy"])
            coords = self.canvas.bbox(inseto["id"])
            if coords[0] <= 0 or coords[2] >= self.canvas.winfo_width():
                inseto["dx"] = -inseto["dx"]
            if coords[1] <= 0 or coords[3] >= self.canvas.winfo_height():
                inseto["dy"] = -inseto["dy"]

        for besouro in self.besouros:
            self.canvas.move(besouro["id"], besouro["dx"], besouro["dy"])
            coords = self.canvas.bbox(besouro["id"])
            if coords[0] <= 0 or coords[2] >= self.canvas.winfo_width():
                besouro["dx"] = -besouro["dx"]
            if coords[1] <= 0 or coords[3] >= self.canvas.winfo_height():
                besouro["dy"] = -besouro["dy"]

        self.verificar_colisao()
        self.master.after(50, self.move_animais)

    def abrir_quiz(self):
        quiz_janela = tk.Toplevel(self.master)
        quiz_janela.title("Quiz")
        quiz_app = QuizApp(quiz_janela, self)

    def mostrar_segunda_fase(self):
        self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, text="SEGUNDA FASE", font=("Arial", 30), fill="white", tags="segunda_fase")
        self.master.after(1000, self.remover_texto_e_reiniciar_jogo)

    def remover_texto_e_reiniciar_jogo(self):
        self.canvas.delete("segunda_fase")
        self.iniciar_nova_fase()

    def on_resize(self, event):
        self.desenhar_grama()

    def aumentar_volume(self):
        if self.volume_atual < 1.0:
            self.volume_atual += 0.1  # Aumenta o volume em 10%
            pygame.mixer.music.set_volume(self.volume_atual)
            self.atualizar_label_volume()

    def diminuir_volume(self):
        if self.volume_atual > 0.0:
            self.volume_atual -= 0.1  # Diminui o volume em 10%
            pygame.mixer.music.set_volume(self.volume_atual)
            self.atualizar_label_volume()

    def atualizar_label_volume(self):
        volume_percentual = int(self.volume_atual * 100)
        self.label_volume.config(text="Volume: {}%".format(volume_percentual))

def main():
    pygame.init()
    pygame.mixer.music.load('lofi.mp3')

    root = tk.Tk()
    jogo = Jogo(root)

    pygame.mixer.music.set_volume(0.075)  # Defina o volume para 50%

    pygame.mixer.music.play(loops=-1)  # Reproduzir a música em loop

    root.mainloop()

    pygame.mixer.music.stop()

if __name__ == "__main__":
    main()
