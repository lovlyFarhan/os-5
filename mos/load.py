

from process import Process
from real_machine import RM


class Load(Process):
    def run(self, filename):
        file = open(filename, 'r')
        commands = [line.rstrip('\n').replace('\\n', '\n')
                for line in file if line[0] != '#']
    
        vm_page = RM.get_new_page()
        vm_addr = vm_page * RM.VM_SIZE
        DS = commands[1:commands.index("CODE")]
        CS = commands[commands.index("CODE") + 1:]
        DS_ptr = vm_addr
        CS_ptr = vm_addr + 64 

        for cmd, DR in zip(DS, range(DS.__len__())):
            if(cmd[0:2] == "DW"):
                RM.memory[DS_ptr + DR] = int(cmd[3:])
            else:
                RM.memory[DS_ptr + DR] = cmd[3:]
        
        for cmd, DR in zip(CS, range(CS.__len__())):
            RM.memory[CS_ptr + DR] = cmd
        
        RM.last_vm = vm_page



