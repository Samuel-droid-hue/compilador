from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Scrollbar

# Get data structure to augmented grammar to AnalizadorSintactico LR
def get_ASgrammar(path):
    with open(path, "r") as file:
        content = file.readlines()
    
    grammar = []
    content = content[2:]

    for line in content:
        grammar.append(line.strip().split(" -> "))

    return grammar


def get_TAgrammar(path):
    with open(path, "r") as file:
        content = file.readlines()

    NT = content[0].split()
    TE = content[1].split()

    grammar = []
    content = content[3:]

    for line in content:
        grammar.append(line.strip().replace(" -> ", " "))

    return NT, TE, grammar

def get_allDataTokens(path):
    with open(path, "r") as file:
        content = file.readlines()
    
    for i in range(len(content)):
        content[i] = content[i].strip()

    return content


class AnalizadorSintactico():
    def __init__(self):
        self.isAnalyzed = False
        
        # Variables
        self.analysis = []
        self.program = []
        self.tokens = []
        self.result = []
        
        #ventana
        self.root = Tk()
        self.root.geometry("900x700+400+50")
        self.root.title("TAS")
        self.root.config(bg="#34495E")
        self.root.resizable(False, False)

        # Componentes interfaz
        self.frame = Frame(self.root, background="#99A3A4", relief=SUNKEN, padx=20, pady=20)
        self.frame.pack(padx=10, pady=10)


        open_button = Button(self.frame, text="Abrir Gramatica", background="#C0EFD2", command=lambda:self.open_file(self.grammar_entry))
        open_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.grammar_entry = Entry(self.frame, width=30)
        self.grammar_entry.grid(row=0, column=1, padx=10, pady=10)
        self.grammar_entry.insert(0, "")
        self.grammar_entry.config(state="readonly")

        open_button_tokens = Button(self.frame, text="Abrir Tokens", background="#C0EFD2", command=lambda:self.open_file(self.tokens_entry))
        open_button_tokens.grid(row=1, column=0, padx=10, pady=10)
        
        self.tokens_entry = Entry(self.frame, width=30)
        self.tokens_entry.grid(row=1, column=1, padx=10, pady=10)
        self.tokens_entry.insert(0, "")
        self.tokens_entry.config(state="readonly")
        
        
        self.analyze_button = Button(self.frame, text="Analizar", background="#C0EFD2", command=self.analyze)
        self.analyze_button.grid(row=2, column=0, padx=20, pady=20)
        
        clear_button = Button(self.frame, text="LimpiarTodo", background="#C0EFD2", command=self.clear)
        clear_button.grid(row=2, column=1, padx=20, pady=20)


        self.frame_show = Frame(self.root, background="#99A3A4", relief=FLAT, padx=20, pady=20)
        self.frame_show.pack(padx=20, pady=self.frame.winfo_reqheight()+1)

        
        self.canvas = Canvas(self.frame_show,width=600, height=350)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

        self.table_frame = Frame(self.canvas, bg="#CACFD2")
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        self.scrollbar_vertical = Scrollbar(self.frame_show, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar_vertical.pack(side=RIGHT, fill=Y)
        
        self.scrollbar_horizontal = Scrollbar(self.frame_show, orient=HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_horizontal.pack(side=BOTTOM, fill="x")
    
    def open_file(self, entry_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])

        if len(file_path) > 0:
            entry_widget.config(state="normal")
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)
            entry_widget.config(state="readonly")
            messagebox.showinfo("Analizador Sintactico", "Archivo seleccionado correctamente")
        else:
            messagebox.showerror("Analizador Sintactico", "No se ha seleccionado un archivo!")

    def clear_gram(self):
    # Destruir y reconstruir el marco para la tabla
        if hasattr(self, 'table_frame'):
            self.table_frame.destroy()  # Destruir el marco existente

        self.table_frame = Frame(self.canvas, bg="#CACFD2")  # Crear un nuevo marco
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

    
    def clear(self):
        self.file_path = ""
        self.grammar_entry.config(state="normal")
        self.grammar_entry.delete(0, END)
        self.grammar_entry.config(state="readonly")
        
        self.tokens_entry.config(state="normal")
        self.tokens_entry.delete(0, END)
        self.tokens_entry.config(state="readonly")
        
        # Variables
        self.analysis = []
        self.program = []
        self.tokens = []
        self.result = []
        
        
        # Reiniciar variables de estado
        self.isAnalyzed = False

        # Limpiar la tabla y la interfaz
        self.clear_gram()
    def analyze(self):
        if not self.isAnalyzed:
            self.analizarLR()
    
    def analizarLR(self):
        grammar_path = self.grammar_entry.get()
        tokens_path = self.tokens_entry.get()
        font_style = ("Arial", 10, "bold")
        
        if grammar_path and tokens_path:
            analysis, program, tokens = self.to_analyze(grammar_path, tokens_path)

            label = Label(self.table_frame,text=f"Programa : {program}",borderwidth=2,relief="solid",background="#16C4DF")
            label.grid(row=0, column=0, padx=2, pady=2)
            
            label = Label(self.table_frame,text=f"Tokens : {tokens}",borderwidth=2,relief="solid",background="#16C4DF")
            label.grid(row=1, column=0, padx=2, pady=2)

            label = Label(self.table_frame,text=" Pila ",borderwidth=1,width=35,relief="solid",background="#A43371", foreground="black", font=font_style)
            label.grid(row=2, column=0, padx=2, pady=2)
            label = Label(self.table_frame,text=" Entrada ",borderwidth=1,width=35,relief="solid",background="#A43371",  foreground="black", font=font_style)
            label.grid(row=2, column=1, padx=2, pady=2)
            label = Label(self.table_frame,text=" Accion ",borderwidth=1,width=35,relief="solid",background="#A43371", foreground="black", font=font_style)
            label.grid(row=2, column=2, padx=2, pady=2)
            
            self.result = ""
                
            for i in range(len(analysis)):
                for j in range(len(analysis[i])):
                    self.result+=f"{analysis[i][j]}|"
                self.result+=('\n\n|')
            print(self.result)
            
            header_columns = self.result.strip().split('|') 
            
            current_row = 4  # Comenzar desde la segunda fila
            current_col = 0 
        
            for j,header_text in enumerate(header_columns):
                if "\n\n" not in header_text:
                    rango = len(header_columns)
                    if j<rango-1:
                        label = Label(
                        self.table_frame,
                        text=header_text,
                        borderwidth=1,
                        width=35,
                        relief="solid",
                        background="#16DFAE",  # Color de fondo
                        foreground="black",       # Color de primer plano
                        font=font_style
                        )
                        label.grid(row=current_row, column=current_col, padx=2, pady=2)
                        current_col +=1
                else:
                    current_row +=1
                    current_col=0

    # Get data structure to token strip
    def get_tokens(self, path):
        with open(path, "r") as file:
            content = file.readlines()

        # ONLY CONSIDER A SINGLE LINE OF FILE!
        tokens = []
        tokens = content[1].strip().split()

        return tokens

    # Get one positiion on the table
    # ------------------------------
    # WARNING!: TOO MUCH PARAMAETERS
    # ------------------------------
    # s: State number
    # a: Symbol
    def get_action(self, TA, NT, TE, s, a):
        # Get i index
        i = int(s)
        # Get j index
        if a in TE:
            j = TE.index(a)
        else:
            j = len(TE) + NT.index(a)
        
        return TA[i][j]

    def find_error(self, row, TE):
        indexs = []
        symbols = []
        n = len(TE)-1

        for i in range(0, n):
            if row[i] != '  ':
                indexs.append(i)

        for j in indexs:
            symbols.append(TE[j])
        
        return symbols

    # Get format to rows
    def get_rowda(self, stack, input, action):
        column1 = ' '.join(map(str, stack))
        column2 = ' '.join(input)

        return [column1,  column2, action]

    def get_rowr(self, stack, input, action, production):
        column1 = ' '.join(map(str, stack))
        column2 = ' '.join(input)
        column3 = '->'.join(production)
        column3 = action + ' ' + column3

        return [column1, column2, column3]

    def get_rowe(self, stack, input, symbols):
        column1 = ' '.join(map(str, stack))
        column2 = ' '.join(input)
        column3 = 'Error se esperaba ' + ' o '.join(symbols)

        return [column1, column2, column3]

    # ------------- ANALYZER ------------- #
    def to_analyze(self, grammar_path, tokens_path):
        # Variables
        augmentedGrammar = get_ASgrammar(grammar_path)
        stack = []
        input = []
        accept = False
        error = False
        production = []
        analysis = []

        # Get the table and more values
        NT, TE, TA = self.to_create(grammar_path)
        TE.append('$')
        input = self.get_tokens(tokens_path)
        input.append('$')
        
        # Algorithm
        stack.append(0)

        while not (accept or error):
            case_action = self.get_action(TA, NT, TE, stack[-1], input[0])
            if case_action[0] in {'d', 'r'}:
                # Calculates index of dn or rn
                index = case_action[1:]
                index = int(index)
                if case_action[0] == 'd':
                    # print(stack, "\t\t", input, "\t\t", case_action)
                    analysis.append(self.get_rowda(stack, input, case_action))
                    stack.append(input[0])
                    stack.append(index)
                    input.pop(0)
                elif case_action[0] == 'r':
                    production = augmentedGrammar[index]
                    # print(stack, "\t\t", input, "\t\t", case_action, " ", production)
                    analysis.append(self.get_rowr(stack, input, case_action, production))
                    if production[-1] != '@':
                        for j in range(0, 2*(production[-1].count(' ')+1)):
                            stack.pop()
                    j = stack[-1]
                    stack.append(production[0])
                    ir_a = self.get_action(TA, NT, TE, j, production[0])
                    stack.append(ir_a)
            else:
                if case_action == 'AC':
                    # print(stack, "\t\t", input, "\t\t", case_action)
                    analysis.append(self.get_rowda(stack, input, case_action))
                    accept = True
                else:
                    symbols = self.find_error(TA[stack[-1]], TE)
                    # print(stack, "\t\t", input, "\t\tError se esperaba: ", symbols)
                    analysis.append(self.get_rowe(stack, input, symbols))
                    error = True
        
        # Get data to interface
        data_token = get_allDataTokens(tokens_path)

        return analysis, data_token[0], data_token[1]
    
    # Get data structure to token strip
    def get_tokens(self, path):
        with open(path, "r") as file:
            content = file.readlines()

        # ONLY CONSIDER A SINGLE LINE OF FILE!
        tokens = []
        tokens = content[1].strip().split()

        return tokens
    
    # Get one positiion on the table
    # ------------------------------
    # WARNING!: TOO MUCH PARAMAETERS
    # ------------------------------
    # s: State number
    # a: Symbol
    def get_action(self, TA, NT, TE, s, a):
        # Get i index
        i = int(s)
        # Get j index
        if a in TE:
            j = TE.index(a)
        else:
            j = len(TE) + NT.index(a)
        
        return TA[i][j]

    def find_error(self, row, TE):
        indexs = []
        symbols = []
        n = len(TE)-1

        for i in range(0, n):
            if row[i] != '  ':
                indexs.append(i)

        for j in indexs:
            symbols.append(TE[j])
        
        return symbols

    # Get format to rows
    def get_rowda(self, stack, input, action):
        column1 = ' '.join(map(str, stack))
        column2 = ' '.join(input)

        return [column1,  column2, action]

    def get_rowr(self, stack, input, action, production):
        column1 = ' '.join(map(str, stack))
        column2 = ' '.join(input)
        column3 = '->'.join(production)
        column3 = action + ' ' + column3

        return [column1, column2, column3]

    def get_rowe(self, stack, input, symbols):
        column1 = ' '.join(map(str, stack))
        column2 = ' '.join(input)
        column3 = 'Error se esperaba ' + ' o '.join(symbols)

        return [column1, column2, column3]

    # ------------- ANALYZER ------------- #
    def to_analyze(self, grammar_path, tokens_path):
        # Variables
        augmentedGrammar = get_ASgrammar(grammar_path)
        stack = []
        input = []
        accept = False
        error = False
        production = []
        analysis = []

        # Get the table and more values
        NT, TE, TA = self.to_create(grammar_path)
        TE.append('$')
        input = self.get_tokens(tokens_path)
        input.append('$')
        
        # Algorithm
        stack.append(0)

        while not (accept or error):
            case_action = self.get_action(TA, NT, TE, stack[-1], input[0])
            if case_action[0] in {'d', 'r'}:
                # Calculates index of dn or rn
                index = case_action[1:]
                index = int(index)
                if case_action[0] == 'd':
                    # print(stack, "\t\t", input, "\t\t", case_action)
                    analysis.append(self.get_rowda(stack, input, case_action))
                    stack.append(input[0])
                    stack.append(index)
                    input.pop(0)
                elif case_action[0] == 'r':
                    production = augmentedGrammar[index]
                    # print(stack, "\t\t", input, "\t\t", case_action, " ", production)
                    analysis.append(self.get_rowr(stack, input, case_action, production))
                    if production[-1] != '@':
                        for j in range(0, 2*(production[-1].count(' ')+1)):
                            stack.pop()
                    j = stack[-1]
                    stack.append(production[0])
                    ir_a = self.get_action(TA, NT, TE, j, production[0])
                    stack.append(ir_a)
            else:
                if case_action == 'AC':
                    # print(stack, "\t\t", input, "\t\t", case_action)
                    analysis.append(self.get_rowda(stack, input, case_action))
                    accept = True
                else:
                    symbols = self.find_error(TA[stack[-1]], TE)
                    # print(stack, "\t\t", input, "\t\tError se esperaba: ", symbols)
                    analysis.append(self.get_rowe(stack, input, symbols))
                    error = True
        
        # Get data to interface
        data_token = get_allDataTokens(tokens_path)

        return analysis, data_token[0], data_token[1]