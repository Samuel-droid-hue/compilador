from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Scrollbar
import src.parser.coleccion_canonica as ccan
import src.parser.primeros_siguientes as ps

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

class TablaTAS():
    def __init__(self):
        self.isAnalyzed = False
        self.isGrama = False

        # Variables
        self.NT = []
        self.TE = []
        self.Reglas = []
        self.Reglas2 = []
        self.result2 = []
        self.result = []
        self.tablaAS=[]
        self.siguientes = []
        self.ir_a_NT=[]
        self.ir_a_TE=[] 
        self.states=[] 
        self.PYS=[]
        
        #ventana
        self.root = Tk()
        self.root.geometry("800x700+400+60")
        self.root.title("TAS")
        self.root.config(bg="#847474")
        self.root.resizable(False, False)

        # Componentes interfaz
        self.frame = Frame(self.root, background="#99A3A4", relief=SUNKEN, padx=20, pady=20)
        self.frame.pack(padx=20, pady=20)

        
        open_button = Button(self.frame, text="Abrir Archivo", background="#C0EFD2", command=self.open_file)
        open_button.grid(row=0, column=0, padx=10, pady=10)

        
        self.grammar_entry = Entry(self.frame, width=30)
        self.grammar_entry.grid(row=0, column=1, padx=10, pady=10)
        self.grammar_entry.insert(0, "")
        self.grammar_entry.config(state="readonly")
        
        self.gramatica_button = Button(self.frame, text="Gramatica", background="#C0EFD2", command=self.gramatica)
        self.gramatica_button.grid(row=1, column=0, padx=10, pady=10)
        
        self.analyze_button = Button(self.frame, text="Analizar", background="#C0EFD2", command=self.analyze)
        self.analyze_button.grid(row=1, column=1, padx=10, pady=10)
        
        clear_button = Button(self.frame, text="LimpiarTodo", background="#C0EFD2", command=self.clear)
        clear_button.grid(row=1, column=2, padx=10, pady=10)


        self.frame_show = Frame(self.root, background="#99A3A4", relief=FLAT, padx=20, pady=20)
        self.frame_show.pack(padx=20, pady=self.frame.winfo_reqheight()+1)

        
        self.canvas = Canvas(self.frame_show,width=600, height=400)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

        self.table_frame = Frame(self.canvas, bg="#CACFD2")
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        self.scrollbar_vertical = Scrollbar(self.frame_show, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar_vertical.pack(side=RIGHT, fill=Y)
        
        self.scrollbar_horizontal = Scrollbar(self.frame_show, orient=HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_horizontal.pack(side=BOTTOM, fill="x")
    
    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetype=[("Archivos de texto", "*.txt")])

        if len(self.file_path) > 0:
            self.grammar_entry.config(state="normal")
            self.grammar_entry.insert(0, self.file_path)
            self.grammar_entry.config(state="readonly")
            
            with open(self.file_path, 'r') as file:
                content = file.read()
            lines = content.splitlines()
            # Lee cada línea del archivo
            noDeLinea = 0
            noterminales = []
            terminales = []
            ReglasL = []
            for line in lines:
                if noDeLinea == 0:
                    noterminales = line.split()
                if noDeLinea == 1:
                    terminales = line.split()
                if noDeLinea > 1:
                    ReglasL.append(line.replace("\n", ""))
                noDeLinea += 1
            # cerrar el archivo
            self.NT=noterminales
            self.TE=terminales
            self.Reglas=ReglasL
            
            
            messagebox.showinfo("Coleccion Canonica", "Archivo seleccionado correctamente")
        else:
            messagebox.showerror("Coleccion Canonica", "No se ha seleccionado un archivo!")
            
    def clear_gram(self):
    # Destruir y reconstruir el marco para la tabla
        if hasattr(self, 'table_frame'):
            self.table_frame.destroy()  # Destruir el marco existente

        self.table_frame = Frame(self.canvas, bg="#CACFD2")  # Crear un nuevo marco
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        
    #def clear_gram(self):
    #    
    #    self.table_frame.destroy()  # Destruir el marco existente
    #    self.table_frame = Frame(self.canvas, bg="#CACFD2")  # Crear un nuevo marco
    #    self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
    
    def clear(self):
        self.file_path = ""
        self.grammar_entry.config(state="normal")
        self.grammar_entry.delete(0, END)
        self.grammar_entry.config(state="readonly")
        
        # Limpiar estructuras de datos
        self.NT = []
        self.TE = []
        self.Reglas = []
        self.Reglas2 = []
        self.result2 = []
        self.tablaAS=[]
        self.result = []
        self.siguientes = []
        self.ir_a_NT=[]
        self.ir_a_TE=[] 
        self.states=[] 
        self.PYS=[]
        
        # Reiniciar variables de estado
        self.isAnalyzed = False
        self.isGrama = False

        # Limpiar la tabla y la interfaz
        self.clear_gram()
    
    def mostrar_tabla(self,result,result2):
        header_columns = self.result.strip().split(' ')    
        header_columns2 = self.result2.strip().split(",")  
        # Mostrar el encabezado en la primera fila de la tabla
        for j, header_text in enumerate(header_columns):
            header_text = header_text.replace("'", "").replace(",", "")
            if header_text == "":
                header_text='*'
            label = Label(
            self.table_frame,
            text=header_text,
            borderwidth=1,
            relief="solid",
            width=15,
            background="#16C4DF",  # Color de fondo
            foreground="black"       # Color de primer plano
            )
            label.grid(row=0, column=j, padx=2, pady=2)

        # Mostrar los elementos de result2 en filas sucesivas
        current_row = 1  # Comenzar desde la segunda fila
        current_col = 0 
        
        for j,header_text in enumerate(header_columns2):
            if "\n\n" not in header_text:
                rango = len(header_columns2)
                if j< rango-1:
                    header_text = header_text.replace("'", "")
                    label = Label(
                    self.table_frame,
                    text=header_text,
                    borderwidth=1,
                    relief="solid",
                    width=15,
                    background="#16DFAE",  # Color de fondo
                    foreground="black"       # Color de primer plano
                    )
                    label.grid(row=current_row, column=current_col, padx=2, pady=2)
                    current_col +=1
                
            else:
                current_row +=1
                current_col=0
        self.isGrama = False

    def analyze(self):
        if self.isGrama is not False:
            self.clear_gram()
            if not self.isAnalyzed:
                self.result,self.result2 = self.tabla_analisis()
                # Write on the text area
                self.mostrar_tabla(self.result,self.result2)

                self.isAnalyzed = True
                
        else:
            messagebox.showerror("TAS", "Primero debes ver la gramatica!")
    
    def gramatica(self):
        if not self.isGrama:
            # Write on the text area
            self.clear_gram()
            self.mostrar_gramatica()
            self.isGrama = True
    
    def mostrar_gramatica(self):
        row=0
        for j, header_text in enumerate(self.Reglas):
            label = Label(
            self.table_frame,
            text=header_text,
            borderwidth=1,
            relief="solid",
            width=20,
            background="#16C4DF",  # Color de fondo
            foreground="black"       # Color de primer plano
            )
            label.grid(row=row, column=1, padx=2, pady=2)
            row +=1
        self.isAnalyzed = False
    
    def tabla_analisis(self):
        self.Reglas2 = self.gramaticaSinEspacios(self.Reglas)
        
        self.PYS = ps.PrimerosYsiguientes(self.TE, self.NT, self.Reglas2)
        self.siguientes = self.PYS['S']
        
        self.ir_a_NT, self.ir_a_TE, self.states = ccan.coleccion_canonica(self.NT, self.TE, self.Reglas)
        
        self.tablaAS = tablaDeAnalisisSintactico(self.Reglas, self.states, self.ir_a_TE, self.ir_a_NT, self.siguientes, self.TE, self.NT)
        
        self.result,self.result2 = imprimirTabla(self.tablaAS, self.TE, self.NT)
        return self.result,self.result2
    
    def gramaticaSinEspacios(self, gramatica):
        nuevaGramatica = []
        for regla in gramatica:
            nuevaGramatica.append(regla.replace(" ", ""))
        return nuevaGramatica

#Programa que contiene la función para obtener la tabla de análisis sintáctico, así como sus funciones auxiliares

def obtenerIndex(simbolo, array):
    for i in range(len(array)):
        if array[i] == simbolo:
            return i
    return -1

def puntoAlFinal(cad):
    final = len(cad) - 1
    return cad[final] == "."

def modificar_cadena(cadOrig):
    indice_punto = cadOrig.find('.')
    if indice_punto > 0 and cadOrig[indice_punto - 1] == ' ':
        cad_modificada = cadOrig[:indice_punto - 1]
        return cad_modificada
    return cadOrig

def leerGramatica(direccion):
    # Abre el archivo en modo de lectura ('r')
    archivo = open(direccion, 'r')
    # Lee cada línea del archivo
    noDeLinea = 0
    noterminales = []
    terminales = []
    ReglasL = []
    for linea in archivo:
        if noDeLinea == 0:
            noterminales = linea.split()
        if noDeLinea == 1:
            terminales = linea.split()
        if noDeLinea > 1:
            ReglasL.append(linea.replace("\n", ""))
        noDeLinea += 1
    # cerrar el archivo
    archivo.close()
    return noterminales, terminales, ReglasL
def imprimirTabla(tas, te, nt):
    result = ""
    result2 = ""
    result += ("estados ")
    if "@" in te:
        for ter in te[:-1]:
            result += ("'" + ter + "' ")
    else:
        for ter in te:
            result += ("'" + ter + "' ")
    result +=  "'$' "
    result += (str(nt).replace("[", "").replace("]", "") + "\n\n")
    i = 0
    for estado in tas:
        result2 += (f"{i},"+ str(estado).replace("[", "").replace("]", ",")+ "\n\n,")
        i += 1
    return result, result2

def tablaDeAnalisisSintactico(Gramatica, coleccionEstados, ir_aTerminales, ir_aNoTerminales, siguientes, terminales, noTerminales):
    TAS = []

    if "@" in terminales:
        lenTerminales = len(terminales) - 1 #variable que guarda la longitud - 1 del arreglo de los simbolos terminales
    else:
        lenTerminales = len(terminales) #variable que guarda la longitud del arreglo de los simbolos terminales

    lenNoTerminales = len(noTerminales) #variable que guarda la longitud del arreglo de los simbolos no terminales
    lenGramatica = len(Gramatica)

    #Creando la tabla de transiciones
    for i in range(len(coleccionEstados)):
        TAS.append([])
        for j in range(lenTerminales + 1 + lenNoTerminales):
            TAS[i].append("  ")

    #Recorremos los ir_a con terminales y se agregan a la tabla de transiciones
    for transiciones in ir_aTerminales:
        simbolo = transiciones[1]   #guarda el símbolo con el que se ejecuta la transicion
        if simbolo == "$":  #Pregunta si es el símbolo de aceptación y lo coloca en la última columna de Acción
            TAS[transiciones[0]][lenTerminales] = "AC"
        else:   #Si no, coloca en [estado][index del simboloTerminal] el número de estado al que va la transicion
            TAS[transiciones[0]][obtenerIndex(transiciones[1], terminales)] = "d" + str(transiciones[2])

    #Recorremos los ir_a con no terminales y se agregan a la tabla de transiciones
    for transiciones in ir_aNoTerminales:
        simbolo = transiciones[1]   #guarda el símbolo con el que se ejecuta la transicion
        #coloca en [estado][lenTerminales + 1 posicion ($) + index del simboloNoTerminal] el número de estado al que va la transicion
        TAS[transiciones[0]][lenTerminales + 1 + obtenerIndex(transiciones[1], noTerminales)] = str(transiciones[2])

    #Recorremos los estados de la colección canónica
    noDeEstado = 0
    for estado in coleccionEstados:
        for elemento in estado:
            if puntoAlFinal(elemento):
                nuevaCadena = modificar_cadena(elemento)    #elimina el punto y el espacio del final del elemento y lo guarda en una nueva cadena
                noTerminal = nuevaCadena[0]     #resguarda el no terminal del que se usarán los siguientes
                for numRegla in range(lenGramatica):    #busca la producción en la gramática
                    if nuevaCadena == Gramatica[numRegla]:  #cuando encuentra la producción en la gramática, comienza a ingresar los remplazar(r)
                        siguientesNoTerminal = siguientes[obtenerIndex(noTerminal, noTerminales)]   #obtiene los siguientes del no terminal
                        for simbolo in siguientesNoTerminal:
                            if simbolo == "$":  #Pregunta si es el símbolo de aceptación y coloca el r en la última columna de Acción
                                TAS[noDeEstado][lenTerminales] = "r" + str(numRegla + 1)
                            else:   #Si no, coloca en [estado][index del simboloTerminal] el número de estado al que va la transicion
                                TAS[noDeEstado][obtenerIndex(simbolo, terminales)] = "r" + str(numRegla + 1)
        noDeEstado += 1
    return TAS



#Gramatica = [
#    "E' E $",   #0
#    "E E + T",  #1
#    "E T",      #2
#    "T T * F",  #3
#    "T F",      #4
#    "F ( E )",  #5
#    "F id"      #6
#]
#
#terminales = ["+", "*", "(", ")", "id"]
#noTerminales = ["E", "T", "F"]
#
#ir_aTerminales = [
#    [0, "(", 4],
#    [0, "id", 5],
#    [1, "$", -1],
#    [1, "+", 6],
#    [2, "*", 7],
#    [4, "(", 4],
#    [4, "id", 5],
#    [6, "(", 4],
#    [6, "id", 5],
#    [7, "(", 4],
#    [7, "id", 5],
#    [8, ")", 11],
#    [8, "+", 6],
#    [9, "*", 7]
#]
#
#ir_aNoTerminales = [
#    [0, "E", 1],
#    [0, "T", 2],
#    [0, "F", 3],
#    [4, "E", 8],
#    [4, "T", 2],
#    [4, "F", 3],
#    [6, "T", 9],
#    [6, "F", 3],
#    [7, "F", 10]
#]
#coleccionEstados = [
#    ["E' . E $", "E . E + T", "E . T", "T . T * F", "T . F", "F . ( E )", "F . id"],
#    ["E' E . $", "E E . + T"],
#    ["E T .", "T T . * F"],
#    ["T F ."],
#    ["F ( . E )", "E . E + T", "E . T", "T . T * F", "T . F", "F . ( E )", "F . id"],
#    ["F id ."],
#    ["E E + . T", "T . T * F", "T . F", "F . ( E )", "F . id"],
#    ["T T * . F", "F . ( E )", "F . id"],
#    ["F ( E . )", "E E . + T"],
#    ["E E + T .", "T T . * F"],
#    ["T T * F ."],
#    ["F ( E ) ."]
#]
#
#siguientes = [
#    ["$", "+", ")"],
#    ["$", "+", ")", "*"],
#    ["$", "+", ")", "*"]
#]
#
#TAS = []
#
##Script
#if "@" in terminales:
#    lenTerminales = len(terminales) - 1 #variable que guarda la longitud - 1 del arreglo de los simbolos terminales
#else:
#    lenTerminales = len(terminales) #variable que guarda la longitud del arreglo de los simbolos terminales
#
#lenNoTerminales = len(noTerminales) #variable que guarda la longitud del arreglo de los simbolos no terminales
#lenGramatica = len(Gramatica)
#
##Creando la tabla de transiciones
#for i in range(len(coleccionEstados)):
#    TAS.append([])
#    for j in range(lenTerminales + 1 + lenNoTerminales):
#        TAS[i].append("  ")
#
##Recorremos los ir_a con terminales y se agregan a la tabla de transiciones
#for transiciones in ir_aTerminales:
#    simbolo = transiciones[1]   #guarda el símbolo con el que se ejecuta la transicion
#    if simbolo == "$":  #Pregunta si es el símbolo de aceptación y lo coloca en la última columna de Acción
#        TAS[transiciones[0]][lenTerminales] = "AC"
#    else:   #Si no, coloca en [estado][index del simboloTerminal] el número de estado al que va la transicion
#        TAS[transiciones[0]][obtenerIndex(transiciones[1], terminales)] = "d" + str(transiciones[2])
#
##Recorremos los ir_a con no terminales y se agregan a la tabla de transiciones
#for transiciones in ir_aNoTerminales:
#    simbolo = transiciones[1]   #guarda el símbolo con el que se ejecuta la transicion
#    #coloca en [estado][lenTerminales + 1 posicion ($) + index del simboloNoTerminal] el número de estado al que va la transicion
#    TAS[transiciones[0]][lenTerminales + 1 + obtenerIndex(transiciones[1], noTerminales)] = str(transiciones[2])
#
##Recorremos los estados de la colección canónica
#noDeEstado = 0
#for estado in coleccionEstados:
#    for elemento in estado:
#        if puntoAlFinal(elemento):
#            nuevaCadena = modificar_cadena(elemento)    #elimina el punto y el espacio del final del elemento y lo guarda en una nueva cadena
#            noTerminal = nuevaCadena[0]     #resguarda el no terminal del que se usarán los siguientes
#            for numRegla in range(lenGramatica):    #busca la producción en la gramática
#                if numRegla == 0:   #ignora la producción 0, ya que es parte de la gramática aumentada
#                    continue
#                if nuevaCadena == Gramatica[numRegla]:  #cuando encuentra la producción en la gramática, comienza a ingresar los remplazar(r)
#                    siguientesNoTerminal = siguientes[obtenerIndex(noTerminal, noTerminales)]
#                    for simbolo in siguientesNoTerminal:
#                        if simbolo == "$":  #Pregunta si es el símbolo de aceptación y coloca el r en la última columna de Acción
#                            TAS[noDeEstado][lenTerminales] = "r" + str(numRegla)
#                        else:   #Si no, coloca en [estado][index del simboloTerminal] el número de estado al que va la transicion
#                            TAS[noDeEstado][obtenerIndex(simbolo, terminales)] = "r" + str(numRegla)
#    noDeEstado += 1
#
#imprimirTabla(TAS, terminales, noTerminales)