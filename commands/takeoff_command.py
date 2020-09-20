# from command import ICommand
# from data_models.condition_result import ConditionResult
# from data_models.anomaly import Anomaly
#
#
# class TakeoffCommand(ICommand):
#     window_size = 5
#     command_string = "takeoff"
#
#     def __init__(self):
#         self.add_condition(self.__speed_check)
#
#     def __speed_check(self, window_frame) -> ConditionResult:
#         if not 45 < window_frame[-1].airspeed_indicator_indicated_speed_kt < 100:
#             return ConditionResult.unfulfilled_result(Anomaly(name=TakeoffCommand.command_string,
#                                                               info=f"__speed_check condition is unfulfilled"))
#         return ConditionResult.fulfilled_result()
#
#     def __same_speed_check(self, window_frame) -> ConditionResult:
#         prev = None
#         for data_row in window_frame:
#             if not prev:
#                 prev = data_row
#                 continue
#             if not prev.airspeed_indicator_indicated_speed_kt != data_row.airspeed_indicator_indicated_speed_kt:
#                 return ConditionResult.unfulfilled_result(Anomaly(name=TakeoffCommand.command_string,
#                                                                   info=Anomaly.createErrorMsg(
#                                                                       func_name="__same_speed_check",
#                                                                       faulty_component="airspeed_indicator_indicated_speed_kt")))
#         return ConditionResult.fulfilled_result()
