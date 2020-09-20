from commands.common.command_interface import ICommand
from data_models.condition_result import ConditionResult
from commands.common.common_checks import speed_bounds_check, speed_difference_check, same_speed_check
from typing import List
from data_models.data_row import DataRow
from data_models.anomaly import Anomaly
from data_models.condition_result import ConditionResult


class TurnCommand(ICommand):
    window_size = 10
    command_string = "turn_"
    SPEED_MAX_ALLOWED_DIFF = 10
    SPEED_LOWER_BOUND = 45
    SPEED_UPPER_BOUND = 110

    def __init__(self, command):
        super().__init__()
        turn_degree = command.split(self.command_string)[1]
        mult_factor = 1 if turn_degree[0] == "+" else -1
        turn_degree = int(turn_degree) * mult_factor
        self.turn_degree = turn_degree
        self.add_condition(self.__speed_bounds_check)
        self.add_condition(self.__same_speed_check)
        self.add_condition(self.__speed_difference_check)

    def __speed_bounds_check(self, window_frame: List[DataRow]) -> ConditionResult:
        return speed_bounds_check(lower_bound=TurnCommand.SPEED_LOWER_BOUND,
                                  upper_bound=TurnCommand.SPEED_UPPER_BOUND,
                                  command_name=self.command_string,
                                  window_frame=window_frame)

    def __same_speed_check(self, window_frame: List[DataRow]) -> ConditionResult:
        return same_speed_check(window_frame=window_frame,
                                command_name=self.command_string)

    def __speed_difference_check(self, window_frame: List[DataRow]) -> ConditionResult:
        return speed_difference_check(window_frame=window_frame,
                                      command_name=self.command_string,
                                      max_diff=TurnCommand.SPEED_MAX_ALLOWED_DIFF)
