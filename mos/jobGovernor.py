
from definitions import State
from process import Process
from vm import VM
from rm import RM


#it should manage user's program
class JobGovernor(Process):

    def __init__(self, **args):
        Process.__init__(self, **args)
        #creates virtual machine's instance
        self.vm = VM()
   
    #possible complete redo!!!
    #starts executing user's program for some time
    def run(self):
        #sets timer for user's program
        RM.TI = 5
        #and runs it until time is up or program has finished executing
        while(RM.TI != 0 and self.state != State.FINISHED):
            if self.vm.state == State.FINISHED or self.vm.state == State.ABORTED:
                self.state = State.FINISHED
                break
            #executes one vm's command
            self.vm.run()
            #decreases timer
            RM.TI -= 1
        
