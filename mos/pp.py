
from definitions import Priority
from process import Process
from definitions import State
from load import Load
#from jobGovernor import JobGovernor
from main import Main
from rm import RM


#class which manages all process, decides which should be running etc.
class ProcessPlaner():

    #should pick process which are waiting for execution by highest priority
    def start(self):
        Load.filename = 'jobs/first.pr'
        true = 10
        while True:
            todo_list = self.sort_by_priority()
            for proc in todo_list:
                if proc.state == State.READY:
                    proc.state = State.RUNNING
                    proc.run()
            if true == 0:
                true = 10
                exec(input())
            true -= 1

    def sort_by_priority(self):
        hpl = []
        mpl = []
        lpl = []
        
        for proc in Process.list:
            if proc.priority == Priority.HIGH:
                hpl.append(proc)
            elif proc.priority == Priority.MEDIUM:
                mpl.append(proc)
            else:
                lpl.append(proc)

        sbpl = []
        sbpl.extend(hpl)
        sbpl.extend(mpl)
        sbpl.extend(lpl)
        
        return sbpl


