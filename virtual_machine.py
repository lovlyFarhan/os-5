class VirtualMachine():
    def __init__(self, proc, rm_memory):
        self.memory = rm_memory
        self.DS = "00"
        self.CS = "40"
        self.SS = "A0"
        self.IP = self.CS
        self.SP = self.SS
        self.fill_mem(proc)
        self.exec_commands()

    def fill_mem(self, proc):
        DS = proc.commands[1:proc.commands.index("CODE")]
        CS = proc.commands[proc.commands.index("CODE") + 1:]
        DS_counter = int(self.DS, 16)
        for cmd in DS:
            if(cmd[0:2] == "DW"):
                self.memory["%X" %DS_counter] = int(cmd[3:])
            else:
                self.memory["%X" %DS_counter] = cmd[3:]
            DS_counter += 1

        CS_counter = int(self.CS, 16)
        for cmd in CS:
            self.memory["%X" %CS_counter] = cmd
            CS_counter += 1

    def exec_commands(self):
        ip = int(self.IP, 16)
        sp = int(self.SP, 16)
        while(self.memory["%X" %ip] != "HALT"):
            cmd = self.memory["%X" %ip]
            ip += 1
            if (cmd[:2] == 'DS'):
                sp += 1
                self.memory["%X" %sp] = self.memory[cmd[3:]]
            if (cmd[:2] == 'SD'):
                self.memory[cmd[3:]] = self.memory["%X" %sp]
                sp -= 1
            if (cmd == 'ADD'):
                self.memory["%X" %(sp-1)] = self.memory["%X" %(sp-1)] + self.memory["%X" %sp]
                sp -= 1
            if (cmd == 'SUB'):
                self.memory["%X" %(sp-1)] = self.memory["%X" %(sp-1)] - self.memory["%X" %sp]
                sp -= 1
            if (cmd == 'MUL'):
                self.memory["%X" %(sp-1)] = self.memory["%X" %(sp-1)] * self.memory["%X" %sp]
                sp -= 1
            if (cmd == 'DIV'):
                self.memory["%X" %(sp-1)] = self.memory["%X" %(sp-1)] / self.memory["%X" %sp]
                sp -= 1
            if(cmd == 'PUTS'):
                print(self.memory["%X" %sp])
                sp -= 1 
            if(cmd == 'PUTI'):
                print(self.memory["%X" %sp])
                sp -= 1
            if(cmd == 'AND'):
                self.memory["%X" %(sp-1)] = self.memory["%X" %(sp-1)] & self.memory["%X" %sp]
                sp -= 1
            if(cmd == 'OR'):
                self.memory["%X" %(sp-1)] = self.memory["%X" %(sp-1)] | self.memory["%X" %sp]
                sp -= 1