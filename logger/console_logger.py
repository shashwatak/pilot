from logger import Logger
from termcolor import colored


class ConsoleLogger(Logger):

    def log(self, state, prediction):
        print colored("[predicted]" + "\t\t\t\t" + "phi: " + self.to_str(prediction.values()[0]), 'red')

    """ Helpers """

    def to_str(self, f):
        return "%.2f" % f
