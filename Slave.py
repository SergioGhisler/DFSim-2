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
        return self.database[pos*int(args[1]):pos*int(args[1])+int(args[1])]
        

    def write(self, *args):
        self.database += args[0]

        return None

    def delete(self, *args):
        pos=int(args[0])
        sust= "#" * int(args[1])
        self.database=self.database.replace( self.database[pos*int(args[1]):pos*int(args[1])+int(args[1])],sust)
       
        return None