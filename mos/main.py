
from process import Process
from definitions import Priority
from jobGovernor import JobGovernor


class Main(Process):
    def __init__(self):
        Process.__init__(self, Priority.MEDIUM)


    def run(self):
         JobGovernor()

