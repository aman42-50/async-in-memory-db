from abc import ABC, abstractmethod
from typing import Dict


class Command(ABC):
    is_write: bool = False

    @abstractmethod
    def execute(self, args, store) -> str:
        pass

    @abstractmethod
    def validate_args(self, args) -> bool:
        pass


class CommandRegistry:
    def __init__(self):
        self._commands: Dict[str, Command] = {}

    def register(self, name: str, command: Command):
        self._commands[name.upper()] = command

    def get(self, name: str):
        return self._commands.get(name.upper())


# Supported Commands
class GetCommand(Command):
    def validate_args(self, args) -> bool:
        return len(args) == 1  # GET key

    def execute(self, args, store) -> str:
        key = args[0]
        value = store.get(key)

        if value is None:
            return "(nil)"
        return value


class SetCommand(Command):
    is_write = True

    def validate_args(self, args) -> bool:
        return len(args) == 2  # SET key value

    def execute(self, args, store) -> str:
        key, value = args
        store.set(key, value)
        return "OK"


class DelCommand(Command):
    is_write = True

    def validate_args(self, args) -> bool:
        return len(args) == 1  # DEL key

    def execute(self, args, store) -> str:
        key = args[0]
        success = store.delete(key)
        return "1" if success else "0"


class ExpireCommand(Command):
    is_write = True

    def validate_args(self, args) -> bool:
        return len(args) == 2 and args[1].isdigit()  # EXPIRE key seconds

    def execute(self, args, store) -> str:
        key, seconds = args
        success = store.expire(key, int(seconds))
        return "1" if success else "0"


class ExpireAtCommand(Command):
    is_write = True

    def validate_args(self, args) -> bool:
        if len(args) != 2:
            return False
        try:
            float(args[1])
            return True
        except ValueError:
            return False

    def execute(self, args, store) -> str:
        key, timestamp = args
        success = store.expire_at(key, float(timestamp))
        return "1" if success else "0"


class TTLCommand(Command):
    def validate_args(self, args) -> bool:
        return len(args) == 1  # TTL key

    def execute(self, args, store) -> str:
        key = args[0]
        return str(store.get_ttl(key))


# Register commands
registry = CommandRegistry()
registry.register("GET", GetCommand())
registry.register("SET", SetCommand())
registry.register("DEL", DelCommand())
registry.register("EXPIRE", ExpireCommand())
registry.register("EXPIREAT", ExpireAtCommand())
registry.register("TTL", TTLCommand())
