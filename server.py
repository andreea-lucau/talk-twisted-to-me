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

    def lineReceived(self, data):
        logging.debug("client data received: [%s]", data)
        self.transport.write(self.factory.knowledge_engine.getAnswer(data))
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
    logging.info("server execution ended")


if __name__ == "__main__":
    common.setup_logging("talk_twisted_server", level=logging.DEBUG)
    start_server()
