
from process import Process
from real_machine import RM


class VM(Process):
    def __init__(self, page):
        self.PAGE = page
        self.DS = 0 + page
        self.CS = 64 + page
        self.SS = 160 + page
        self.IP = self.CS
        self.SP = self.SS


    def exec_command(self):
        DR = str(RM.memory[self.IP])
        self.IP += 1

        #try:
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
            RM.memory[self.SP - 1] = int(int(RM.memory[self.SP - 1]) / int(RM.memory[self.SP]))
        elif (DR == 'DIV'):
            RM.memory[self.SP - 1] = int(int(RM.memory[self.SP - 1]) / int(RM.memory[self.SP]))
            self.SP -= 1
        elif(DR == 'ECHO'):
            vm_gui.outputBox.insertPlainText(str(RM.memory[self.SP]))
            self.SP -= 1 
        elif(DR == 'AND'):
            RM.memory[self.SP - 1] = int(RM.memory[self.SP - 1]) & int(RM.memory[self.SP])
            self.SP -= 1
        elif(DR == 'OR'):
            RM.memory[self.SP - 1] = int(RM.memory[self.SP - 1]) | int(RM.memory[self.SP])
            self.SP -= 1
        elif(DR == 'READ'):
            vm_gui.read_msg_box()
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
            return True
        #else:
                #vm_gui.msg_box_exception("Error: invalid command")
             
        #except ZeroDivisionError:
        #    vm_gui.msg_box_exception("Error: division by zero")

        #except Exception:
        #    vm_gui.msg_box_exception("Error: unknown error")

