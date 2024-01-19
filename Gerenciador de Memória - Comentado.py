# Importações de bibliotecas

# Bibliotecas de Tkinter para a parte visual
from tkinter import *

# Biblioteca para caixa de mensagem
from tkinter import messagebox
import tkinter as tk

# Bibioteca para janela com entrada de dados
import tkinter.simpledialog
from tkinter import ttk

# Biblioteca de iteração
import itertools

# Biblioteca para geração random de valores
import random

# Biblioteca com alfabeto
import string

# Gera nomes em ordem alfabética
def gerador_nome_processo():
    tamanho = 1
    while True:
        for s in itertools.product(string.ascii_uppercase, repeat=tamanho):
            yield "".join(s)
        tamanho += 1

# Objeto do Gerenciador de Memório
class GerenciadorMemoria:
    
    # Atributos do objeto
    def __init__(self, mestre):
        self.mestre = mestre
        self.grade = [None] * 100
        self.grupos = {}
        self.chars = gerador_nome_processo()
        self.status = [0] * 100
        self.criar_grade()
        
    # Métodos do objeto
    
    # Cria grade de memória de 100 blocos 
    def criar_grade(self):
        quadro = tk.Frame(self.mestre)
        quadro.pack(expand=True)
        for i in range(100):
            rotulo = tk.Label(quadro, bg="white", width=10, height=3, relief="solid", borderwidth=1.2)
            rotulo.grid(row=i//10, column=i%10)
            self.grade[i] = rotulo
            
    # Aloca processo na memória
    def alocar(self):
        # Solicita ao usuário o tamanho do processo
        n = tkinter.simpledialog.askinteger("Alocar", "Digite o Tamanho do Processo")
        blocos_livres = []
        best_fit = None
        total_livre = 0
        
        # Procura um espaço livre de tamanho exato ou maior com a menor quantidade sobrando
        for i in range(100):
            
            # Verifica todos os espaços livres e adiciona a uma lista e acrescenta no contador a quantidade livre
            if self.status[i] == 0:
                total_livre += 1
                blocos_livres.append(i)
            
            # Ao achar um bloco ocupado, verifica se o tamanho livre adicionado anteriormente é maior ou igual a entrada de tamanho do usuário e salva as posições na variável best_fit
            else:    
                if len(blocos_livres) >= n:
                    if best_fit is None or len(best_fit) > len(blocos_livres):
                        best_fit = list(blocos_livres)
                
                # Após alocar o processo no menor espaço disponível, limpa a lista dos blocos_livres que está desatualizada para o próximo processo solicitado pelo usuário
                blocos_livres = []
                
        if len(blocos_livres) >= n:
            if best_fit is None or len(best_fit) > len(blocos_livres):
                best_fit = list(blocos_livres)
                
        # Se não houver espaço livre total suficiente, uma mensagem de erro é exibida
        if total_livre < n:
            messagebox.showinfo("Erro", "Sem Espaço Total")
            return
        
        # Se não houver espaço livre sequencial suficiente, uma mensagem de erro é exibida
        if best_fit is None:
            messagebox.showinfo("Erro", "Sem Espaço Sequencial")
            return

        # Chama a função para gerar o nome do processo e gera uma cor aleatória 
        nome_bloco = next(self.chars)
        cor_bloco = "#{:06x}".format(random.randint(0x0000, 0xFFFFFF))
        
        # Aloca na memória usando as posições da variável best_fit, altera seu status para "1" com o nome em ordem alfabética e cor aleatória
        for k in range(n):
            self.status[best_fit[k]] = 1
            
            # Altera parte visual do Tkinter, adicionando o nome do processo e sua cor
            self.grade[best_fit[k]]["text"] = nome_bloco
            self.grade[best_fit[k]]["background"] = cor_bloco
        
    # Desalocar um processo
    def desalocar(self):
        
        # Solicita ao usuário o nome do processo para desalocar
        d = tkinter.simpledialog.askstring("Desalocar", "Digite o Nome do Processo")
        
        # Busca o processo pelo nome do processo declarado pelo usuário e altera para "0"
        for i in range(100):
            if self.grade[i]["text"] == d.upper():
                self.status[i] = 0
                
                # Altera parte visual do Tkinter, removendo o nome do processo e mudando sua cor para branco
                self.grade[i]["text"] = ""
                self.grade[i]['background'] = "white"
                
    # Busca nas 100 posições todos os processos que não estão livres e muda de "1" para "0" o status e altera para sem texto e cor branca visualmente 
    def limpar_processos(self):
        for i in range(100):
            if self.status[i] == 1:
                self.status[i] = 0
                
                # Altera parte visual do Tkinter
                self.grade[i]["text"] = ""
                self.grade[i]["background"] = "white"
                
    # Realoca um processo por vez a cada clique
    def realocar(self):
        tamanho_processo = 0
        texto_memoria = None
        cor_memória = None
        
        # Começa na posição 1 para evitar o primeiro processo e achar os espaços vazio entre os processos
        for pos in range(1, 100):
            
            # Verifica se a posição anterior está vazia e se a atual está ocupada, localizando o começo de um processo
            if self.status[pos - 1] == 0 and self.status[pos] == 1:
                
                # Salva o texto e memória do processo atual para atualizar visualmente no Tkinter
                texto_memoria = self.grade[pos]["text"]
                cor_memória = self.grade[pos]["background"]
                
                # Enquanto o nome do processo for o mesmo, conta seu tamanho e a posição em que está dentro da lista
                while pos < 100 and self.grade[pos]["text"] == texto_memoria:
                    tamanho_processo += 1
                    pos += 1
                break
        
        # Altera os dados da posição atual do processo     
        for pos in range(100):
            
            # Enquanto o nome do processo for o mesmo, altera seu status para "0"
            if texto_memoria == self.grade[pos]["text"]:
                self.status[pos] = 0
                
                # Altera parte visual do Tkinter, removendo o nome do processo e mudando sua cor para branco
                self.grade[pos]["text"] = ""
                self.grade[pos]["background"] = "white"
        
        # Faz a busca na lista até achar o primeiro bloco livre e verifica se a memória é maior que zero, alterando seu status para "1"         
        for pos in range(100):
            if self.status[pos] == 0 and tamanho_processo > 0:
                self.status[pos] = 1
                
                # Altera parte visual do Tkinter, removendo o nome do processo e mudando sua cor para branco e diminui um contador referente ao tamanho do processo
                self.grade[pos]["text"] = texto_memoria
                self.grade[pos]["background"] = cor_memória
                tamanho_processo -= 1
        
        # Atualiza a cada realocação de processo visualmente no Tkinter
        return self.grade
    
    # Botão de Ajuda para o usuário
    def ajuda(self):
        
        # Define que a janela aparecerá por cima do programa
        janela_ajuda = tk.Toplevel()
        
        #Título da janela
        janela_ajuda.title("Ajuda")
        
        # Definição do tamanho e posição da janela centralizado conforme a tela do usuário ao fazer SysCall para o Windows
        largura_ajuda = 600
        altura_ajuda = 300
        largura_tela = raiz.winfo_screenwidth()
        altura_tela = raiz.winfo_screenheight()
        x = (largura_tela/2) - (largura_ajuda/2)
        y = (altura_tela/2) - (altura_ajuda/2)
        janela_ajuda.geometry('%dx%d+%d+%d' % (largura_ajuda, altura_ajuda, x, y))
        
        # Título dentro da janela de ajuda
        Info = Label(janela_ajuda, text="Explicação do funcionamento de cada botão")
        Info.pack(padx=10, pady=3)
        nb = ttk.Notebook(janela_ajuda, width=600, height=400)
        nb.pack(padx=10, pady=10)
        
        # Aba sobre o Funcionamento do Programa
        funcionamento = Frame(nb)
        nb.add(funcionamento, text="Funcionamento do Programa")
        label_funcionamento = Label(funcionamento, text="Esse Programa simula uma memória de um computador.\nVocê poderá alocar processos em uma memória com até 100 blocos de memória\n os processos serão criadas em ordem alfabética e cores aleatórias.\nVocê poderá desalocar um processo especifico da memória ou limpar todos os processos.\nConforme o uso do programa haverá espaços vazios no meio de processos que não podem ser alocados\n com processos maiores, então o programa possui um meio de realocar os blocos de processos até o inicio\n da memória e liberar o mesmo espaço vazio para a parte final da memória.")
        label_funcionamento.pack(pady=20, anchor=CENTER, fill="both")
        
        # Rodapé com o nome dos criadores do programa
        label_criadores = Label(funcionamento, text="Desenvolvido por: Guilherme Penso, Matheus Guilherme, Murilo Lustosa\n e Emanoel Andre.")
        label_criadores.pack(padx=10, pady=0)
        label_criadores.config(font="Arial 12")
        
        # Aba sobre o funcionamento da Alocação
        Alocar = Frame(nb)
        label_info = Label(Alocar, text="Funcionamento do Botão Alocar.")
        label_info.pack(padx=10, pady=10)
        mensagem_alocar = Label(Alocar, text="Antes de alocar um processo, a memória estará vazia. Após o clicar no botão Alocar, abrirá uma aba\n onde é possível adicionar o tamanho de um processo com números inteiros, após confirmar\n o tamanho, a Memória adicionará um processo com a quantidade de blocos nomeada de forma sequencial\n do alfabeto e cor aleatória.")
        mensagem_alocar.pack()
        nb.add(Alocar, text="Alocar")
        
        # Aba sobre o funcionamento da Desalocação
        Desalocar = Frame(nb)
        label_info2 = Label(Desalocar, text="Funcionamento do Botão Desalocar.")
        label_info2.pack(padx=10, pady=10)
        mensagem_desalocar = Label(Desalocar, text="A Memória estando com pelo menos um processo alocado, é possível desalocar com a letra correspondente\n ao processo, que irá remover o processo em específico.")
        mensagem_desalocar.pack()
        nb.add(Desalocar, text="Desalocar")
        
        # Aba sobre o funcionamento do Desalocar Tudo
        Desalocar_tudo = Frame(nb)
        label_info3 = Label(Desalocar_tudo, text="Funcionamento do Botão Limpar Processos.")
        label_info3.pack(padx=10, pady=10)
        mensagem_desalocar_tudo = Label(Desalocar_tudo, text="A Memória estando com um ou mais processos, é possível apagar tudo ao clicar no botão Limpar Processos.")
        mensagem_desalocar_tudo.pack()
        nb.add(Desalocar_tudo, text="Limpar Processos")
        
        # Aaba sobre o funcionamento de Realocação
        Realocar = Frame(nb)
        label_info4 = Label(Realocar, text="Funcionamento do Botão Realocar.")
        label_info4.pack(padx=10, pady=10)
        mensageRealocar = Label(Realocar, text="Com espaços vazios entre os processos que podem ser reutilizados para alocar outros processos, a \ncada clique será realocado o primeiro bloco de processo que tenha espaço vazio antes de seu início. ")
        mensageRealocar.pack()
        nb.add(Realocar, text="Realocar")

# Cria a tela principal chamada raiz e aciona o Tkinter        
raiz = tk.Tk()

# Definição do tamanho e posição da janela centralizado conforme a tela do usuário ao fazer SysCall para o Windows
largura_menu = 800
altura_menu = 600
raiz.resizable(0, 0)
raiz.title('Gerenciador de Memória')
largura_tela = raiz.winfo_screenwidth()
altura_tela = raiz.winfo_screenheight()
x = (largura_tela/2) - (largura_menu/2)
y = (altura_tela/2) - (altura_menu/2)
raiz.geometry('%dx%d+%d+%d' % (largura_menu, altura_menu, x, y))

# gm irá chamar os métodos do objeto GerenciadorMemória
gm = GerenciadorMemoria(raiz)

# Cria um quadro de botões abaixo da grade de posições
quadro_botao = tk.Frame(raiz)
quadro_botao.pack(side="top", fill="x", pady=20)

# Botão que aciona a função de Alocar
botao_alocar = tk.Button(quadro_botao, text="Alocar", command=gm.alocar, height=5, width=21, bg='gray', borderwidth=0)
botao_alocar.pack(side="left", padx=5)

# Botão que aciona a função de Desalocar
botao_desalocar = tk.Button(quadro_botao, text="Desalocar", command=gm.desalocar, height=5, width=21, bg='gray', borderwidth=0)
botao_desalocar.pack(side="left", padx=5)

# Botão que aciona a função de Limpar Processos
botao_limpar_processos = tk.Button(quadro_botao, text="Limpar Processos", command=gm.limpar_processos, height= 5, width=21, bg='gray', borderwidth=0)
botao_limpar_processos.pack(side='left', padx=5)

# Botão que aciona a função de Realocar
botao_realocar = tk.Button(quadro_botao, text="Realocar", command=gm.realocar, height=5, width=21, bg='gray', borderwidth=0)
botao_realocar.pack(side="left", padx=5)

# Botão que aciona a função de Ajuda
botao_ajuda = tk.Button(quadro_botao,text="Ajuda",command=gm.ajuda, height=5, width=21,bg='gray',borderwidth=0)
botao_ajuda.pack(side="left", padx=5)
raiz.mainloop()