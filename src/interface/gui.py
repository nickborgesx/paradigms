import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import Frame, Text, Button, END, Label
from src.lexer import lexer

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Analisador Léxico XML")
        self.root.configure(background="#f0f0f0")
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.style.configure('Treeview', font=('Consolas', 9), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'))
        self.style.map('TButton', 
                      foreground=[('pressed', 'white'), ('active', 'white')],
                      background=[('pressed', '#0052cc'), ('active', '#0066ff')])
        
        self.cria_layout()
        self.configura_botoes()
        
    def cria_layout(self):
        # Frame principal com layout em duas colunas
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Coluna esquerda (Editor e Botões)
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Frame do editor (parte superior esquerda)
        self.editor_frame = ttk.Frame(self.left_frame)
        self.editor_frame.pack(fill='both', expand=True)
        
        # Scrollbar para o editor
        scroll_y = ttk.Scrollbar(self.editor_frame)
        scroll_y.pack(side='right', fill='y')
        
        # Caixa de texto para o XML
        self.codigo_entry = Text(
            self.editor_frame, 
            wrap='word', 
            font=('Consolas', 10),
            undo=True, 
            yscrollcommand=scroll_y.set,
            padx=5, 
            pady=5,
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.codigo_entry.pack(fill='both', expand=True)
        scroll_y.config(command=self.codigo_entry.yview)
        
        # Frame dos botões (parte inferior esquerda)
        self.button_frame = ttk.Frame(self.left_frame)
        self.button_frame.pack(fill='x', pady=(10, 0))
        
        # Coluna direita (Resultados)
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side='right', fill='both', expand=True)
        
        # Frame dos resultados
        self.result_frame = ttk.LabelFrame(self.right_frame, text=" Resultados da Análise ", padding=10)
        self.result_frame.pack(fill='both', expand=True)
        
        # Scrollbars para a Treeview
        scroll_y2 = ttk.Scrollbar(self.result_frame)
        scroll_y2.pack(side='right', fill='y')
        
        scroll_x2 = ttk.Scrollbar(self.result_frame, orient='horizontal')
        scroll_x2.pack(side='bottom', fill='x')
        
        # Treeview para mostrar tokens
        columns = ('line', 'position', 'token', 'lexeme', 'notification')
        self.saida = ttk.Treeview(
            self.result_frame, 
            columns=columns, 
            show='headings',
            yscrollcommand=scroll_y2.set,
            xscrollcommand=scroll_x2.set,
            selectmode='extended'
        )
        
        # Configuração das colunas
        self.saida.heading('line', text='Linha', anchor='w')
        self.saida.heading('position', text='Posição', anchor='w')
        self.saida.heading('token', text='Token', anchor='w')
        self.saida.heading('lexeme', text='Lexema', anchor='w')
        self.saida.heading('notification', text='Notificação', anchor='w')
        
        self.saida.column('line', width=50, minwidth=50, stretch=False)
        self.saida.column('position', width=70, minwidth=70, stretch=False)
        self.saida.column('token', width=120, minwidth=100)
        self.saida.column('lexeme', width=200, minwidth=150)
        self.saida.column('notification', width=200, minwidth=150)
        
        self.saida.pack(fill='both', expand=True)
        
        scroll_y2.config(command=self.saida.yview)
        scroll_x2.config(command=self.saida.xview)
        
        # Adiciona tags para cores alternadas
        self.saida.tag_configure('oddrow', background='#f9f9f9')
        self.saida.tag_configure('evenrow', background='#ffffff')
        
    def configura_botoes(self):
        # Botão Importar
        btn_importar = ttk.Button(
            self.button_frame, 
            text="Importar XML", 
            command=self.importar_xml,
            style='Accent.TButton'
        )
        btn_importar.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        # Botão Analisar
        btn_analisar = ttk.Button(
            self.button_frame, 
            text="Analisar", 
            command=self.chama_lexer,
            style='Accent.TButton'
        )
        btn_analisar.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        # Botão Limpar
        btn_limpar = ttk.Button(
            self.button_frame, 
            text="Limpar", 
            command=self.limpar_campos
        )
        btn_limpar.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        # Configura estilo para botão de destaque
        self.style.configure('Accent.TButton', foreground='white', background='#0078d7')
        
        # Barra de status
        self.status_bar = ttk.Label(
            self.root, 
            text="Pronto", 
            relief='sunken', 
            anchor='w',
            font=('Segoe UI', 9)
        )
        self.status_bar.pack(fill='x', side='bottom', ipady=5)
        
    def importar_xml(self):
        try:
            filepath = filedialog.askopenfilename(
                title="Selecione um arquivo XML",
                filetypes=(("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*")))
            
            if filepath:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.codigo_entry.delete("1.0", END)
                    self.codigo_entry.insert("1.0", content)
                self.status_bar.config(text=f"Arquivo carregado: {filepath}")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{str(e)}")
            self.status_bar.config(text="Erro ao carregar arquivo")
            
    def chama_lexer(self):
        self.saida.delete(*self.saida.get_children())  # Limpa a saída
        input_data = self.codigo_entry.get("1.0", END)
        
        if not input_data.strip():
            messagebox.showwarning("Aviso", "Por favor, insira um código XML ou importe um arquivo.")
            return
            
        try:
            # Versão simplificada da análise para evitar travamentos
            lexer.input(input_data)
            tokens = []
            
            # Coleta todos os tokens primeiro
            while True:
                tok = lexer.token()
                if not tok:
                    break
                tokens.append(tok)
            
            # Processa os tokens coletados
            for i, tok in enumerate(tokens):
                line_number = input_data.count('\n', 0, tok.lexpos) + 1
                position = tok.lexpos
                token_type = tok.type
                lexeme = tok.value
                notification = ''
                
                # Alterna as cores das linhas
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                
                # Insere os valores na Treeview
                self.saida.insert('', 'end', values=(
                    line_number, position, token_type, lexeme, notification), tags=(tag))
                
                # Atualiza a interface periodicamente
                if i % 100 == 0:
                    self.root.update()
            
            self.status_bar.config(text=f"Análise concluída - {len(tokens)} tokens encontrados")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a análise:\n{str(e)}")
            self.status_bar.config(text="Erro durante a análise")
            
    def limpar_campos(self):
        self.codigo_entry.delete("1.0", END)
        self.saida.delete(*self.saida.get_children())
        self.status_bar.config(text="Campos limpos")
        
    def run(self):
        # Centraliza a janela
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()