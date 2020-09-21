from abc import ABC, abstractmethod
from data_models.condition_result import ConditionResult
from typing import List
from data_models.data_row import DataRow


# Interface
class ICommand(ABC):

    def __init__(self):
        self.conditions = set()

    def add_condition(self, condition_func):
        self.conditions.add(condition_func)

    def add_all_conditions(self, conditions):
        if not isinstance(conditions, list):
            conditions = [conditions]
        for condition in conditions:
            self.conditions.add(condition)

    def check_all_conditions(self, window_frame: List[DataRow]) -> List[ConditionResult]:
        false_conditions = []
        for condition in self.conditions:
            condition_result = condition(window_frame)
            if not condition_result.status:
                false_conditions.append(condition_result)
        return false_conditions
