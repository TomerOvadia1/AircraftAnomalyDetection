class Anomaly:
    def __init__(self, name, info):
        self.name = name
        self.info = info

    @staticmethod
    def createErrorMsg(func_name, faulty_component):
        return f"{func_name} condition is unfulfilled: faulty - {faulty_component}"