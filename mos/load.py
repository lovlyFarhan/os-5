
from process import Process
from rm import RM
from definitions import Priority


#it should load user's program's instuction to virtual memory
class Load(Process):
    def __init__(self):
        Process.__init__(self, Priority.MEDIUM)


    def run(self, filename):
        file = open(filename, 'r')
        commands = [line.rstrip('\n').replace('\\n', '\n')
                for line in file if line[0] != '#']
        
        #vm will get this page number
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
        
        #vm will take it's page number from here
        RM.last_vm = vm_page


