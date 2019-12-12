import math
import random
import re
from time import time
import os
class Master:
    ############################################
    #               NO TOCAR                   #
    ############################################
    # Cadena de caracteres (STRING) que contiene toda la informacion del nodo maestro
    database = None
    slaveDB = None  # Tupla de nodos esclavos
    # Tamanyo del bloque de memoria actual, expresado en numero de caracteres
    memoryBlock = None

    def __init__(self, slaveDB, memoryBlock):
        self.database = ""
        self.slaveDB = slaveDB
        self.memoryBlock = memoryBlock

    ############################################
    #       MODIFICAR A PARTIR DE AQUI         #
    ############################################


    def mapReduce(self,*args):
        operacion = args[0][1]

        aux = self.database.split(";")
        factor_replicacion=int(aux[0])
        if not args[0][0]+"$%&" in aux:
            print("No existe ese archivo")
            return None
        nombre = aux.index(args[0][0]+"$%&")
        del aux[-1]
        

        lon = int(aux[nombre+1])
        aux = aux[nombre+2:nombre+2+lon]

        
        aux2={}
        contador=0
        while True:
            aux2[contador]=(aux[0:factor_replicacion])
            del aux[0:factor_replicacion]
            contador+=1
            if len(aux)==0:
                break
        d={}
        for i in aux2:
            mindict= aux2[i]
            for j in range(0,len(aux2)):
                a = mindict[j].split(":")
                slave = a[0]
                pos = int(a[1])
                hasheo = int(a[2])
                if(hasheo==hash(self.slaveDB[slave].database[pos*int(self.memoryBlock):pos*int(self.memoryBlock)+int(self.memoryBlock)])):
                    busqueda=j
                
                    break
            
            a = mindict[j].split(":")
            slave = a[0]
            pos = a[1]
            hasheo = a[2]

            

            
            #Lo que es el mapReduce empieza aqui, antes solo hemos accedido al igual que en el leer al texto.
            map= self.slaveDB[slave].map(pos, self.memoryBlock,operacion)
            for i in map:
                if i in d:
                    d[i].append(tuple((i,map[i])))
                else:
                    d[i]=[(i,map[i])]
            contador=0
        resultado={}
        
        for i in d:
            resultado.update(self.slaveDB['S'+str(contador)].reduce(d[i],operacion))
            if contador<len(self.slaveDB)-1:
                contador+=1
            else:
                contador=0
        resultado=list(resultado.items())
        if operacion=='palabras':
            
            aux=list(sorted( ((v,k) for k,v in resultado)))
            resultado=[]
            for i in aux:

                resultado.append(i[1])

        if '' in resultado:
            index=resultado.index('')
            del resultado[index]
        print(resultado)

        return resultado

    def read(self, *args):
        
        tiempoInicial= time()
        aux = self.database.split(";")
        factor_replicacion=int(aux[0])
        if not args[0][0]+"$%&" in aux:
            print("No existe ese archivo")
            return None
        nombre = aux.index(args[0][0]+"$%&")
        del aux[-1]
        j = 0

        lon = int(aux[nombre+1])
        aux = aux[nombre+2:nombre+2+lon]

        resultado = ""
        aux2={}
        contador=0

        ##Para hacer un diccionario de tuplas del mismo fragmento de texto
        while True:
            aux2[contador]=(aux[0:factor_replicacion])
            del aux[0:factor_replicacion]
            contador+=1
            if len(aux)==0:
                break
            
        for i in aux2:
            mindict= aux2[i]
            for j in range(0,len(aux2)):
                a = mindict[j].split(":")
                slave = a[0]
                pos = int(a[1])
                hasheo = int(a[2])
                if(hasheo==hash(self.slaveDB[slave].database[pos*int(self.memoryBlock):pos*int(self.memoryBlock)+int(self.memoryBlock)])):
                    busqueda=j
                
                    break
            
            a = mindict[j].split(":")
            slave = a[0]
            pos = a[1]
            hasheo = a[2]

            resultado = resultado + \
                self.slaveDB[slave].read(pos, self.memoryBlock)

        doc = open('lectura_'+args[0][0], 'a')
        doc.seek(0)
        doc.truncate()
        doc.write(resultado)
        doc.close()
        
        tiempoFinal=time()
        tiempoTotal= tiempoFinal-tiempoInicial
        print("lectura"+str(tiempoTotal))
        return None

        
    def writeAleatorio(self,*args):
        factor_replicacion= int(args[1])
        tiempoInicial= time()
        
        j = 0
        noLlenos=dict(self.slaveDB)
        
        for k in args[0]:
            aux=random.choice(list(noLlenos.keys()))
            successful = False
            while not successful:
                if len(self.slaveDB[aux].database) == self.slaveDB[aux].memory:
                    del noLlenos[aux]
                    aux=random.choice(list(noLlenos.keys()))
                    
                else:
                    noUsado=dict(self.slaveDB)

                    for i in range(0,factor_replicacion):
                        texto = args[0][k]
                        pos = int(self.slaveDB[aux].write(texto, self.memoryBlock))
                        self.database += aux+':'+str(pos)+":"+str(hash(texto))+";"
                        del noUsado[aux]
                        aux=random.choice(list(noUsado.keys()))
                        
                    successful=True
        tiempoFinal=time()
        tiempoTotal= tiempoFinal-tiempoInicial
        print("escritura"+str(tiempoTotal))         
   




        

    def write(self, *args):
        if self.database=='':
            factor_de_replicacion= input("Introduzca el factor de replicacion del sisrtema: ")
            self.database=factor_de_replicacion+';'
        #Total de la memoria total del sistema
        memoriaMaxima = int(len(self.slaveDB)*(self.slaveDB[list(self.slaveDB)[0]].memory/self.memoryBlock))

        switcher = {
           ### 1: self.writePrimeroVacio,
            2: self.writeAleatorio,
            ###3: self.wirteSecuencial,
            ###4: self.writeMaximaCarga
        }
        if not os.path.isfile(args[0][0]):
            print('Ese archivo no existe')
            return None
        f = open(args[0][0])
        
        # la z la anadimos para tener el metadato de la longitud
        # Z es el número de "huecos" que utiliza el texto
        aux=f.read()
        
        z= math.ceil(len(aux)/self.memoryBlock)
        aux2= self.database.split(";")
        if  args[0][0]+"$%&" in aux2:
            print("Ya existe este archivo")
            return None
        dict={}
        for k in range(z):
            # Con ljust nos aseguramos que todos los bloques sean del mismo tamano
            dict["S"+str(k)] = aux[0:self.memoryBlock].ljust(self.memoryBlock)

            aux = aux[self.memoryBlock ::]

        factor_replicacion = aux2[0]
        
        i=0
        for j in aux2:
            if '$%&' in j:
                i+=1
        i=i*2
        #+1 pq siempre hay un hueco vacio en el diccionario
        huecosRestantes=memoriaMaxima-(len(aux2)-i)+1
        if z*int(factor_replicacion)<huecosRestantes:
            self.database += f.buffer.name+"$%&;"+str(z*int(factor_replicacion))+";"
            command = 2
            '''input("Tipo--> (1: Primero vacio 2: Aleatorio 3:Secuencial 4: Máxima carga) ") '''
        
            output = switcher[int(command)](dict,factor_replicacion)
        else:
            print("No queda espacio para este texto")
            output = "none"
        

        


