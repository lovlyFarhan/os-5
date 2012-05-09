
from definitions import Priority
from process import Process
from definitions import State
from load import Load
#from jobGovernor import JobGovernor
from main import Main
from rm import RM


#class which manages all process, decides which should be running etc.
class ProcessPlaner():
    last_proc = None
    def __init__(self):
        self.procs = []
    #should pick process which are waiting for execution by highest priority
        
        
    def run_once(self):   
        if self.procs == []:
            self.procs = self.sort_by_priority()
            
        proc = self.procs.pop(0)
        while proc.state != State.READY:
            if self.procs == []:
                self.procs = self.sort_by_priority()
                
            proc = self.procs.pop(0)
            
        proc.state = State.RUNNING
        proc.run()
        ProcessPlaner.last_proc = proc        
            
            
    def run_cycle(self):
        for proc in self.procs:
            if proc.state == State.READY:
                proc.state = State.RUNNING
                proc.run()


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

