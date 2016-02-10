"""Server"""
import logging

from twisted.internet import reactor, endpoints, protocol
from twisted.protocols import basic

import config
import common
import knowledge_engine


class KnowledgeProtocol(basic.LineReceiver):

    def connectionMade(self):
        logging.debug("client connected")
        self.transport.write(config.START_MESSAGE)

    def lineReceived(self, question):
        client_id, question = question.split(":")
        logging.debug("client %s send question: [%s]", client_id, question)
        defferedAnswer = self.factory.knowledge_engine.getAnswer(question)
        defferedAnswer.addCallback(self.sendAnswer, client_id)

    def sendAnswer(self, answer, client_id):
        logging.debug("sending answer to client %s: [%s]",
                      client_id, answer)
        self.transport.write(answer)
        self.transport.loseConnection()


class KnowledgeFactory(protocol.ServerFactory):
    protocol = KnowledgeProtocol
    knowledge_engine = knowledge_engine.KnowledgeEngine()


def start_server():
    factory = KnowledgeFactory()

    endpoints.serverFromString(
        reactor, "tcp:%s" % config.SERVER_PORT).listen(factory)

    logging.info("server started on port %d", config.SERVER_PORT)
    reactor.run()
    reactor.callLater(100, reactor.stop)
    logging.info("server execution ended")


if __name__ == "__main__":
    common.setup_logging("talk_twisted_server", level=logging.DEBUG)
    start_server()
