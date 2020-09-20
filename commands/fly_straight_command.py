from commands.common.command_interface import ICommand
from data_models.condition_result import ConditionResult
from commands.common.common_checks import speed_bounds_check, speed_difference_check, same_speed_check


class FlyStraightCommand(ICommand):
    window_size = 10
    command_string = "fly_strait"
    SPEED_MAX_ALLOWED_DIFF = 10
    SPEED_LOWER_BOUND = 45
    SPEED_UPPER_BOUND = 120

    def __init__(self):
        self.add_condition(self.__speed_bounds_check)
        self.add_condition(self.__same_speed_check)
        self.add_condition(self.__speed_difference_check)

    def __speed_bounds_check(self, window_frame) -> ConditionResult:
        return speed_bounds_check(lower_bound=FlyStraightCommand.SPEED_LOWER_BOUND,
                                  upper_bound=FlyStraightCommand.SPEED_UPPER_BOUND,
                                  command_name=self.command_string,
                                  window_frame=window_frame)

    def __same_speed_check(self, window_frame) -> ConditionResult:
        return same_speed_check(window_frame=window_frame,
                                command_name=self.command_string)

    def __speed_difference_check(self, window_frame) -> ConditionResult:
        return speed_difference_check(window_frame=window_frame,
                                      command_name=self.command_string,
                                      max_diff=FlyStraightCommand.SPEED_MAX_ALLOWED_DIFF)