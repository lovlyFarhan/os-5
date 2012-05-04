
#manually defined Enum for readability
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError



#process will have working state
State = Enum(["RUNNING", "BLOCKED", "READY", "STOPPED", "FINISHED"])

#and priority
Priority = Enum(["HIGH", "MEDIUM", "LOW"])
