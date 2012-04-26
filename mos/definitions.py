

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError



State = Enum(["RUNNING", "BLOCKED", "READY", "STOPPED", "FINISHED"])

Priority = Enum(["HIGH", "MEDIUM", "LOW"])
