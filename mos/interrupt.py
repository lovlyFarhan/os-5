
from process import Process
from rm import RM
from definitions import Priority


#it should spot interrupt as soon as occurs
class Interrupt(Process):
    def __init__(self):
        Process.__init__(self, Priority.HIGH)


    def run(self):
        #wrong operation
        if(RM.PI == 1):
            pass
        #division by zero
        elif(RM.PI == 2):
            pass
        #perhapse those three will be optional
        #puts
        elif(RM.SI == 1):
            pass
        #read
        elif(RM.SI == 2):
            pass
        #halt
        elif(RM.SI == 3):
            pass
        #watchdog
        elif(RM.SI == 4):
            pass
        #timer
        elif(RM.TI == 0):
            pass


