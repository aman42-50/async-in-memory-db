import asyncio

from command_processor import CommandProcessor
from data_store import DataStore


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.store = DataStore()
        self.processor = CommandProcessor(self.store)

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info("peername")
        print("New Connection:", addr)
        try:
            while True:
                msg = await reader.read(1024)
                if not msg:
                    break

                command = msg.decode().strip()
                response = self.processor.process(command)
                writer.write((response + "\n").encode())
                await writer.drain()
        except Exception:
            pass
        finally:
            print("Disconnected:", addr)
            writer.close()
            await writer.wait_closed()

    async def start(self):
        server = await asyncio.start_server(
            self.handle_client, host=self.host, port=self.port
        )

        print(f"Async KV server running on {self.host}:{self.port}")

        async with server:
            await server.serve_forever()


async def main():
    server = Server("127.0.0.1", 9876)
    await server.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shut down")
