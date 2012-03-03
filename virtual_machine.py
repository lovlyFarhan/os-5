

class VirtualMachine:
    def __init__(rm_memory):
        self.user_memory = rm_memory
        self.DS = "00"
        self.CS = "64"
        self.SS = "160"
        self.IP = self.CS
        self.SP = self.SS
