import random
class Slave:
    ############################################
    #               NO TOCAR                   #
    ############################################
    # Cadena de caracteres (STRING) que contiene toda la informacion del nodo esclavo
    database = None
    id = None  # Nombre del nodo esclavo
    memory = None

    def map(self,*args):
        pos=int(args[0])
        operacion=args[2]
        texto= self.database[pos*int(args[1]):pos*int(args[1])+int(args[1])].lower()
        d={}
        if operacion=="caracter":
            for i in texto:
                if i in d:
                    d[i]=d[i]+1
                else:
                    d[i]=1
        if operacion=="duo":

            aux=[]
            
            while len(texto)>=2:
                aux.append(texto[0]+texto[1])
                texto=texto[1:]
            for i in aux:
                if i in d:
                    d[i]=d[i]+1
                else:
                    d[i]=1


        if operacion == "palabras":
            texto= texto.split()
            for i in texto:
                d[i]= len(i)

        return d

    def reduce(self,*args):
        aux= args[0]
        operacion= args[1]
        d={}
        if operacion== 'palabras':
            d[aux[0][0]]=aux[0][1]
        else:
            
            for i in aux:
                if i[0] in d:
                    d[i[0]]=d[i[0]]+i[1]
                else:
                    d[i[0]]=i[1]
        return d
    def __init__(self, id, maxMemory):
        self.database = ""
        self.id = id
        self.memory = maxMemory

    ############################################
    #       MODIFICAR A PARTIR DE AQUI         #
    ############################################

    def read(self, *args):
        pos=int(args[0])
        
        return self.database[pos*int(args[1]):pos*int(args[1])+int(args[1])]
        

    def write(self, *args):
        pos=len(self.database)/args[1]
        self.database += args[0]
        p= 0.000001#En porcentaje es 0.000001% 
        if(random.random() < p ):
            self.database= ""
            print('Se ha borrado slave '+self.id )
        return pos

    def delete(self, *args):
        pos=int(args[0])
        
        self.database=self.database.replace( self.database[pos*int(args[1]):pos*int(args[1])+int(args[1])],'')
       
        return None