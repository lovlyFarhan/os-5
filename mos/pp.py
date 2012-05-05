
from definitions import Priority
from process import Process
from definitions import State
from load import Load
#from jobGovernor import JobGovernor
from main import Main

#class which manages all process, decides which should be running etc.
class ProcessPlaner():

    #should pick process which are waiting for execution by highest priority
    def start(self):
        true = True
        false = True
        Load()
        Load.filename = 'jobs/first.pr'
        Process.find_by_name("Load").run()
        #Main().run()
        Load.filename = 'jobs/second.pr'
        #Process.find_by_name("Main").run()
        true = 10
        while True:
            todo_list = self.sort_by_priority()
            for proc in todo_list:
                if proc.state == State.READY:
                    proc.run()
            if true == 0:
                Process.find_by_name("Load").state = State.READY
            #print(RM.memory)    
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


