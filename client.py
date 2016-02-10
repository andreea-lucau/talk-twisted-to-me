import logging
import sys

from twisted.internet import protocol, reactor, task
from twisted.protocols import basic

import common
import config

answers_received = 0
clients_no = 10


class CuriousProtocol(basic.LineReceiver):
    def dataReceived(self, data):
        logging.info("%s received data from server: [%s]",
                     self.client_id, data)
        if data == config.START_MESSAGE:
            question = "%s: what is the meaning of life?" % self.client_id
            logging.info("client %s will send question to server: [%s]",
                         self.client_id, question)
            self.transport.write("%s\r\n" % question)
        else:
            global answers_received
            answers_received += 1

        sys.stdout.write(data)

    def setId(self, client_id):
        self.client_id = client_id


class CuriousClientFactory(protocol.ClientFactory):
    def startedConnecting(self, connector):
        logging.info("starting client connection")

    def buildProtocol(self, addr):
        logging.info("client %s connected to %s", self.client_id, addr)
        client_protocol = CuriousProtocol()
        client_protocol.setId(self.client_id)
        return client_protocol

    def clientConnectionFailed(self, connector, reason):
        logging.error("client %s connection failed - reason: %s",
                      self.client_id, reason)

    def setId(self, client_id):
        self.client_id = client_id


def check_stop_client():
    global answers_received

    if answers_received == clients_no:
        logging.info("stopping client reactor")
        reactor.stop()


def run_client():
    clients = [None] * clients_no

    for i in range(clients_no):
        clients[i] = CuriousClientFactory()
        clients[i].setId(i)
        reactor.connectTCP(config.SERVER_HOST, config.SERVER_PORT,
                           clients[i])

    lc = task.LoopingCall(check_stop_client)
    lc.start(2)

    reactor.run()



if __name__ == "__main__":
    common.setup_logging("talk_twisted_client", level=logging.DEBUG)
    run_client()
