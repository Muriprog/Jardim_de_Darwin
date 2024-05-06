import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame

class Jogo:
    pontuacao_total = 0

    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="green")
        self.canvas.pack()

        self.imagem_passaro = Image.open("Tentilhao.png").resize((50, 50))
        self.passaro = ImageTk.PhotoImage(self.imagem_passaro)
        self.passaro_id = self.canvas.create_image(50, 300, anchor=tk.NW, image=self.passaro)

        self.imagem_inseto = Image.open("insetos.png").resize((60, 60))
        self.inseto_img = ImageTk.PhotoImage(self.imagem_inseto)

        self.imagem_besouro = Image.open("besouro.png").resize((60, 60))
        self.besouro_img = ImageTk.PhotoImage(self.imagem_besouro)

        self.pontuacao_label = self.canvas.create_text(50, 50, anchor=tk.NW, text="Pontuação Total: {}".format(self.pontuacao_total), fill="white", font=("Arial", 15))

        self.insetos = []
        self.besouros = []

        for _ in range(5):
            self.adicionar_inseto()

        for _ in range(5):
            x, y = random.randint(100, 700), random.randint(0, 550)
            besouro_id = self.canvas.create_image(x, y, anchor=tk.NW, image=self.besouro_img)
            self.besouros.append(besouro_id)
            self.canvas.tag_raise(self.passaro_id, besouro_id)

        self.canvas.focus_set()
        self.canvas.bind("<Up>", self.mover_cima)
        self.canvas.bind("<Down>", self.mover_baixo)
        self.canvas.bind("<Left>", self.mover_esquerda)
        self.canvas.bind("<Right>", self.mover_direita)

        self.canvas.bind("w", self.mover_cima)
        self.canvas.bind("s", self.mover_baixo)
        self.canvas.bind("a", self.mover_esquerda)
        self.canvas.bind("d", self.mover_direita)

        self.master.after(5000, self.abrir_quiz)

    def adicionar_inseto(self):
        x, y = random.randint(100, 700), random.randint(0, 550)
        inseto_id = self.canvas.create_image(x, y, anchor=tk.NW, image=self.inseto_img)
        self.insetos.append(inseto_id)
        self.canvas.tag_raise(inseto_id)

    def remover_inseto(self, inseto_id):
        self.canvas.delete(inseto_id)
        self.insetos.remove(inseto_id)
        self.adicionar_inseto()

    def mover_cima(self, event):
        self.canvas.move(self.passaro_id, 0, -15)
        self.verificar_colisao()

    def mover_baixo(self, event):
        self.canvas.move(self.passaro_id, 0, 15)
        self.verificar_colisao()

    def mover_esquerda(self, event):
        self.canvas.move(self.passaro_id, -15, 0)
        self.verificar_colisao()

    def mover_direita(self, event):
        self.canvas.move(self.passaro_id, 15, 0)
        self.verificar_colisao()

    def verificar_colisao(self):
        passaro_bbox = self.canvas.bbox(self.passaro_id)
        for inseto_id in self.insetos:
            if passaro_bbox and self.canvas.find_overlapping(*passaro_bbox) and inseto_id in self.canvas.find_overlapping(*passaro_bbox):
                self.remover_inseto(inseto_id)
                self.pontuacao_total += 1
                self.atualizar_pontuacao_na_interface()
                break

    def abrir_quiz(self):
        self.canvas.delete("all")
        quiz_app = QuizApp(self.master)
        self.canvas.bind("<Up>", lambda event: None)
        self.canvas.bind("<Down>", lambda event: None)
        self.canvas.bind("<Left>", lambda event: None)
        self.canvas.bind("<Right>", lambda event: None)

    def atualizar_pontuacao_na_interface(self):
        self.canvas.itemconfig(self.pontuacao_label, text="Pontuação Total: {}".format(self.pontuacao_total))

class QuizApp:
    def __init__(self, master):
        self.master = master
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
                "pergunta": " Assinale a alternativa correta.",
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
        self.score = 0

        self.label_pergunta = tk.Label(self.frame, text="", font=("Arial", 14), bg="white")
        self.label_pergunta.pack(pady=10)

        self.opcoes_var = tk.StringVar(self.frame)
        self.opcoes_var.set("Selecione uma opção")
        self.opcoes_menu = tk.OptionMenu(self.frame, self.opcoes_var, "")
        self.opcoes_menu.pack(pady=10)

        self.botao_responder = tk.Button(self.frame, text="Responder", command=self.responder_pergunta, bg="#4CAF50", fg="white")
        self.botao_responder.pack(pady=5)

        self.mostrar_nova_rodada()

    def mostrar_nova_rodada(self):
        keys = list(self.categories.keys())
        random.shuffle(keys)
        self.round_questions = [self.categories[key] for key in keys]
        self.current_question_index = 0
        self.score = 0
        self.mostrar_pergunta_atual()

    def atualizar_pontuacao_total(self):
        self.master.update_idletasks()  # Atualizar a interface antes de exibir a mensagem
        self.master.after(100, lambda: messagebox.showinfo("Fim da Rodada", f"Fim da rodada! Sua pontuação: {self.score}\nPontuação Total: {Jogo.pontuacao_total}"))

    def mostrar_pergunta_atual(self):
        if self.current_question_index < len(self.round_questions):
            pergunta_atual = self.round_questions[self.current_question_index]
            self.label_pergunta.config(text=f"Pergunta: {pergunta_atual['pergunta']}")
            self.opcoes_menu["menu"].delete(0, "end")
            for opcao in pergunta_atual["opcoes"]:
                self.opcoes_menu["menu"].add_command(label=opcao, command=tk._setit(self.opcoes_var, opcao))
        else:
            messagebox.showinfo("Fim da Rodada", f"Fim da rodada! Sua pontuação: {self.score}\nPontuação Total: {Jogo.pontuacao_total}")

            # Exibir a pontuação total após a rodada
            self.master.update_idletasks()  # Atualizar a interface antes de exibir a mensagem

    def responder_pergunta(self):
        resposta_usuario = self.opcoes_var.get()
        resposta_correta = self.round_questions[self.current_question_index]["resposta"]
        if resposta_usuario == resposta_correta:
            self.score += 5
            Jogo.pontuacao_total += 5
            messagebox.showinfo("Resposta Correta", "Parabéns! Sua resposta está correta!")
        else:
            messagebox.showerror("Resposta Incorreta", f"A resposta correta era: {resposta_correta}")

        self.current_question_index += 1
        self.mostrar_pergunta_atual()

    def nova_rodada(self):
        self.mostrar_nova_rodada()

def main():
    pygame.init()
    pygame.mixer.music.load('lofi.mp3')

    janela = tk.Tk()
    janela.title("Jogo e Quiz")
    jogo = Jogo(janela)

    pygame.mixer.music.play(loops=-1)

    janela.mainloop()

    pygame.mixer.music.stop()

if __name__ == "__main__":
    main()
