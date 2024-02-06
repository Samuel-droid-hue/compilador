from tkinter import filedialog

def get_reglas(path):
    with open(path, 'r') as file:
        content = file.readlines()
    content=' '.join(content)
    content=content.split("\n")
    content ='-|-'.join(content)
    content=content.split("-> ")
    content =''.join(content)
    content=content.split("-|- ")
    no_terminales = content[0].strip()
    terminales = content[1].strip()
    content.pop(0)
    content.pop(0)
    content.pop(0)

    return no_terminales, terminales, content

def obtener_Primeros(S,regla,noTerminales,terminales,bandera=0):
    v=0
    a=0
    primeros=[]
    if S=="@" :
        if bandera==1:
            return bandera,""
        return bandera,S
    if S in terminales :
        return 0,S
    for i in regla:
        i=i.split(" ")
        b=1
        i = [conta for conta in i if conta != '']
        if i[0]==S :
                if len(i)>2:
                    bandera=1
                h=1
                while (bandera==1 or b==1) and i[h] !=S:
                    b=0
                    v,k=obtener_Primeros(i[h],regla,noTerminales,terminales,bandera)
                    if v==1:
                        a=1
                    primeros.append(k)
                    primeros[0]=' '.join(primeros)
                    if len(primeros)==2:
                        primeros.pop(1)
                    if len(i)==2:    
                        break
                    h=h+1
                    if a==1 and v==1:
                        b=1
                    else:
                        bandera=0  
    if a==0 and bandera==1:
        bandera=0
        
    return bandera,primeros[0]  

def obtener_siguientes(i,regla,noterminales,terminale,primeros,sig):
    siguiente=""
    for reg in regla:
        reg=reg.split(" ")
        B=reg[0]
        reg.pop(0)
        reg = [conta for conta in reg if conta != '']
        if i in reg:
                index=reg.index(i)
                if index+1<len(reg):
                    if  reg[index+1] in terminale:
                        siguiente=siguiente+" "+reg[index+1]
                    else:
                        siguiente=siguiente+" "+primeros[reg[index+1]]
                        if "@" in siguiente:
                            conta=1
                            while ("@" in siguiente) and (index+conta<len(reg)):
                                
                                if index+conta!=index+1:
                                    siguiente=siguiente.replace("@","")
                                    if reg[index+conta] in terminale:
                                        siguiente=siguiente+" "+reg[index+conta]
                                    else:
                                        siguiente=siguiente+" "+primeros[reg[index+conta]]
                                conta=conta+1
                            if "@" in siguiente: 
                                if i != B:   
                                    try:
                                        if ("@" in sig[B]) and ("@" in siguiente):
                                            siguiente=siguiente+" "+sig[B]
                                        else:
                                            siguiente=siguiente+" "+sig[B]
                                            siguiente=siguiente.replace("@","")
                                    except KeyError:
                                        if i != B:
                                            sig[B]=obtener_siguientes(B,regla,noterminales,terminale,primeros,sig)
                                            sig[B]=sig[B].split(" ")
                                            sig[B]=list(set(sig[B]))
                                            sig[B] = [conta for conta in sig[B] if conta != '']
                                            sig[B]=' '.join(sig[B])
                                            if ("@" in sig[B]) and ("@" in siguiente):
                                                siguiente=siguiente+" "+sig[B]
                                            else:
                                                siguiente=siguiente+" "+sig[B]
                                                siguiente=siguiente.replace("@","")
                else:
                    if i != B:   
                        try:
                                siguiente=siguiente+" "+sig[B]
                        except KeyError:
                            if i != B:
                                sig[B]=obtener_siguientes(B,regla,noterminales,terminale,primeros,sig)
                                sig[B]=sig[B].split(" ")
                                sig[B]=list(set(sig[B]))
                                sig[B] = [conta for conta in sig[B] if conta != '']
                                sig[B]=' '.join(sig[B])
                                siguiente=siguiente+" "+sig[B]
                                if ("@" in sig[B]) and ("@" in siguiente):
                                    siguiente=siguiente+" "+sig[B]
                                else:
                                    siguiente=siguiente+" "+sig[B]
                                    siguiente=siguiente.replace("@","")
    
    return siguiente

#noterminales = "P T F L D"
#noterminales=noterminales.split(" ")
#
#terminale="( ) int float main id ,"
#terminale=terminale.split(" ")
#
#regla=[
#"P T F ( L )"
#,"T int"
#,"T @"
#,"F main"
#,"F id"
#,"L T P id"
#,"L , P id"
#,"L @"
#,"D T P id"
#,"D @"]

def primeros_siguientes(noterminales,terminale,regla):
    # noterminales="P T F L D I V N E K R B O H S W A X Y M Z G J Q"
    noterminales=noterminales.split(" ")
    # terminale="( ) { } main id , ; [ ] int float printf literalCad scanf & nint nfloat * + - / % = if else while for switch case : < > ! | do return"
    terminale=terminale.split(" ")

    #regla=[
    #"P T F ( L ) { D I O H X A W G }",
    #"T int ",
    #"T float",
    #"F main",
    #"F id",
    #"L T P id V L",
    #"L , P id V L",
    #"L @",
    #"D T P id V L ; D",
    #"D @",
    #"I printf ( literalCad ) ; I",
    #"I scanf ( literalCad , & id ) ; I",
    #"I @",
    #"V [ N ]",
    #"V @",
    #"N nint ",
    #"N @",
    #"E nfloat",
    #"E @",
    #"P * ",
    #"P +",
    #"P -",
    #"P /",
    #"P %",
    #"P @",
    #"K { R }",
    #"K R",
    #"K B P B",
    #"K B + +",
    #"K B - -",
    #"R N E R",
    #"R , N E R",
    #"R @",
    #"B id",
    #"B nint",
    #"B nfloat",
    #"B @",
    #"O B = O ; O",
    #"O B P B P",
    #"O B",
    #"O @",
    #"H if ( B Z B ) { I } S",
    #"H I",
    #"S else { H }",
    #"S @",
    #"W while ( B Z B ) { J O M }",
    #"A for ( B Z B ; B Z B ; K ) { O A }",
    #"A @",
    # "X switch ( id ) { Y } ",
    # "Y case int :  O ; break ; Y",
    # "Y @",
    # "M M - = O ;",
    # "M M + = O ;",
    # "M M + + ;",
    # "M M - - ;",
    # "M id",
    # "M nint ",
    # "Z Z =",
    # "Z =",
    # "Z <",
    # "Z !",
    # "Z >",
    # "Z Z |",
    # "Z |",
    # "Z Z &",
    # "Z &",
    # "G T F ( L ) { Q }",
    # "J do { I } while ( B Z B Z B Z B ) ;",
    # "Q return O ;",]
    bandera=0
    primeros={}
    for i in noterminales:
        bandera,primeros[i]=obtener_Primeros(i,regla,noterminales,terminale)
    for i in noterminales:
        primeros[i]=primeros[i].split(" ")
        primeros[i]=list(set(primeros[i]))
        primeros[i] = [i for i in primeros[i] if i != '']
        primeros[i]=' '.join(primeros[i])
    #print(primeros)

    siguiente={}
    siguiente["P"]="$"
    for i in noterminales:
        try:
            if len(siguiente[i])<2:
                siguiente[i]=siguiente[i]+obtener_siguientes(i,regla,noterminales,terminale,primeros,siguiente)
        except KeyError:
            
            siguiente[i]=obtener_siguientes(i,regla,noterminales,terminale,primeros,siguiente)
        
        siguiente[i]=siguiente[i].split(" ")
        siguiente[i]=list(set(siguiente[i]))
        siguiente[i] = [i for i in siguiente[i] if i != '']
        siguiente[i]=' '.join(siguiente[i])
    #print(siguiente)

    p=[]
    S=[]
    for i in noterminales:
        p.append(primeros[i])
        S.append(siguiente[i])
    PS={}
    PS["S"]=S
    PS["P"]=p

    return PS

#path = filedialog.askopenfilename(filetype=[("Archivos de texto", "*.txt")])
#no_terminales, terminales, reglas = get_reglas(path)
#ps = primeros_siguientes(no_terminales, terminales, reglas)
#print(ps['S'])
#print("######################################################")
#print(ps['P'])