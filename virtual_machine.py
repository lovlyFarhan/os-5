

class VirtualMachine:
    def __init__(self, proc, rm_memory):
        self.memory = rm_memory
        self.DS = "00"
        self.CS = "40"
        self.SS = "A0"
        self.IP = self.CS
        self.SP = self.SS
        
    def fill_mem(self, proc):
        for i in range(1,64):
            code = proc.commands.index('CODE')
            if i < len(proc.commands)and i < code:
                c = hex(i)[2:]
                self.memory[c] = proc.commands[i]
        for i in range(64,256):
            c = hex(i)[2:]
            if code < len(proc.commands):
                self.memory[c] = proc.commands[code]
                code += 1     
            else:
                self.memory[c] = ''
            
            
