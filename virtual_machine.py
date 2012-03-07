class VirtualMachine():
    def __init__(self, proc, rm_memory):
        self.memory = rm_memory
        self.DS = 0
        self.CS = 64
        self.SS = 160
        self.IP = self.CS
        self.SP = self.SS
        self.fill_mem(proc)
        self.exec_commands()

    def fill_mem(self, proc):
        DS = proc.commands[1:proc.commands.index("CODE")]
        CS = proc.commands[proc.commands.index("CODE") + 1:]
        for cmd in DS:
            if(cmd[0:2] == "DW"):
                self.memory[self.DS] = int(cmd[2:])
            else:
                self.memory[self.DS] = cmd[3:]
            self.DS += 1
        for cmd in CS:
            self.memory[self.CS] = cmd
            self.CS += 1
        print(self.memory)
    def exec_commands(self):
        while(self.memory[self.IP] != "HALT"):
            cmd = self.memory[self.IP]
            self.IP += 1
            if (cmd[:2] == 'DS'):
                self.SP += 1
                self.memory[self.SP] = self.memory[int(cmd[2:])]
            elif (cmd[:2] == 'SD'):
                self.memory[cmd[2:]] = self.memory[self.SP] 
                self.SP -= 1
            elif (cmd == 'ADD'):
                self.memory[self.SP-1] = self.memory[self.SP-1] + self.memory[self.SP]
                self.SP -= 1
            elif (cmd == 'SUB'):
                self.memory[self.SP-1] = self.memory[self.SP-1] - self.memory[self.SP]
                self.SP -= 1
            elif (cmd == 'MUL'):
                self.memory[self.SP-1] = self.memory[self.SP-1] * self.memory[self.SP]
                self.SP -= 1
            elif (cmd == 'DIV'):
                self.memory[self.SP-1] = self.memory[self.SP-1] / self.memory[self.SP]
                self.SP -= 1
            elif(cmd == 'PUTS'):
                print(self.memory[self.SP].replace("\\n", "\n"), end="")
                self.SP -= 1 
            elif(cmd == 'PUTI'):
                print(self.memory[self.SP], end="")
                self.SP -= 1
            elif(cmd == 'AND'):
                self.memory[self.SP-1] = self.memory[self.SP-1] & self.memory[self.SP]
                self.SP -= 1
            elif(cmd == 'OR'):
                self.memory[self.SP-1] = self.memory[self.SP-1] | self.memory[self.SP]
                self.SP -= 1
            elif(cmd == 'READ'):
                self.memory[self.SP] = input()
            elif(cmd == 'CMP'):
                if (self.memory[self.SP-1] == self.memory[self.SP]):
                    self.memory[self.SP] = 1
                elif (self.memory[self.SP-1] > self.memory[self.SP]):
                    self.memory[self.SP] = 0
                else:
                    self.memory[self.SP] = 2
                self.SP -= 1
            elif(cmd == 'NEG'):
                self.memory[self.SP] = 0 - self.memory[self.SP]
            elif(cmd == 'NOT'):
                self.memory[self.SP] = not(self.memory[self.SP])
            elif(cmd[:2] == 'JP'):
                self.IP = 16 * cmd[-2:-1] + cmd[:3]
            elif(cmd[:2] == 'JE'):
                if(self.memory[self.SP] == 1):
                    self.IP = 16 * cmd[-2:-1] + cmd[:3]
                self.SP -= 1
            elif(cmd[:2] == 'JL'):
                if(self.memory[self.SP] == 0):
                    self.IP = 16 * cmd[-2:-1] + cmd[:3]
                self.SP -= 1
            elif(cmd[:2] == 'JG'):
                if(self.memory[self.SP] == 2):
                    self.IP = 16 * cmd[-2:-1] + cmd[:3]
                self.SP -= 1
            
                
                
                
            
                                   
                
                
