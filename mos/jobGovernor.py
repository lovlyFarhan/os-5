
from definitions import State
from process import Process
from vm import VM


#it should manage user's program
class JobGovernor(Process):

    def __init__(self):
        #creates virtual machine's instance
        self.vm = VM()
   
    #possible complete redo!!!
    #starts executing user's program for some time
    def run(self):
        #sets timer for user's program
        RM.TI = 5
        #and runs it until time is up or program has finished executing
        while((RM.TI != 0) or (vm.state != State.FINISHED)):
            #executes one vm's command
            self.vm.run()
            #decreases timer
            RM.TI -= 1
        
