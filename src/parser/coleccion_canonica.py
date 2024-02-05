from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import Tk
import re

class ColeccionCanonica:
    def __init__(self):
        self.file_path = ""
        self.isAnalyzed = False

        # Variables
        self.terminals = []
        self.not_terminals = []
        self.gramatical_rules = []
        self.result= ""

        # Window
        self.root = Toplevel()
        self.root.geometry("800x700+400+60")
        self.root.title("Coleccion Canonica")
        self.root.config(bg="#34495E")
        self.root.resizable(False, False)

        # Interface Components
        self.frame = Frame(self.root, background="#99A3A4", relief=SUNKEN, padx=20, pady=20)
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

        self.frame_show = Frame(self.root, background="#CACFD2", relief=SUNKEN, padx=20, pady=20)
        self.frame_show.pack(padx=20, pady=self.frame.winfo_reqheight() + 20)

        self.grammar_entry_show = Text(self.frame_show, width=80, height=25, wrap="word")
        self.grammar_entry_show.grid(row=1, column=1, padx=10, pady=10)
        self.grammar_entry_show.insert("1.0", "")
        self.grammar_entry_show.config(state="disabled")
        
        scrollbar = Scrollbar(self.frame_show, command=self.grammar_entry_show.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.grammar_entry_show.config(yscrollcommand=scrollbar.set)

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetype=[("Archivos de texto", "*.txt")])

        if len(self.file_path) > 0:
            self.grammar_entry.config(state="normal")
            self.grammar_entry.insert(0, self.file_path)
            self.grammar_entry.config(state="readonly")
            
            with open(self.file_path, 'r') as file:
                content = file.read()
            lines = content.splitlines()
            
            # Assignment terminals and not terminals symbols
            self.not_terminals = lines[0].split(' ')
            self.terminals = lines[1].split(' ')

            # Assignment gramatical rules
            for i in range(2, len(lines)):
                rule = lines[i].split(' -> ')
                rule[-1] = self.split_derivation(rule[-1])
                self.gramatical_rules.append(rule)

            messagebox.showinfo("Coleccion Canonica", "Archivo seleccionado correctamente")
        else:
            messagebox.showerror("Coleccion Canonica", "No se ha seleccionado un archivo!")

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
    
    def restart(self):
        self.terminals = []
        self.not_terminals = []
        self.gramatical_rules = []
        self.isAnalyzed = False
    
    def clear(self):
        self.restart()
        self.clear_text()

    def analyze(self):
        if self.isAnalyzed == False and len(self.file_path) > 0:

            self.result = self.conjunto_canonico()

            # Write on the text area
            self.grammar_entry_show.config(state="normal")
            self.grammar_entry_show.insert("1.0", self.result)
            self.grammar_entry_show.config(state="disabled")

            self.isAnalyzed = True
        else:
            messagebox.showwarning("Coleccion Canonica", "Seleccione un archivo!")
    
    def split_derivation(self, derivation):
        # Importante : Debera borra la siguiente linea yo solo la coloque para tratar las variables como globales en este caso equivalencia al atributo del objeto

        symbols = self.terminals + self.not_terminals + ['$'] + ['@']

        pattern = '|'.join(map(re.escape, symbols))
        result = re.findall(pattern, derivation)

        return result
    
    # ---------------------- FORMAT ---------------------------
    # Format to an only grammar element
    def element_format(self, element):
        symbol = element[0]
        list_production = element[1]
        production = ""

        for i in list_production:
            production += i

        return f"[ {symbol} -> {production} ]"

    # Format to all one state
    def status_format(self, state):
        if isinstance(state, list):
            format = ""

            for element in state:
                format += self.element_format(element) + " "
        
            return "{ " + format + "}"
        else:
            return state

    # Output format
    def ouput_item_format(self, item):
        element = ""
        element += item[0]

        sublist = item[-1]
        for i in sublist:
            element += " " + i

        return element

    def output_format(self, state):
        format = []
        
        for element in state:
            format.append(self.ouput_item_format(element))
        
        return format
    # ---------------------------------------------------------

    def conjunto_canonico(self):    
        output = ""
        
        output += f"Terminals: {self.terminals}\n"
        output += f"Not Terminals: {self.not_terminals}\n"
        output += f"Grammar: {self.status_format(self.gramatical_rules)}\n\n"
        
        # -- Step 1
        states = []
        final = []

        i0 = self.move_dot_together([self.gramatical_rules[0]])
        states.append(self.full_lock(i0))
        final.append(self.status_format(states[0]))

        # Variable to state current and new
        icurrent = 0
        inew = 0
        
        
        output += f"Cerradura: ({self.status_format(i0)})\n"
        output += f"I{inew} = {self.status_format(final[0])}\n\n"

        for s in states:
            while s:
                w, matches = self.search_after_point(s)

                if isinstance(matches, list):
                    matches = self.move_dot_together(matches)
                    cerradura = self.full_lock(matches)
                    if self.search_matches(final, self.status_format(cerradura)) is False and cerradura and w != '.':
                        final.append(self.status_format(cerradura))
                        states.append(cerradura)
                        inew += 1
                        output += f"Ir_a (I{icurrent}, {w}) = Cerradura: ({self.status_format(matches)})\n"
                        output += f"I{inew} = : {self.status_format(cerradura)}\n\n"
                else:
                    final.append(matches)
                    if matches == "Aceptacion":
                        output += f"Ir_a (I{icurrent}, {w}) = {matches}\n\n"

            icurrent += 1
        return output

    # ------------------------ POINT --------------------------
    # Only changes position point
    def move_dot(self, derivation):
        if '.' not in derivation:
            derivation.insert(0, '.')
        elif derivation.index('.') == len(derivation) - 1:
            derivation = None
        else:
            position = derivation.index('.')
            derivation.remove('.')
            position += 1
            derivation.insert(position, '.')
            
        return derivation

    # Changes position point into a set
    # Recive a list of lists of items
    def move_dot_together(self, element):
        i = 0
        while i < len(element):
            element[i][-1] = self.move_dot(element[i][-1])
            if element[i][-1] == None:
                element.pop(i)
                i = 0
            else:
                i += 1

        #for i in range(len(element)):
            #element[i][-1] = self.move_dot(element[i][-1])
            #if element[i][-1] == None:
                #element.pop(i)
        
        return element
    # ---------------------------------------------------------

    # ---------------------- SEARCH ---------------------------
    # Search into productions by not terminal symbol
    def search_productions(self, not_terminal):
        result = []

        for i in range(len(self.gramatical_rules)):
            if self.gramatical_rules[i][0] == not_terminal:
                result.append(self.gramatical_rules[i])
        
        return result

    # To determinate if there are same states
    def search_matches(self, list, element):
        if element in list:
            return True
        else:
            return False

    # Recieve a state
    def search_after_point(self, state):
        result = []
        element = self.after_point(state[0])
        result.append(state.pop(0))
        if element == "$":
            return element, "Aceptacion"
        else:
            
            while state and self.after_point(state[0]) == element:
                result.append(state.pop(0))

            return element, result

    # Seach element after the point
    def after_point(self, production):
            index = production[-1].index('.')
            if index < len(production[-1]) - 1:
                return production[-1][index+1]
            else:
                return production[-1][index]
    # ---------------------------------------------------------
            
    # ---------------------- LOCK -----------------------------
    # Calculate lock of an only element
    def element_lock(self, element):
        # Importante : Debera borra la siguiente linea yo solo la coloque para tratar las variables como globales en este caso equivalencia al atributo del objeto
        global not_terminals

        # p : point's position
        # c : current symbol to search a
        # n : next symbol to search e

        result = [element]
        queue = []
        n = ""

        p = result[0][-1].index('.')
        if p < len(result[0][-1])-1:
            n = result[0][-1][p+1]
            if n in self.not_terminals:
                queue = self.move_dot_together(self.search_productions(n))

        # Saber el estado actual
        c = n
        # Mientras la pila de operaciones no este vacia
        while queue:
            p = queue[0][-1].index('.')
            # Si el punto no esta al final
            #######################################
            # if p < len(queue[0][-1]):
            if p < len(queue[0][-1])-1:
                n = queue[0][-1][p+1]
                # Si el elemento siguiente es no terminal y es igual que actual
                # Solo apila no calcules
                if n in self.not_terminals and n == c:
                    # Busca si el resultado existe o no 
                    if self.search_matches(result, queue[0]) is False:
                        result.append(queue.pop(0))
                    else:
                        queue.pop(0)
                # Si el elemento siguiente es un terminal
                elif n in self.terminals:
                    if self.search_matches(result, queue[0]) is False:
                        result.append(queue.pop(0))
                    else:
                        queue.pop(0)
                # Si el elemento siguiente es diferente del actual y es no terminal
                # Calcula de nuevo y apila
                elif n != c and n in self.not_terminals:
                    if self.search_matches(result, queue[0]) is False:
                        result.append(queue.pop(0))
                    else:
                        queue.pop(0)
                    ###########################################################
                    # HERE IS THE ERROR!!!!
                    queue_aux = self.move_dot_together(self.search_productions(n))
                    for item in queue_aux:
                        queue.append(item)
                    # queue.append(move_dot_together(search_productions(n)))
                    # queue = move_dot_together(search_productions(n))
                    ###########################################################
            
                # Caso para el epsilon donde solamente se calcula el L -> .
                elif n == '@':
                    aux = queue.pop(0)
                    aux[-1] = ['.']
                    if self.search_matches(result, aux) is False:
                        result.append(aux)
            #######################################
            # Si el punto esta al final
            #######################################
            else:
                if self.search_matches(result, queue[0]) is False:
                    result.append(queue.pop(0))
                else:
                    queue.pop(0)
            # Actualiza el simbolo actual
            ##############################################
            # En caso de que el elemento exista en la pila
            ##############################################
            c = n
        return result

    def full_lock(self, list):
        new_state = []
        back = None

        for element in list:
            back = self.restore_grammar()
            new_state += self.element_lock(element)
            self.gramatical_rules = back

        return new_state
    # ---------------------------------------------------------

    def coleccion_canonica(self, TE, NT, rules):
        terminals = NT

        not_terminals = TE

        # Parse to data structure rules
        self.create_rules(rules)
        
        # -- Step 1
        states = []
        final = []

        # Output
        output_states = []
        output_ir_a_NT = []
        output_ir_a_TE = []

        i0 = self.move_dot_together([self.gramatical_rules[0]])
        states.append(self.full_lock(i0))
        final.append(self.status_format(states[0]))
        output_states.append(self.output_format(states[0]))

        # Variable to state current and new
        icurrent = 0
        inew = 0

        for s in states:
            while s:
                w, matches = self.search_after_point(s)

                if isinstance(matches, list):
                    matches = self.move_dot_together(matches)
                    cerradura = self.full_lock(matches)
                    if self.search_matches(final, self.status_format(cerradura)) is False and cerradura and w != '.':
                        final.append(self.status_format(cerradura))
                        states.append(cerradura)
                        # output_states.append(status_format(cerradura))
                        output_states.append(self.output_format(cerradura))
                        inew += 1
                        if w in terminals:
                            output_ir_a_TE.append([icurrent, w, inew])
                        elif w in not_terminals:
                            output_ir_a_NT.append([icurrent, w, inew])
                        # print(f"Ir_a (I{icurrent}, {w}) = Cerradura: ({status_format(matches)} )")
                        # print(f"I{inew} = : {status_format(cerradura)}\n")
                    elif self.search_matches(final, self.status_format(cerradura))is True:
                        # print(f"Ir_a (I{icurrent}, {w}) = Cerradura: ({status_format(matches)} )")
                        # print(f"I{final.index(status_format(cerradura))} = : {status_format(cerradura)}\n")
                        if w in terminals:
                            output_ir_a_TE.append([icurrent, w, final.index(self.status_format(cerradura))])
                        elif w in not_terminals:
                            output_ir_a_NT.append([icurrent, w, final.index(self.status_format(cerradura))])

                else:
                    #final.append(matches)
                    if matches == "Aceptacion":
                        #print(f"Ir_a (I{icurrent}, {w}) = {matches}\n")
                        output_ir_a_TE.append([icurrent, w, -1])
                        
            icurrent += 1

        self.gramatical_rules.clear()
        
        return output_ir_a_NT, output_ir_a_TE, output_states

    def create_rules(self, rules):
        aux_s = []
        aux_list = []
        symbol = ""
        
        # First rule type $
        self.gramatical_rules.append([rules[0][0]+"'", [rules[0][0], "$"]])

        for i in rules:
            aux_s = i.split(" ")
            symbol = aux_s.pop(0)
            for j in aux_s:
                aux_list.append(j)
            self.gramatical_rules.append([symbol, aux_list])
            aux_list = []

    # ------------------- AUXILIARY ---------------------------
    def restore_grammar(self):
        gram_original=[]
        gram_original2=[]
        # Recorre gramatical rules
        # RECUERDA AGREGAR GRAMATICAL RULES SELF
        for r in range(len(self.gramatical_rules)):
            gram_original2=[]
            # 2 por que son dos elementos
            for k in range(2):
                # RECUERDA AGREGAR GRAMATICAL RULES SELF
                for i in range(len(self.gramatical_rules[r][k])):
                    if k!=0:
                        # RECUERDA AGREGAR GRAMATICAL RULES SELF
                        gram_original2.append(self.gramatical_rules[r][k][i]) 
                    else:
                        if i!=1 and k!=1:
                            # RECUERDA AGREGAR GRAMATICAL RULES SELF
                            gram_original2.append(self.gramatical_rules[r][k])
            gram_original.append(gram_original2) 
        
        original=[]
        for i in range(len(gram_original)):
            aux=""
            aux2=[]
            original_aux=[]
            for k in range(len(gram_original[i])):
                if k==0:
                    aux=gram_original[i][k]
                else:
                    aux2.append(gram_original[i][k])
            original_aux.append(aux)
            original_aux.append(aux2)
            original.append(original_aux)

        return original
    # -----------------------------------------------------------