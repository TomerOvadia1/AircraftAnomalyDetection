from typing import List
from data_models.fault import Fault


class Anomaly:
    def __init__(self, name, description, fault_lst: List[Fault]):
        self.name = name
        self.info = description
        self.fault_lst = fault_lst

    @staticmethod
    def create_error_msg(func_name, fault):
        return f"{func_name} condition is unfulfilled: fault - {fault}"
