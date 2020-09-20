from commands.takeoff_command import TakeoffCommand
from commands.fly_straight_command import FlyStraightCommand
from commands.turn_command import TurnCommand
from commands.descent_command import DescentCommand


class CommandFactory:
    def __init__(self):
        self._non_parametric_command_dict = {
            TakeoffCommand.command_string: TakeoffCommand(),
            FlyStraightCommand.command_string: FlyStraightCommand()
        }
        self._parametric_command_dict = {
            TurnCommand.command_string: TurnCommand,
            DescentCommand.command_string: DescentCommand
        }

    def get(self, command_str):
        command = self._non_parametric_command_dict.get(command_str)
        if command:
            return command
        for k,v in self._parametric_command_dict.items():
            if command_str.startswith(k):
                return v(command_str)
        raise KeyError(command)

