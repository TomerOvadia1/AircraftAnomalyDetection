class ConditionResult:
    def __init__(self, status, anomaly):
        self.status = status
        self.anomaly = anomaly

    @classmethod
    def unfulfilled_result(cls, anomaly):
        return cls(False, anomaly)

    @classmethod
    def fulfilled_result(cls):
        return cls(True, None)

    def is_fulfilled(self):
        return self.status
