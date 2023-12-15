import asyncio

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = set()

    async def handle_client(self, reader, writer):
        self.clients.add(writer)
        try:
            while True:
                data = await reader.read(100)
                message = data.decode()
                if not message:
                    break

                addr = writer.get_extra_info('peername')
                print(f"Message received from {addr} : {message}")

                # Broadcast the message to all clients
                await self.broadcast(message, writer)

        except asyncio.CancelledError:
            pass
        finally:
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast(self, message, sender):
        for client in self.clients:
            if client != sender:
                try:
                    client.write(message.encode())
                    await client.drain()
                except:
                    pass

    async def run_server(self):
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    chat_server = ChatServer('127.0.0.1', 15555)
    asyncio.run(chat_server.run_server())
