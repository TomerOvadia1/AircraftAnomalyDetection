class Anomaly:
    def __init__(self, name, info):
        self.name = name
        self.info = info

    @staticmethod
    def create_error_msg(func_name, fault):
        return f"{func_name} condition is unfulfilled: fault - {fault}"