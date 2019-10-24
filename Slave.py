class Slave:
    ############################################
    #               NO TOCAR                   #
    ############################################
    # Cadena de caracteres (STRING) que contiene toda la informacion del nodo esclavo
    database = None
    id = None  # Nombre del nodo esclavo
    memory = None

    def __init__(self, id, maxMemory):
        self.database = ""
        self.id = id
        self.memory = maxMemory

    ############################################
    #       MODIFICAR A PARTIR DE AQUI         #
    ############################################

    def read(self, *args):
        pos=int(args[0])
        if(pos==0):
            return self.database[0:16]
        if(pos==1):
            return self.database[16:32]
        if(pos==2):
            return self.database[32:48]
        if(pos==3):
            return self.database[48:64]

    def write(self, *args):
        self.database += args[0]

        return None
