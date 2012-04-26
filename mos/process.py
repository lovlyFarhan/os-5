
from definitions import State
from definitions import Priority


class Process:
    list = []

    def __init__(self, priority):
        self.state = State.BLOCKED
        self.priority = priority
        self.id = Process.get_new_id()
        Process.list.append(self)


    def get_new_id():
        if Process.list == []:
            return 0
        else:
            return max([proc.id for proc in Process.list]) + 1


p1 = Process(Priority.LOW)
p2 = Process(Priority.HIGH)

print(p2.id)
