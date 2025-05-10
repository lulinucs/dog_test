from dog.dog_actor import DogActor
from dog.dog_interface import DogPlayerInterface
from dog.start_status import StartStatus
import tkinter as tk
from tkinter import messagebox, simpledialog

class JogoTeste(DogPlayerInterface):
    def __init__(self):
        super().__init__()
        self.dog_actor = DogActor()
        self.jogadores = []
        
        # Configuração da interface
        self.root = tk.Tk()
        self.root.title("Jogo de Teste DOG")
        
        # Área de mensagens
        self.frame_mensagens = tk.Frame(self.root)
        self.frame_mensagens.pack(pady=10)
        
        self.label_mensagens = tk.Label(self.frame_mensagens, text="Aguardando início...")
        self.label_mensagens.pack()
        
        # Botão para enviar mensagem
        self.frame_controles = tk.Frame(self.root)
        self.frame_controles.pack(pady=10)
        
        self.entry_mensagem = tk.Entry(self.frame_controles)
        self.entry_mensagem.pack(side=tk.LEFT, padx=5)
        
        tk.Button(self.frame_controles, text="Enviar Mensagem", 
                 command=self.enviar_mensagem).pack(side=tk.LEFT, padx=5)
        
        # Botão iniciar partida
        tk.Button(self.root, text="Iniciar Partida", 
                 command=self.iniciar_partida).pack(pady=10)

    def initialize(self):
        nome = simpledialog.askstring("Nome", "Digite seu nome:")
        if nome:
            resultado = self.dog_actor.initialize(nome, self)
            messagebox.showinfo("Status", resultado)
            return resultado
        return "Nome não fornecido"

    def iniciar_partida(self):
        status = self.dog_actor.start_match(2)  # 2 jogadores
        if status.code == '2':
            self.jogadores = status.players
            self.label_mensagens.config(text="Partida iniciada! Você pode enviar mensagens.")
        else:
            messagebox.showinfo("Erro", status.mensagem)

    def enviar_mensagem(self):
        if not self.jogadores:
            messagebox.showinfo("Erro", "Partida não iniciada!")
            return
            
        mensagem = self.entry_mensagem.get()
        if mensagem:
            self.dog_actor.send_move({
                'mensagem': mensagem,
                'match_status': 'next'
            })
            self.entry_mensagem.delete(0, tk.END)
            self.label_mensagens.config(text=f"Você enviou: {mensagem}")

    def receive_start(self, status: StartStatus):
        self.jogadores = status.players
        self.label_mensagens.config(text="Partida iniciada! Você pode enviar mensagens.")

    def receive_move(self, move):
        mensagem = move['mensagem']
        self.label_mensagens.config(text=f"Mensagem recebida: {mensagem}")

    def receive_withdrawal_notification(self):
        messagebox.showinfo("Fim de Jogo", "Um jogador abandonou a partida!")
        self.label_mensagens.config(text="Partida encerrada!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    jogo = JogoTeste()
    jogo.initialize()
    jogo.run() 