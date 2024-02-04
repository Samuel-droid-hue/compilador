import tkinter as tk
import src.lexer.construccion_conjuntos as cc
import src.parser.coleccion_canonica as ccan
import src.parser.primeros_siguientes as ps
import src.parser.tabla_analisis as tas
import src.lexer.analizador_lexico as a

class MiCompilador():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mi Compilador")
        self.root.geometry("600x400")
        self.root.resizable(0,0)
        self.root.config(bg="#EFEFEF")
        self.execution = None
        self.init_components()

    def init_components(self):
        self.root.main_menu = tk.Menu(self.root)
        # Menu creation
        self.root.lexical_menu = tk.Menu(self.root.main_menu, tearoff=0)
        self.root.syntax_menu = tk.Menu(self.root.main_menu, tearoff=0)
        self.root.semantic_menu = tk.Menu(self.root.main_menu, tearoff=0)
        # Menu Analizador Lexico
        self.root.lexical_menu.add_command(label="Algoritmo Construccion de Conjuntos", command=self.construccion_conjuntos)
        self.root.lexical_menu.add_command(label="Analizador Lexico", command=self.analizador_lexico)
        self.root.main_menu.add_cascade(label="Analizador Lexico", menu=self.root.lexical_menu)
        # Menu Analizador Sintactico
        self.root.syntax_menu.add_command(label="Algoritmo Primeros y Siguientes", command=self.primeros_siguientes)
        self.root.syntax_menu.add_command(label="Algoritmo Coleccion Canonica", command=self.coleccion_canonica)
        self.root.syntax_menu.add_command(label="Construccion Tabla Analisis Sintactico", command=self.construccion_tabla_analisis_sintactico)
        self.root.syntax_menu.add_command(label="Analizador Sintactico LR", command=self.analizador_sintactico_lr)
        self.root.main_menu.add_cascade(label="Analizador Sintactico", menu=self.root.syntax_menu)
        # Menu Analizador Semantico
        self.root.semantic_menu.add_command(label="Analizador Semantico LR", command=self.analizador_semantico_lr)
        self.root.main_menu.add_cascade(label="Analizador Semantico", menu=self.root.semantic_menu)
        self.root.config(menu=self.root.main_menu)

    def construccion_conjuntos(self):
        self.execution = cc.ConstruccionConjuntos()
        self.execution.root.mainloop()

    def analizador_lexico(self):
        self.execution = a.Application()
        self.execution.root.mainloop()
    
    def primeros_siguientes(self):
        self.execution = ps.CalculoPrimerosSiguientes()
        self.execution.root.mainloop()

    def coleccion_canonica(self):
        self.execution = ccan.ColeccionCanonica()
        self.execution.root.mainloop()

    def construccion_tabla_analisis_sintactico(self):
        self.execution = tas.TablaTAS()
        self.execution.root.mainloop()

    def analizador_sintactico_lr(self):
        print("AnalizadorSintacticoLR")

    def analizador_semantico_lr(self):
        print("AnalizadorSemanticoLR")

if __name__ == "__main__":
    app = MiCompilador()
    app.root.mainloop()