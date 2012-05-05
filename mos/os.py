
from process import Process
from init import Init
from pp import ProcessPlaner

#to stop os we will trap INT signal(Ctrl+ Z)
import signal

def sig_handler(*args):
    print("shutting down Vata os", end="")
    exit()

signal.signal(signal.SIGINT, sig_handler)



#start os
if __name__ == '__main__':
    print("starting Vata os")
    Init()
    ProcessPlaner().start()



