from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import re
import math

class TrieNode:
    def __init__(self, value=None):
        self.value = value
        self.children = {}

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert_rule(self, rule):
        node = self.root
        for symbol in rule:
            if symbol not in node.children:
                node.children[symbol] = TrieNode(symbol)
            node = node.children[symbol]

def print_tree(node, depth=0):
    if node.value is not None:
        print("  " * depth+ node.value)
    for child in node.children.values():
        print_tree(child, depth + 1)

class CalculoPrimerosSiguientes:
    def __init__(self):
        # Variables app
        self.file_path = ""
        self.isAnalyzed = False

        # Variables Primeros Siguientes
        self.NT = []
        self.TE = []
        self.reglas = []
        self.SimboloInicial = ""
        self.Primeros = []
        self.result = ""

        # Creacion ventana
        self.root = Tk()
        self.root.geometry("800x700+400+60")
        self.root.title("Calculo de Primero y Siguientes")
        self.root.config(bg="#E7E7B0")
        self.root.resizable(False, False)

        # Componentes interfaz
        self.frame = Frame(self.root, background="#FFFFDD", relief=SUNKEN, padx=20, pady=20)
        self.frame.pack(padx=20, pady=20)

        self.open_label = Label(self.frame, text="Seleccionar una gramatica:")
        self.open_label.grid(row=0, column=0, padx=10, pady=10)

        open_button = Button(self.frame, text="Abrir Archivo", background="#C0EFD2", command=self.open_file)
        open_button.grid(row=0, column=1, padx=10, pady=10)

        self.grammar_label = Label(self.frame, text="Gramatica seleccionda: ")
        self.grammar_label.grid(row=1, column=0, padx=10, pady=10)

        self.grammar_entry = Entry(self.frame, width=30)
        self.grammar_entry.grid(row=1, column=1, padx=10, pady=10)
        self.grammar_entry.insert(0, "")
        self.grammar_entry.config(state="readonly")

        self.analyze_button = Button(self.frame, text="Analizar", background="#C0EFD2", command=self.analyze)
        self.analyze_button.grid(row=2, column=0, padx=10, pady=10)

        clear_button = Button(self.frame, text="Limpiar", background="#C0EFD2", command=self.clear)
        clear_button.grid(row=2, column=1, padx=10, pady=10)

        self.frame_show = Frame(self.root, background="#FFFFDD", relief=SUNKEN, padx=20, pady=20)
        self.frame_show.pack(padx=20, pady=self.frame.winfo_reqheight() + 20)

        self.grammar_entry_show = Text(self.frame_show, width=80, height=80, wrap="word")
        self.grammar_entry_show.grid(row=1, column=1, padx=10, pady=10)
        self.grammar_entry_show.insert("1.0", "")
        self.grammar_entry_show.config(state="disabled")

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetype=[("Archivos de texto", "*.txt")])

        if len(self.file_path) > 0:
            self.grammar_entry.config(state="normal")
            self.grammar_entry.insert(0, self.file_path)
            self.grammar_entry.config(state="readonly")
            # File treatment
            with open(self.file_path, 'r') as file:
                content = file.read()
            lines = content.splitlines()
            # Assignment
            self.TE = lines[0].split(" ")
            self.NT = lines[1].split(" ")

            for i in range(2, len(lines)):
                # Need to consider when there is a case like E->ET|@
                lines[i] = lines[i].replace(" ", "")
                lines[i] = lines[i].replace("->", "")
                self.reglas.append(lines[i])
                if(self.reglas[-1].find("|")):
                    aux = self.reglas[-1].split("|")
                    self.reglas[-1] = aux[0]
                    for j in range(1, len(aux)):
                        self.reglas.append(self.reglas[-1][0]+aux[j])
            
            # print(self.NT)
            # print(self.TE)
            # print(self.reglas)
            messagebox.showinfo("Calculo de Primeros y Siguientes", "Archivo seleccionado correctamente")
        else:
            messagebox.showerror("Calculo de Primeros y Siguientes", "No ha seleccionado un archivo!")

    def clear_text(self):
        # Variables
        self.file_path = ""
        # Componentes
        self.grammar_entry.config(state="normal")
        self.grammar_entry.delete(0, END)
        self.grammar_entry.config(state="readonly")

        self.grammar_entry_show.config(state="normal")
        self.grammar_entry_show.delete("1.0", END)
        self.grammar_entry_show.config(state="disabled")

    # Reinicia para ejecuciones mas de 1 
    def restart(self):
        self.NT = []
        self.TE = []
        self.reglas = []
        self.SimboloInicial = ""
        self.Primeros = []
        self.result = ""

        self.isAnalyzed = False
    
    def clear(self):
        self.restart()
        self.clear_text()

    def analyze(self):
        if self.isAnalyzed == False and len(self.file_path) > 0:

            # Calcula primeros y siguientes
            self.calculate()

            # Write on the text area
            self.grammar_entry_show.config(state="normal")
            self.grammar_entry_show.insert("1.0", self.result)
            self.grammar_entry_show.config(state="disabled")

            self.isAnalyzed = True
        else:
            messagebox.showwarning("Calculo de Primeros y Siguientes", "Seleccione un archivo!")
    
    def PrimerosYsiguientes(self, TEaux,NTaux,Reglasaux):           
        # Crear un árbol Trie basado en las reglas dadas
        trie = Trie()
        self.TE=TEaux
        self.NT=NTaux
        self.reglas=Reglasaux
        cadena=[]
        Siguientes=[]   #arreglo que contendra los siguientes de los simbolos no terminales
        self.SimboloInicial=self.NT[0]    #se guarda el simbolo inicial de la gramatica
        self.reducirS(self.TE,self.reglas,cadena)
        for rule in self.reglas:
            trie.insert_rule(rule)
        K=[]
        S=[]
        PrimeroD={}
        value=""
        contador=0
        self.buscarP(trie.root,K,PrimeroD,value)
        for r in range(len(K)):
            if  'A' <= K[r][2] <= 'Z':
                contador=contador+1
        PrimeroDAx={} 
        for i in K:
            PrimeroDAx[i[0]]=""
        for f in K:
            PrimeroD[f[0]]= PrimeroDAx[f[0]]+" "+f[2]
            PrimeroDAx[f[0]]=  PrimeroD[f[0]] 
        PrimeroD=PrimeroDAx       
        contador2=0
        k=0
        k1=contador
        while k <k1:
            contador2=0
            for r in range(len(K)):
                if  'A' <= K[r][2] <= 'Z':
                    contador2=contador2+1    
                if  'A' <= K[r][2] <= 'Z' and contador2==contador:
                    PrimeroD[K[r][0]]=PrimeroD[K[r][2]]
                    contador=contador-1
            k=k+1   
        cadena2="" 
        for k in self.NT:
            for i in range(math.floor(len(cadena)/2)):
                cadena2=PrimeroD[k]
                cadena2=self.replace_word(cadena2,cadena[i*2+1], cadena[i*2])
                PrimeroD[k]=cadena2
        self.Primeros=[]
        value=""
        for i in self.NT:
            value=PrimeroD[i]
            self.Primeros.append(value.split())
        NTAux=self.NT
        TEaux=self.TE
        auxPrimeros=self.Primeros
        for i in range(math.floor(len(cadena)/2)):
            for k in range(len(self.TE)):
                self.TE[k]=self.TE[k].replace(cadena[i*2],cadena[i*2+1])

        for i in range(math.floor(len(cadena)/2)):
            for k in range(len(self.Primeros)):
                for j in range(len(self.Primeros[k])):
                    self.Primeros[k][j]=self.replace_word(self.Primeros[k][j],cadena[i*2+1], cadena[i*2])
        Siguientes=[]   #arreglo que contendra los siguientes de los simbolos no terminales
        SimboloInicial=self.NT[0]    #se guarda el simbolo inicial de la gramatica

        for SimboloNoTerminal in self.NT:
            Siguientes.append(self.siguiente(SimboloNoTerminal))
        for i in range(math.floor(len(cadena)/2)):
            for k in range(len(self.TE)):
                #TE[k]=TE[k].replace(cadena[i*2+1],cadena[i*2])
                self.TE[k]=self.replace_word(self.TE[k],cadena[i*2+1], cadena[i*2])
        for i in range(math.floor(len(cadena)/2)):
            for k in range(len(Siguientes)):
                for j in range(len(Siguientes[k])):
                    Siguientes[k][j]=self.replace_word(Siguientes[k][j],cadena[i*2+1], cadena[i*2])

        return {'S':Siguientes,'P':self.Primeros}
    
    def siguiente(self, A):
        sig = []
        if A == self.SimboloInicial: #Si A es el simbolo inicial, agrega "$" a los siguientes de A
            sig.append("$")
        
        for regla in self.reglas:    #analiza las reglas en busca del simbolo A
            B = regla[0]    #B tiene el simbolo no terminal que inicia la regla. en "F -> TE", F seria el simbolo B
            Beta=[]  #arreglo que va a contener los simbolos de Beta
            for i in range(len(regla)):    #indice que recorre la regla
                if i == 0:  #condicion que impide que se analice el simbolo que inicia la regla
                    continue
                if regla[i] == A:   #se ejecuta si detecta el simbolo A en la regla
                    j = i + 1   #indice que recorre los simbolos que estan después de A, es decir, los simbolos que tendrá Beta
                    if j < len(regla) and regla[j]:    #se ejecuta si existen simbolos que agregar a Beta (B -> alfa A beta)
                        while j < len(regla) and regla[j]:
                            Beta.append(regla[j])
                            j += 1
                        if Beta:
                            primerosBeta=self.obtenerPrimeros(Beta)
                            for k in primerosBeta:
                                if k != "@":
                                    sig.append(k)
                            if "@" in primerosBeta and B != A:  #se ejecuta si en los primeros de beta hay @, y B no es el simbolo A
                                sig = self.agregarSiguientesB(B, sig)
                    elif B != A:    #se ejecuta si la transicion es del tipo B -> alfa A y B no es el simbolo A
                        sig = self.agregarSiguientesB(B, sig)
        return sig  #retorna una arreglo con los siguientes de A
    
    def obtenerPrimeros(self, arregloBeta):
        primerosB = []
        for cadena in arregloBeta:
            if cadena in self.TE:
                primerosB.append(cadena)
                return primerosB
            primerosAux = self.Primeros[self.NT.index(cadena)]
            for cadena2 in primerosAux:
                primerosB.append(cadena2)
        return primerosB
    
    def agregarSiguientesB(self, B, sigArreglo):
        siguientesB = self.siguiente(B)  #obtiene los siguientes de B
        conjuntoSig = set(siguientesB)
        siguientesPrincipal = set(sigArreglo)
        siguientesPrincipal.update(conjuntoSig)
        siguienteActualizado = list(siguientesPrincipal)
        return siguienteActualizado

    def reducirS(self, TE,Reglas,cadena):
        i=0
        k=0
        ind=0
        letra=97
        for s in TE:
            if len(str(TE[i]))!=1:
                cadena.append(TE[i])
                cadena.append(chr(letra))
                letra=letra+1
                ind=0
                for r in range (len(Reglas)):
                    Reglas[r]=Reglas[r].replace(cadena[k*2],cadena[k*2+1])
                    ind=ind+1
                k=k+1       
            i=i+1

    #Simbolos terminales y no terminales
    def replace_word(text, old_word, new_word):
        pattern = re.compile(r'\b' + re.escape(old_word) + r'\b')
        return pattern.sub(new_word, text)

    def buscarP(self, node,K=None,PrimeroD=None,value="",depth=0):
        for child in node.children.values():
            if(child.value!=node.value and 'A' <= str(node.value) <= 'Z' and depth!=2):
                self.buscarP(child,K,PrimeroD,value,depth+1)
                if(node.value!=None ):
                    K.append(str(node.value)+"="+str(child.value))
                    PrimeroD[node.value]=value+" "+child.value
                    value=child.value