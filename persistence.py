import os


class AOFHandler:
    def __init__(self, filepath: str = "appendonly.aof"):
        self._filepath = filepath
        self._file = None

    def open(self):
        self._file = open(self._filepath, "a")

    def close(self):
        if self._file:
            self._file.close()
            self._file = None

    def log(self, command_str: str):
        if self._file is not None:
            self._file.write(command_str + "\n")
            self._file.flush()

    def replay(self, processor) -> int:
        if not os.path.exists(self._filepath):
            return 0

        count = 0
        with open(self._filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    processor.process(line, from_aof=True)
                    count += 1

        return count
