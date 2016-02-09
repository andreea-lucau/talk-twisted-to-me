import logging
import sys

from twisted.internet import protocol, reactor
from twisted.protocols import basic

import common
import config


class CuriousProtocol(basic.LineReceiver):
    def dataReceived(self, data):
        logging.info("received data from server: [%s]", data)
        if data == config.START_MESSAGE:
            logging.info("will send question to server")
            self.transport.write("what is the meaning of life?\r\n")

        sys.stdout.write(data)


class CuriousClientFactory(protocol.ClientFactory):
    def startedConnecting(self, connector):
        logging.info("starting client connection")

    def buildProtocol(self, addr):
        logging.info("client connected to %s", addr)
        return CuriousProtocol()

    def clientConnectionLost(self, connector, reason):
        logging.info("client connection lost - reason: %s", reason)

    def clientConnectionFailed(self, connector, reason):
        logging.error("client connection failed - reason: %s", reason)


def run_client():
    reactor.connectTCP(config.SERVER_HOST, config.SERVER_PORT,
                       CuriousClientFactory())
    reactor.run()


if __name__ == "__main__":
    common.setup_logging("talk_twisted_client", level=logging.DEBUG)
    run_client()
