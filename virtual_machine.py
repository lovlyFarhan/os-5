
class VirtualMachine():
    def __init__(self, proc, page, rm_memory):
        self.PAGE = page
        self.DS = 0 + page
        self.CS = 64 + page
        self.SS = 160 + page
        self.IP = self.CS
        self.SP = self.SS
        self.memory = rm_memory #{i:rm_memory[i] for i in range(self.DS, self.DS + 256)}
        self.DR = ''
        self.exec_commands()


    def exec_commands(self):
        while(self.exec_command() != True):
            pass


    def exec_command(self):
        self.DR = self.memory[self.IP]
        self.IP += 1
        if (self.DR[:2] == 'DS'):
            self.SP += 1
            self.memory[self.SP] = self.memory[self.DS + int(self.DR[2:])]
        elif (self.DR[:2] == 'SD'):
            self.memory[self.DS + int(self.DR[2:])] = self.memory[self.SP] 
            self.SP -= 1
        elif (self.DR == 'ADD'):
            self.memory[self.SP - 1] = int(self.memory[self.SP - 1]) + int(self.memory[self.SP])
            self.SP -= 1
        elif (self.DR == 'SUB'):
            self.memory[self.SP - 1] = int(self.memory[self.SP - 1]) - int(self.memory[self.SP])
            self.SP -= 1
        elif (self.DR == 'MUL'):
            self.memory[self.SP - 1] = int(self.memory[self.SP - 1]) * int(self.memory[self.SP])
            self.SP -= 1
        elif (self.DR == 'DIV'):
            try:
                self.memory[self.SP - 1] = int(int(self.memory[self.SP - 1]) / int(self.memory[self.SP]))
            except ZeroDivisionError as zde:
                raise Exception("Division by zero")
            self.SP -= 1
        elif(self.DR == 'ECHO'):
            print(self.memory[self.SP], end="")
            self.SP -= 1 
        elif(self.DR == 'AND'):
            self.memory[self.SP - 1] = int(self.memory[self.SP - 1]) & int(self.memory[self.SP])
            self.SP -= 1
        elif(self.DR == 'OR'):
            self.memory[self.SP - 1] = int(self.memory[self.SP - 1]) | int(self.memory[self.SP])
            self.SP -= 1
        elif(self.DR == 'READ'):
            self.SP += 1
            self.memory[self.SP] = input()[:4]
        elif(self.DR == 'CMP'):
            if (int(self.memory[self.SP - 1]) == int(self.memory[self.SP])):
                self.memory[self.SP - 1] = 1
            elif (int(self.memory[self.SP - 1]) > int(self.memory[self.SP])):
                self.memory[self.SP - 1] = 0
            else:
                self.memory[self.SP - 1] = 2
            self.SP -= 1
        elif(self.DR == 'NEG'):
            self.memory[self.SP] = int(-self.memory[self.SP])
        elif(self.DR == 'NOT'):
            if(int(self.memory[self.SP]) == 0):
                self.memory[self.SP] = 1
            else:
                self.memory[self.SP] = 0
        elif(self.DR[:2] == 'JP'):
            self.IP = self.CS + int(self.DR[2:])
        elif(self.DR[:2] == 'JE'):
            if(self.memory[self.SP] == 1):
                self.IP = self.CS + int(self.DR[2:])
            self.SP -= 1
        elif(self.DR[:2] == 'JL'):
            if(self.memory[self.SP] == 0):
                self.IP = self.CS + int(self.DR[2:])
            self.SP -= 1
        elif(self.DR[:2] == 'JG'):
            if(self.memory[self.SP] == 2):
                self.IP = self.CS + int(self.DR[2:])
            self.SP -= 1
        elif(self.DR == "HALT"):
            return True
        return False


            
                          
