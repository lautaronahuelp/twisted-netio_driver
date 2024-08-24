class ProtocoloComando:
    _tokens = ["ide", "10", "15"]
    #ide=70710494|15=1|10=KBY:1234|!
    def __init__(self, stringInicial = None):
        self._stringOriginal = ""
        self._stringLimpio = None

        if stringInicial != None:
            self._stringOriginal = stringInicial
        
        self._nroserie = ""
        self._particion = 1
        self._kby = ""
        self._valido = False
        
    def debugString(self):
        return ("nroserie: %s\n\rparticion: %d\n\rkby: %s\n\r" % (self._nroserie, self._particion, self._kby))
    
    def procesarString(self):
        diccionarioProtocolo = {}
        if(self.esValido()):
            stringDescontruido = self._stringLimpio.rsplit("|")
            for sp in stringDescontruido:
                if sp.find("=") != -1:
                    campoDes = sp.split("=")
                    if(self._tokens.count(campoDes[0]) == 1):
                        diccionarioProtocolo[campoDes[0]] = campoDes[1]
                        if(campoDes[0] == "ide"):
                            self._nroserie = campoDes[1]
                        elif(campoDes[0] == "10"):
                            self._kby = campoDes[1].strip("KBY:")
                        elif(campoDes[0] == "15"):
                            self._particion = int(campoDes[1], 0)
            return True
        return False
    
    def esValido(self):
        #ide=70710494|15=1|10=KBY:1234|!
        band = False

        if self._stringOriginal != None:
            protocoloLength = len(self._stringOriginal)
            if protocoloLength >= 28 and self._stringOriginal.startswith("ide") and self._stringOriginal[-1] == "!":
                    band = True
                    self._stringLimpio = self._stringOriginal

        self._valido = band
        
        return self._valido
