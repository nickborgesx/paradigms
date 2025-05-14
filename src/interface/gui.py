import tkinter as tk
from tkinter import ttk
from tkinter import Frame, Text, Button, END
from src.lexer import lexer

root = tk.Tk()


class Application:
    def __init__(self):
        self.root = root
        self.root.title("Analisador Léxico XML")
        self.root.configure(background="#DCDCDC")
        self.root.geometry("900x700")
        self.frames_da_tela()
        self.botoes()

    def frames_da_tela(self):
        # Frame para entrada do XML
        self.frame_1 = Frame(self.root, bd=4, bg="#DCDCDC",
                             highlightbackground="grey", highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.07, relwidth=0.96, relheight=0.55)

        # Frame para saída da análise léxica
        self.frame_2 = Frame(self.root, bd=4, bg="#DCDCDC",
                             highlightbackground="grey", highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.70, relwidth=0.96, relheight=0.20)

        # Caixa de texto para digitar ou colar XML
        self.codigo_entry = Text(self.frame_1, wrap='word')
        # espaço extra para os botões
        self.codigo_entry.pack(fill='both', expand=True, padx=5, pady=(5, 40))

        # Treeview para mostrar tokens
        columns = ('line', 'position', 'token', 'lexeme', 'notification')
        self.saida = ttk.Treeview(
            self.frame_2, columns=columns, show='headings')

        self.saida.heading('line', text='Linha')
        self.saida.heading('position', text='Posição')
        self.saida.heading('token', text='Token')
        self.saida.heading('lexeme', text='Lexema')
        self.saida.heading('notification', text='Notificação')

        self.saida.pack(fill='both', expand=True)

    def botoes(self):
        # Botões na parte inferior direita do frame_1
        botao_frame = Frame(self.frame_1, bg="#DCDCDC")
        botao_frame.place(relx=0.7, rely=0.93, relwidth=0.28)

        btn_analisar = Button(botao_frame, text="Analisar",
                              command=self.chama_lexer, width=12)
        btn_analisar.pack(side='right', padx=5, pady=5)

        btn_limpar = Button(botao_frame, text="Limpar",
                            command=self.limpar_campos, width=12)
        btn_limpar.pack(side='right', padx=5, pady=5)

    def chama_lexer(self):
        self.saida.delete(*self.saida.get_children())  # Limpa a saída
        input_data = self.codigo_entry.get("1.0", END)

        lexer.input(input_data)

        for tok in lexer:
            # calcula a linha contando quantas quebras vieram antes de lexpos
            line_number = input_data.count('\n', 0, tok.lexpos) + 1
            position = tok.lexpos
            token_type = tok.type
            lexeme = tok.value
            notification = ''

            # Insere os valores na Treeview
            self.saida.insert('', 'end', values=(
                line_number, position, token_type, lexeme, notification))

    def limpar_campos(self):
        self.codigo_entry.delete("1.0", END)
        self.saida.delete(*self.saida.get_children())

    def run(self):
        self.root.mainloop()
