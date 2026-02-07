from data_store import DataStore
from commands import registry


class CommandProcessor:
    def __init__(self, store: DataStore):
        self.store = store
        self.registry = registry

    def process(self, command_str: str) -> str:
        parts = command_str.split()

        cmd_name = parts[0]
        args = parts[1:]

        command = self.registry.get(cmd_name.upper())

        if not command:
            return f"ERROR: unknown command '{cmd_name}'"

        if not command.validate_args(args):
            return f"ERROR: Invalid arguments for command {cmd_name.upper()}"

        return command.execute(args, self.store)
