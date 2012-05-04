
from definitions import Priority
from process import Process
from definitions import State
from load import Load
from jobGovernor import JobGovernor

#class witch manages all process, decides which should be running etc.
class ProcessPlaner():

    #should pick process which are waiting for execution by highest priority
    def start(self):
        count = 1000
        true = True
        while count != 0:
            todo_list = self.sort_by_priority()
            for proc in todo_list:
                if proc.state == State.READY:
                    proc.run()
                if true and proc.__class__.__name__ == "Load":
                    proc.state = State.READY
                    true = False
                
                Load.filename = 'jobs/first.pr'
            if count == 995:
                JobGovernor(state=State.READY)
               
            count -= 1
        

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


