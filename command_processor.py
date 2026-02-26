import time

from data_store import DataStore
from commands import registry


class CommandProcessor:
    def __init__(self, store: DataStore):
        self.store = store
        self.registry = registry
        self._aof_handler = None

    def set_aof_handler(self, handler):
        self._aof_handler = handler

    def process(self, command_str: str, from_aof: bool = False) -> str:
        parts = command_str.split()

        if not parts:
            return "ERROR: empty command"

        cmd_name = parts[0]
        args = parts[1:]

        command = self.registry.get(cmd_name.upper())

        if not command:
            return f"ERROR: unknown command '{cmd_name}'"

        if not command.validate_args(args):
            return f"ERROR: Invalid arguments for command {cmd_name.upper()}"

        result = command.execute(args, self.store)

        if (self._aof_handler
                and command.is_write
                and not from_aof
                and not result.startswith("ERROR")):
            if cmd_name.upper() == "EXPIRE":
                timestamp = time.time() + int(args[1])
                command_str = f"EXPIREAT {args[0]} {timestamp}"
            self._aof_handler.log(command_str)

        return result
