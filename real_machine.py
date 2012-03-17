
from virtual_machine import VirtualMachine


class Proccess():
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.commands = [line.rstrip('\n').replace('\\n', '\n')
                for line in file if line[0] != '#']


class RealMachine():
    def __init__(self):
        self.MAX_VMS = 2
        self.clear_mem()
        self.paging_table = []


    def clear_mem(self):
        self.memory = {i : "" for i in range(self.MAX_VMS * 256)}


    def get_new_page(self):
        if(self.paging_table == []):
            self.paging_table.append(0)
            return 0
        else:
            for i in range(max(self.paging_table) + 2):
                if i not in self.paging_table:
                    self.paging_table.append(i)
                    return i


    def fill_mem(self, proc):
        page = self.get_new_page() * 256
        DS = proc.commands[1:proc.commands.index("CODE")]
        CS = proc.commands[proc.commands.index("CODE") + 1:]
        DS_ptr = page
        CS_ptr = page + 64 

        for cmd, DR in zip(DS, range(DS.__len__())):
            if(cmd[0:2] == "DW"):
                self.memory[DS_ptr + DR] = int(cmd[3:])
            else:
                self.memory[DS_ptr + DR] = cmd[3:]
        
        for cmd, DR in zip(CS, range(CS.__len__())):
            self.memory[CS_ptr + DR] = cmd
        
        return page

    def start_vm(self, file_name):
        proc = Proccess(file_name)
        page = self.fill_mem(proc)
        self.vm = VirtualMachine(proc, page, self.memory)


    def remove_vm(self, vm_number):
        self.paging_table - vm_number


#from sys import argv
#rm = RealMachine()
#rm.start_vm(argv[1])
#rm.start_vm(argv[2])
#rm.start_vm(argv[3])
