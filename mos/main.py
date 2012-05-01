
from process import Process
from definitions import Priority


class Main(Process):
    def __init__(self):
        Process.__init__(self, Priority.MEDIUM)


    def run(self):
        pass

