# from takeoff_command import TakeoffCommand
from commands.fly_straight_command import FlyStraightCommand


class CommandFactory:
    def __init__(self):
        self._command_dict = {
            # TakeoffCommand.command_string: TakeoffCommand,
            FlyStraightCommand.command_string: FlyStraightCommand()
        }

    def get(self, name):
        return self._command_dict[name]
