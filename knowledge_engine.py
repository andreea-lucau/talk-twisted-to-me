import random
import time

from twisted.internet import defer, reactor


class KnowledgeEngine():
    MIN_THINKING_TIME = 1
    MAX_THINKING_TIME = 10

    def __init__(self):
        pass

    def getAnswer(self, question):
        d = defer.Deferred()

        thinking_time = random.randint(self.MIN_THINKING_TIME,
                self.MAX_THINKING_TIME)
        reactor.callLater(thinking_time, d.callback, "42")

        return d
