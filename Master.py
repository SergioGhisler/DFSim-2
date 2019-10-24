import math
class Master:
    ############################################
    #               NO TOCAR                   #
    ############################################
    database = None        #Cadena de caracteres (STRING) que contiene toda la informacion del nodo maestro
    slaveDB = None         #Tupla de nodos esclavos
    memoryBlock = None     #Tamanyo del bloque de memoria actual, expresado en numero de caracteres

    def __init__(self, slaveDB, memoryBlock):
        self.database = ""
        self.slaveDB = slaveDB
        self.memoryBlock = memoryBlock

    ############################################
    #       MODIFICAR A PARTIR DE AQUI         #
    ############################################

    def read(self, *args):
        nombre=self.database.find(args[0][0])
        aux=self.database.split(";")
        j=0
        
        ##ARRGELAR ESTO
        aux.pop(0)
        aux.pop()    
        ####################
        resultado=""
        
        
        for i in aux:
            
            a=i.split(":")
            slave=a[0]
            pos=a[1]
            
            resultado=resultado+self.slaveDB[slave].read(pos)


        return resultado

    def write(self, *args):
        espaciolibre= TO DO
        f = open(args[0][0])
        aux=f.read()
        self.database += f.buffer.name+" ;"

        j= math.ceil(len(aux)/self.memoryBlock)
        dict={}
        for k in range(j):
            dict["S"+str(k)] = aux[0:self.memoryBlock]

            aux = aux[self.memoryBlock ::]

        for i in dict:
            print (dict[i])
        j=0
        for i in dict:
            longitud= len(self.slaveDB["S"+str(j)].database)
            if(longitud==self.slaveDB["S"+str(j)].memory):
                j=j+1
                m=0
            else:
                if(longitud==0):
                    m=0
                    
                if(longitud==16):
                    m=1
                if(longitud==32):
                    m=2
                if(longitud==48):
                    m=3
            self.slaveDB["S"+str(j)].write(dict[i])
                
            aux2="S"+str(j)+":"+str(m)+";"
            self.database += aux2
            

        print(self.database)
            
       
        print(len(self.database))
        return None