
from process import Process
from rm import RM
from definitions import Priority


class Interrupt(Process):
    def __init__(self):
        Process.__init__(self, Priority.HIGH)


    def run(self):
        if(RM.PI == 1):
            pass
        elif(RM.PI == 2):
            pass
        elif(RM.SI == 1):
            pass
        elif(RM.SI == 2):
            pass
        elif(RM.SI == 3):
            pass
        elif(RM.SI == 4):
            pass
        elif(RM.TI == 0):
            pass


