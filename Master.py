import math
import random
import re
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

    def read(self, *args):

        aux = self.database.split(";")
        nombre = aux.index(args[0][0]+"$%&")
        del aux[-1]
        j = 0

        lon = int(aux[nombre+1])
        aux = aux[nombre+2:nombre+2+lon]

        resultado = ""

        for i in aux:

            a = i.split(":")
            slave = a[0]
            pos = a[1]

            resultado = resultado + \
                self.slaveDB[slave].read(pos, self.memoryBlock)

        doc = open('lectura_'+args[0][0], 'a')
        doc.seek(0)
        doc.truncate()
        doc.write(resultado)
        doc.close()
        return None

    def wirteSecuencial(self, *args):
        j = 0
        for k in args[0]:
            successful = False
            while not successful:
                if len(self.slaveDB['S'+str(j)].database) == self.slaveDB['S'+str(j)].memory:
                    if(j==len(self.slaveDB)-1):
                        j=0
                    else:
                        j += 1
                    
                else:
                    texto = args[0][k]
                    pos = int(self.slaveDB['S'+str(j)].write(texto, self.memoryBlock))
                    self.database += 'S'+str(j)+':'+str(pos)+";"
                    
                    if(j==len(self.slaveDB)-1):
                        j=0
                    else:
                        j += 1
                    successful=True
                


        print(self.database)
    def writeAleatorio(self,*args):
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
                    texto = args[0][k]
                    pos = int(self.slaveDB[aux].write(texto, self.memoryBlock))
                    self.database += aux+':'+str(pos)+";"
                    successful=True
        print(self.database)           
    def writePrimeroVacio(self, *args):
        vuelta=0
        for i in args[0]:
            texto=args[0][i]

            for j in self.slaveDB:
                pos=int(len(self.slaveDB[j].database)/self.memoryBlock)
                if(pos!=vuelta):
                    if j== list(self.slaveDB)[len(self.slaveDB)-1]:
                        vuelta+=1
                    continue

                else:
                    self.slaveDB[j].write(texto,self.memoryBlock)
                    self.database+=j+':'+str(pos)+";"
                    if j== list(self.slaveDB)[len(self.slaveDB)-1]:
                        vuelta+=1
                    break

        print(self.database)
    def writeMaximaCarga(self,*args):
        for i in args[0]:
            texto=args[0][i]
            for j in self.slaveDB:
                if len(self.slaveDB[j].database)==self.slaveDB[j].memory:
                    continue
                else:
                    pos=int(self.slaveDB[j].write(texto,self.memoryBlock))
                    self.database+=j+':'+str(pos)+";"
                    break

        print(self.database)





        

    def write(self, *args):
        memoriaMaxima = int(len(self.slaveDB)*(self.slaveDB[list(self.slaveDB)[0]].memory/self.memoryBlock))
        
        
        switcher = {
            1: self.writePrimeroVacio,
            2: self.writeAleatorio,
            3: self.wirteSecuencial,
            4: self.writeMaximaCarga
        }

        f = open(args[0][0])
        
        # la z la anadimos para tener el metadato de la longitud
        aux=f.read()
        z= math.ceil(len(aux)/self.memoryBlock)
        aux2= self.database.split(";")
        dict={}
        for k in range(z):
            # Con ljust nos aseguramos que todos los bloques sean del mismo tamano
            dict["S"+str(k)] = aux[0:self.memoryBlock].ljust(self.memoryBlock)

            aux = aux[self.memoryBlock ::]

        
        i=0
        for j in aux2:
            if '$%&' in j:
                i+=1
        i=i*2
        huecosRestantes=memoriaMaxima-(len(aux2)-i)
        if z<huecosRestantes:
            self.database += f.buffer.name+"$%&;"+str(z)+";"
            command = input("Tipo--> ") 
        
            output = switcher[int(command)](dict)
        else:
            print("No queda espacio para este texto")
            output = "none"
        

        


    def delete(self, *args):
            
        aux=self.database.split(";")
        nombre=aux.index(args[0][0]+"$%&")
        del aux[-1]
        j=0
        
        lon=int(aux[nombre+1])
        aux2=aux[nombre+2:nombre+2+lon]
       
        get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x in y]
        
        
        for i in reversed(aux2):
            
            a=i.split(":")
            slave=a[0]
            pos=int(a[1])
            max=int(self.slaveDB[slave].memory/self.memoryBlock)-1
            if pos!=max:
                if(len(self.slaveDB[slave].database)==self.database):
                    self.slaveDB[slave].delete(pos,self.memoryBlock)
                else:
                    indices=get_indexes(slave+':',aux)
                    
                    for p in indices:
                        if int(aux[p].split(':')[1])>pos:
                            
                            aux[p]=aux[p].split(':')[0]+':'+str(int(aux[p].split(':')[1])-1)
                            
                        
                        
                        

            self.slaveDB[slave].delete(pos,self.memoryBlock)

        del aux[nombre:nombre+2+lon]
        
        self.database=';'.join(aux)
        if aux:
            self.database+=';'
        print(self.database)
        return None
