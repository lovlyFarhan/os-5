
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
    
    def kill_vm():
        RM.current_vm.state = State.ABORTED
        RM.current_vm = None
        RM.TI = 0


    def run(self):
        #wrong operation
        if(RM.PI == 1):
            print("wrong operation in ", RM.current_vm.PAGE)
            Interrupt.kill_vm()   
        #division by zero
        elif(RM.PI == 2):
            print("division by zero in ", RM.current_vm.PAGE)
            Interrupt.kill_vm()
        #error while loading user's program
        elif(RM.PI == 3):
            print("error while trying to load ", Load.filename)
        #success loading user's program
        elif(RM.PI == 4):
            Process.find_by_name("Main").state = State.READY
        #test
        elif(RM.PI == 5):
            Process.find_by_name("Load").state = State.READY
        #perhaps those two will be optional
        if(RM.SI == 1):
            RM.current_vm.state = State.BLOCKED
            Process.find_by_name("Output").state = State.READY
#            pass
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
            Interrupt.kill_vm()
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
                #vms.append(vms.pop(0))
                #make first ready
                if vms.__len__() > 1:
                    vms[1].state = State.READY
                else:
                    vms[0].state = State.READY
                #set timer for vm
                RM.TI = TIMER_PERIOD
                #turn on watchdog
                Process.find_by_name("Watchdog").state = State.READY
            else:
                #no need to use watchdog if there is no user's programs
                Process.find_by_name("Watchdog").state = State.BLOCKED

        #clear
        RM.PI = 0
        RM.SI = 0
        self.state = State.READY


