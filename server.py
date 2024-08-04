from twisted.internet import protocol, reactor, endpoints
from ProtocoloNETIO import ProtocoloNetio

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        decodeada = data.decode("ascii")
        print("Se recibio data:" + decodeada)

        recibido = ProtocoloNetio(decodeada)
        if(recibido.procesarString()):
            print("RECIBIDO: ")
            print(recibido)
            #<ide=70710494|00=58388E5C|01=123456|03=74|04=FFFF|!34EF>
            #ide=70710494|00=58388E5E|07|!11D5
            respuestaAck = ProtocoloNetio()
            if(not(recibido.esAck())):
                #if(recibido.getSecuencia() != -1):
                #    pass#respuestaAck = "ide=%s|" % ()
                #else:
                    respuestaAck.setComoAck()
                    respuestaAck.setNroSerie(recibido.getNroSerie()) 
                    respuestaAck.setTimestamp(recibido.getTimestamp())
                    respuestaAck.setSecuencia(recibido.getSecuencia())

                    self.transport.write(respuestaAck.__str__().encode("ascii"))
               
        else:
            self.transport.write(data)
            print("PROTOCOLO INVALIDO")
        

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        print("Se crea protocol:" + str(addr))
        return Echo()

endpoints.serverFromString(reactor, "tcp:54000:interface=192.168.100.4").listen(EchoFactory())
reactor.run()