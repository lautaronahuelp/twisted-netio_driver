from twisted.internet import protocol, reactor, endpoints
from twisted.internet.protocol import connectionDone
from ProtocoloNETIO import ProtocoloNetio
from ProtocoloComando import ProtocoloComando

class ProtoNetio(protocol.Protocol):
    
    def __init__(self, dispositivos):
        self._dispositivos = dispositivos
        self._nroserie = None

    def dataReceived(self, data):
        decodeada = data.decode("ascii")
        print("Se recibio data:" + decodeada)

        recibido = ProtocoloNetio(decodeada)
        if(recibido.procesarString()):
            print("RECIBIDO: ")
            print(recibido)
            #print(recibido.debugString())

            self._dispositivos[recibido.getNroSerie()] = self
            self._nroserie = recibido.getNroSerie()
            print(self._dispositivos)
            #ide=70710494|00=58388E5C|01=123456|03=74|04=FFFF|!34EF
            #ide=70710494|00=58388E5E|07|!11D5
            respuestaAck = ProtocoloNetio()
            if(not(recibido.esAck())):
                respuestaAck.setComoAck()
                respuestaAck.setNroSerie(recibido.getNroSerie()) 
                respuestaAck.setTimestamp(recibido.getTimestamp())
                respuestaAck.setSecuencia(recibido.getSecuencia())

                self.transport.write(respuestaAck.__str__().encode("ascii"))
               
        else:
            print("PROTOCOLO INVALIDO")

    def connectionLost(self, reason):
        if self._nroserie in self._dispositivos:
            del self._dispositivos[self._nroserie]
        print(self._dispositivos)
    
    def enviarComando(self, comando):
        self.transport.write(comando.__str__().encode("ascii"))

class ProtoComandos(protocol.DatagramProtocol):
    def __init__(self, driver):
        self._driver = driver

    def datagramReceived(self, data, addr):
        decodeada = data.decode("ascii")
        print("Se recibio data: %s |De: %s" % (decodeada, str(addr)))
        comando = ProtocoloComando(decodeada)
        if comando.procesarString():
            print(comando.debugString())
            print(self._driver._dispositivos)
            if comando.getNroSerie() in self._driver._dispositivos:
                self.transport.write(data, addr)
                ntComando = ProtocoloNetio()
                ntComando.setNroSerie(comando.getNroSerie())
                ntComando.setComando(comando.getComando())
                self._driver._dispositivos[comando.getNroSerie()].enviarComando(ntComando)
            else:
                respuesta = "noexiste"
                self.transport.write(respuesta.encode("ascii"), addr)
        else:
            print("Recibio erróneo")
               
class DriverNetio(protocol.Factory):
    def __init__(self):
        self._dispositivos = {}

    def buildProtocol(self, addr):
        print("Se crea protocol:" + str(addr))
        return ProtoNetio(self._dispositivos)

d = DriverNetio()

endpoints.serverFromString(reactor, "tcp:54000:interface=192.168.100.4").listen(d)
reactor.listenUDP(53000, ProtoComandos(d))
reactor.run()