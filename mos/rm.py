

class RM():
    MAX_VMS = 16
    VM_SIZE = 256
    PPTR = MAX_VMS * VM_SIZE
    SI = None
    PI = None
    TI = None
    last_vm = None

    memory = {i : "" for i in range(MAX_VMS * VM_SIZE)}
    for i in range(MAX_VMS):
        memory[PPTR + i] = ""


    def get_new_page():
        empty_pos = -1
        paging_table = []
        for i in range(RM.MAX_VMS):
            page = RM.memory[RM.PPTR + i]
            if(page == "" and empty_pos == -1):
                empty_pos = RM.PPTR + i 
            elif(page != ""):
                paging_table.append(int(page))
        
        if(paging_table == []):
            RM.memory[empty_pos] = "0"
            return 0
        else:
            for i in range(max(paging_table) + 2):
                if i not in paging_table:
                    RM.memory[empty_pos] = str(i)
                    return i


