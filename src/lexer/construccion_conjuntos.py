from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import Tk
import re

# Algoritmo Construccion De Conjuntos

class ConstruccionConjuntos:
    def __init__(self):
        # Variables 
        self.alfabeto = []
        self.TablaThompson = []
        self.TablaFinal = []
        self.contadorEstados = 0

        # Creacion de la ventana
        self.root = Toplevel()
        self.root.geometry("800x700+600+150")
        self.root.title("Construccion De Conjuntos")
        # self.root.iconbitmap("icon.ico")
        self.root.config(bg="#E7E7B0")

        # Creacion del boton
        self.frame = Frame(self.root, background="#FFFFDD", relief=SUNKEN, padx=20, pady=20)
        self.frame.pack(padx=20, pady=20)

        boton_abrir = Button(self.frame, text="Abrir Archivo", background="#C0EFD2", command=self.abrir_archivo)
        boton_abrir.grid(row=0, column=0, padx=10)

        boton_limpiar = Button(self.frame, text="Limpiar", background="#C0EFD2", command=self.limpiar)
        boton_limpiar.grid(row=0, column=1, padx=10, pady=10)

        self.table = ttk.Treeview(self.root)

    def abrir_archivo(self):
        file = filedialog.askopenfilename(filetype=[("Archivos de texto", "*.txt")])
        
        if file:
            # Lee el archivo y lo separa por lineas
            with open(file, "r") as archivo:
                contenido = archivo.read()
            lineas = contenido.splitlines()

            # Creando lista de alfabeto de entrada
            self.alfabeto = lineas[0].split(", ")

            # Lectura de la tabla de los estados
            i = len(lineas) - 1
            j = 1
            while (j <= i):
                self.TablaThompson.append(lineas[j].split(", "))
                j += 1
                
                # Detecta multiples estados destino y crea sublistas de enteros
            for i in range(len(self.TablaThompson)):
                for j in range(len(self.TablaThompson[i])):
                    if re.findall(r"\[", self.TablaThompson[i][j]):
                        self.TablaThompson[i][j] = re.sub(r"\[", "", self.TablaThompson[i][j])
                    if re.findall(r"\]", self.TablaThompson[i][j]):
                        self.TablaThompson[i][j] = re.sub(r"\]", "", self.TablaThompson[i][j])
                    if re.findall(r",", self.TablaThompson[i][j]):
                        elementos = self.TablaThompson[i][j].split(",")
                        self.TablaThompson[i][j] = [int(elemento) for elemento in elementos]

            # Conversion de datos restantes a int o None
            for i in range(len(self.TablaThompson)):
                for j in range(len(self.TablaThompson[i])):
                    if type(self.TablaThompson[i][j]) is str:
                        if self.TablaThompson[i][j].isnumeric():
                            self.TablaThompson[i][j] = int(self.TablaThompson[i][j])
                        elif self.TablaThompson[i][j] == "None":
                            self.TablaThompson[i][j] = None

            self.construir()
            self.reiniciar()
        else:
            messagebox.showerror("Error", "No se selecciono ningun archivo")

    # Algoritmo de construccion de conjuntos
    def construir(self):
        EstadoInicial = self.cerraduraEpsilon(0)
        Inicio=0
        Fin=len(self.TablaThompson) - 1
        self.nuevoEstado(self.contadorEstados, EstadoInicial)
        self.contadorEstados += 1

        for estadosN in self.TablaFinal:
            for s in range(len(self.alfabeto)):
                estadoAux=set()
                movs=self.move(estadosN[0], s)
                for e in movs:
                    estadoAux.update(self.cerraduraEpsilon(e))
                if len(estadoAux) > 0:
                    yaEsta=0
                    indice=0
                    for verSiYaEsta in self.TablaFinal:
                        if verSiYaEsta[0] == estadoAux:
                            yaEsta=1
                            ubicacionEstado=indice
                        indice += 1
                    if yaEsta == 0:
                        self.nuevoEstado(self.contadorEstados, estadoAux)
                        estadosN[s+1]=self.contadorEstados
                        self.contadorEstados += 1
                    else:
                        estadosN[s+1]=ubicacionEstado
        
        self.contadorEstados = 0
        # Mostrar la tabla de conjuntos
        self.generarTabla(Fin)
        self.reiniciar()

    def cerraduraEpsilon(self, estado): #Solo evalua 1 estado, no un conjunto
        conjunto=set() #Conjunto vacio
        conjunto.add(estado) #Añade el estado a evaluar
        pila=[] #Inicializa la pila
        if self.TablaThompson[estado][len(self.alfabeto)] != None: #Pregunta si hay transiciones epsilon
            if isinstance(self.TablaThompson[estado][len(self.alfabeto)], list): #Pregunta si hay un arreglo
                pila.append(self.TablaThompson[estado][len(self.alfabeto)][0]) #Añade el primer elemento del arreglo a la pila 
                conjunto.add(self.TablaThompson[estado][len(self.alfabeto)][0]) #Añade el primer elemento del arreglo al conjunto
                conjunto.add(self.TablaThompson[estado][len(self.alfabeto)][1]) #Añade el segundo elemento del arreglo a la pila 
                pila.append(self.TablaThompson[estado][len(self.alfabeto)][1]) #Añade el segundo elemento del arreglo al conjunto
            else: #Se ejecuta si solo hay un elemento en la transicion epsilon
                pila.append(self.TablaThompson[estado][len(self.alfabeto)]) #Añade el elemento a la pila
                conjunto.add(self.TablaThompson[estado][len(self.alfabeto)]) #Añade el elemento al conjunto
            while(pila): #Mientras haya elementos en la pila
                temp=pila.pop() #Saca un elemento de la pila
                conjuntoAux=self.cerraduraEpsilon(temp) #Obtenemos la cerradura-epsilon de temp (llamada recursiva)
                conjunto.update(conjuntoAux) #Unimos el conjunto aux obtenido con el conjunto principal 
                for elemento in conjuntoAux: #Si hay un elemento diferente a temp en el conjunto aux, se añade a la pila
                    if elemento != temp:
                        pila.append(elemento)
        return conjunto #Retorna el conjunto

    def move(self, conjuntoNuevo, simbolo):
        movimientos=set()
        for elemento in conjuntoNuevo:
            if self.TablaThompson[elemento][simbolo] != None:
                movimientos.add(self.TablaThompson[elemento][simbolo])
        return movimientos

    def nuevoEstado(self, contador, conjunto):
        self.TablaFinal.append([])
        self.TablaFinal[contador].append(conjunto)
        for k in range(len(self.alfabeto)):
            self.TablaFinal[contador].append(None)

    def generarTabla(self, Fin):
        # Asegura que las tablas no se amontonen
        self.limpiar()
        self.table = ttk.Treeview(self.root, columns=("Estado",)+tuple(range(len(self.alfabeto))), show="headings")

        # Estilo para la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
        style.map('Treeview', background=[('selected', '#E9D6AF')])
        style.map('Treeview', foreground=[('selected', 'black')])

        self.table.heading("Estado", text="Estado")
        self.table.column("Estado", width=100, anchor="center")

        # Escribir cabeceras
        for i in range(len(self.alfabeto)):
            self.table.heading(i, text=self.alfabeto[i])
            self.table.column(i, width=100, anchor="center")
            
        # Escribir filas
        datos = []
        for i in range(len(self.TablaFinal)):
            if i == 0:
                datos.append(chr(i+65) + " i")
            elif Fin in self.TablaFinal[i][0]:
                datos.append(chr(i+65) + " f")
            else:
                datos.append(chr(i+65))
            for j in range(len(self.alfabeto)):
                if self.TablaFinal[i][j+1] != None:
                    datos.append(chr(65+self.TablaFinal[i][j+1]))
                else:
                    datos.append("-")
            self.table.insert("", "end", values=datos)
            datos = []

        self.table.pack(padx=20, pady=20)

    # Metodos de limpieza backend y frontend
    def reiniciar(self):
        self.alfabeto = []
        self.TablaThompson = []
        self.TablaFinal = []
        self.contadorEstados = 0

    def limpiar(self):
        self.table.destroy()
        self.table = ttk.Treeview(self.root)