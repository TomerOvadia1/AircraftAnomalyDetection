class Fault:
    def __init__(self, clock, fault_type):
        self.clock = clock
        self.fault_type = fault_type

    @classmethod
    def unknown(cls):
        return cls(clock=None, fault_type=None)

    @classmethod
    def is_unknown(cls, fault):
        return not fault.clock and not fault.fault_type
