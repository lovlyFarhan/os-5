
from process import Process
from vm import VM

class JobGovernor(Process):

    def __init__(self):
        self.vm = VM()

    def run(self):
        self.vm.run()
        
