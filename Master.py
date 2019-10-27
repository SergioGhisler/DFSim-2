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
        
        aux=self.database.split(";")
        nombre=aux.index(args[0][0])
        del aux[-1]
        j=0
        
        lon=int(aux[nombre+1])
        aux=aux[nombre+2:nombre+2+lon]
       
        resultado=""
        
        
        for i in aux:
            
            a=i.split(":")
            slave=a[0]
            pos=a[1]
            
            resultado=resultado+self.slaveDB[slave].read(pos,self.memoryBlock)

        doc=Path(args[0][0]).touch()
        doc.write(resultado)
        return resultado

    def write(self, *args):

        j=0
        m=0
        #Si ya hay algo guardado en memoria seguir por donde lo dejol
        if(self.database!=''):
            sep=self.database.split(";")
            del sep[-1]
            a= sep[-1].split(":")
            j=int(a[0][1 : : ])
             
            m=int(a[1])+1
            #Por si el ultimo nodo esta a tope
            if(len(self.slaveDB["S"+str(j)].database)==self.slaveDB["S"+str(j)].memory):
                j=j+1
                m=0
           
        
        f = open(args[0][0])
        aux=f.read()
        z= math.ceil(len(aux)/self.memoryBlock)
        # la z la anadimos para tener el metadato de la longitud
        self.database += f.buffer.name+";"+str(z)+";"
        
        dict={}
        for k in range(z):
            dict["S"+str(k)] = aux[0:self.memoryBlock].ljust(self.memoryBlock)

            aux = aux[self.memoryBlock ::]

        
        for i in dict:
            
            self.slaveDB["S"+str(j)].write(dict[i])
                
            aux2="S"+str(j)+":"+str(m)+";"
            self.database += aux2
            longitud= len(self.slaveDB["S"+str(j)].database)
            if(longitud==self.slaveDB["S"+str(j)].memory):
                j=j+1
                m=0
            else:
                m+=1
            
            

        print(self.database)
            
       
        print(len(self.database))
        return None