
from virtual_machine import VirtualMachine


class Proccess():
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.commands = [line.rstrip('\n').replace('\\n', '\n')
                for line in file if line[0] != '#']

class RealMachine():
    def __init__(self):
        self.MAX_VMS = 4
        self.PPTR = self.MAX_VMS * 256
        self.clear_mem()


    def clear_mem(self):
        self.memory = {i : "" for i in range(self.MAX_VMS * 256)}
        for i in range(16):
            self.memory[self.PPTR + i] = ""


    def get_new_page(self):
        empty_pos = -1
        paging_table = []
        for i in range(self.MAX_VMS):
            page = self.memory[self.PPTR + i]
            if(page == "" and empty_pos == -1):
                empty_pos = self.PPTR + i 
            elif(page != ""):
                paging_table.append(int(page))
        print(paging_table) 
        if(paging_table == []):
            self.memory[empty_pos] = "0"
            return 0
        else:
            for i in range(max(paging_table) + 2):
                if i not in paging_table:
                    self.memory[empty_pos] = str(i)
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


    def remove_vm(self, page):
        for i in range(self.MAX_VMS):
            if(self.memory[self.PPTR + i] == str(page)):
                self.memory[self.PPTR + i] = ""
                return



#from sys import argv
#rm = RealMachine()
#try:
#    rm.start_vm(argv[1])
#except Exception as e:
#    print(e)
#rm.start_vm(argv[2])
#rm.start_vm(argv[3])
