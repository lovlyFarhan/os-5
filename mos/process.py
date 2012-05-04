
from definitions import State
from definitions import Priority


#all processes will intherit this class
class Process:
    #here every process will be stored
    list = []

    def __init__(self, state=State.BLOCKED, priority=Priority.LOW):
        self.state = State.BLOCKED
        self.priority = priority
        #every process will have it own unique id
        self.id = Process.get_new_id()
        Process.list.append(self)


    def get_new_id():
        if Process.list == []:
            return 0
        else:
            return max([proc.id for proc in Process.list]) + 1


