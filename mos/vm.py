
from definitions import State
from process import Process
from rm import RM
from io_channel import IOChannel


#virtual machine - runs user's program
class VM(Process):
    #all vms will be stored here
    list = []
    #Output = ""

    def rotate():
        VM.list.append(VM.list.pop(0))


    def get_active():
        active = []
        for proc in VM.list:
            if proc.state == State.BLOCKED or proc.state == State.READY:
                active.append(proc)

        return active


    def __init__(self, **args):
        Process.__init__(self, **args)
        VM.list.append(self)
        #page number
        self.PAGE = RM.last_vm
        self.LC = RM.last_vm_lc
        vm_addr = self.PAGE * RM.VM_SIZE
        #data segment adress
        self.DS = 0 + vm_addr
        #code segment adress
        self.CS = 64 + vm_addr
        #stack segment adress
        self.SS = 160 + vm_addr
        #instruction pointer
        self.IP = self.CS
        #stack pointer
        self.SP = self.SS


    #executing command of user's program
    def run(self):
        RM.current_vm = self
        DR = str(RM.memory[self.IP])
        self.IP += 1
        RM.TI -= 1
        self.LC -= 1
        
        if (DR[:2] == 'DS'):
            self.SP += 1
            RM.memory[self.SP] = RM.memory[self.DS + int(DR[2:])]
        elif (DR[:2] == 'SD'):
            RM.memory[self.DS + int(DR[2:])] = RM.memory[self.SP] 
            self.SP -= 1
        elif (DR == 'ADD'):
            RM.memory[self.SP - 1] = int(RM.memory[self.SP - 1]) + int(RM.memory[self.SP])
            self.SP -= 1
        elif (DR == 'SUB'):
            RM.memory[self.SP - 1] = int(RM.memory[self.SP - 1]) - int(RM.memory[self.SP])
            self.SP -= 1
        elif (DR == 'MUL'):
            RM.memory[self.SP - 1] = int(RM.memory[self.SP - 1]) * int(RM.memory[self.SP])
            self.SP -= 1
        elif (DR == 'DIV'):
            #if division by 0 - interrupt
            if int(RM.memory[self.SP]) == 0:
                RM.PI = 2
            else:
                RM.memory[self.SP - 1] = int(int(RM.memory[self.SP - 1]) / int(RM.memory[self.SP]))
            self.SP -= 1
        elif(DR == 'ECHO'):
            RM.SI = 1
            IOChannel.send_output(self, str(RM.memory[self.SP]))
            self.state = State.WAITING
            self.SP -= 1 
        elif(DR == 'AND'):
            RM.memory[self.SP - 1] = int(RM.memory[self.SP - 1]) & int(RM.memory[self.SP])
            self.SP -= 1
        elif(DR == 'OR'):
            RM.memory[self.SP - 1] = int(RM.memory[self.SP - 1]) | int(RM.memory[self.SP])
            self.SP -= 1
        elif(DR == 'READ'):
            RM.SI = 2
            IOChannel.send_input_request(self)
            self.state = State.WAITING
            self.SP += 1
        elif(DR == 'CMP'):
            if (int(RM.memory[self.SP - 1]) == int(RM.memory[self.SP])):
                RM.memory[self.SP - 1] = 1
            elif (int(RM.memory[self.SP - 1]) > int(RM.memory[self.SP])):
                RM.memory[self.SP - 1] = 0
            else:
                RM.memory[self.SP - 1] = 2
            self.SP -= 1
        elif(DR == 'NEG'):
            RM.memory[self.SP] = int(-RM.memory[self.SP])
        elif(DR == 'NOT'):
            if(int(RM.memory[self.SP]) == 0):
                RM.memory[self.SP] = 1
            else:
                RM.memory[self.SP] = 0
        elif(DR[:2] == 'JP'):
            self.IP = self.CS + int(DR[2:])
        elif(DR[:2] == 'JE'):
            if(RM.memory[self.SP] == 1):
                self.IP = self.CS + int(DR[2:])
            self.SP -= 1
        elif(DR[:2] == 'JL'):
            if(RM.memory[self.SP] == 0):
                self.IP = self.CS + int(DR[2:])
            self.SP -= 1
        elif(DR[:2] == 'JG'):
            if(RM.memory[self.SP] == 2):
                self.IP = self.CS + int(DR[2:])
            self.SP -= 1
        elif(DR == "HALT"):
            RM.SI = 3
        else:
            #wrong command
            RM.PI = 1

        if self.state != State.WAITING:
            self.state = State.READY
             

