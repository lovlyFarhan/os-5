
from process import Process
from rm import RM
from definitions import Priority
from definitions import State
from definitions import TIMER_PERIOD
from vm import VM
from load import Load


#it should spot interrupt as soon as it occurs
class Interrupt(Process):
    def __init__(self):
        Process.__init__(self, state=State.READY, priority=Priority.HIGH)


    def run(self):
        #wrong operation
        if(RM.PI == 1):
            print("wrong operation in ", RM.current_vm.PAGE)
            RM.current_vm.state = State.ABORTED
            RM.current_vm = None
            RM.TI = 0
        #division by zero
        elif(RM.PI == 2):
            print("division by zero in ", RM.current_vm.PAGE)
            RM.current_vm.state = State.ABORTED
            RM.current_vm = None
            RM.TI = 0
        #error while loading user's program
        elif(RM.PI == 3):
            print("error while trying to load ", Load.filename)
        #success loading user's program
        elif(RM.PI == 4):
            Process.find_by_name("Main").state = State.READY
        #test
        elif(RM.PI == 5):
            Process.find_by_name("Load").state = State.READY
        #perhapse those two will be optional
        if(RM.SI == 1):
            pass
        #read
        elif(RM.SI == 2):
            pass
        #halt
        elif(RM.SI == 3):
            RM.current_vm.state = State.FINISHED
            RM.current_vm = None
            RM.TI = 0
        #watchdog
        elif(RM.SI == 4):
            RM.current_vm.state = State.ABORTED
            RM.current_vm = None
        #timer
        if(RM.TI == 0):
            #get all active vms
            vms = VM.get_active()
            #for vm in vms:
            #    print(vm, "   ", vm.PAGE)
            if vms != []:
                #this vm already worked
                vms[0].state = State.BLOCKED
                #rotate vms list
                VM.rotate()
                #set timer for vm
                #RM.current_vm = vms[0]
                #make first ready
                vms[0].state = State.READY
                RM.TI = TIMER_PERIOD
        #clear
        RM.PI = 0
        RM.SI = 0
        self.state = State.READY


