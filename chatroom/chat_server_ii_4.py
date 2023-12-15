import asyncio

CLIENTS = {}

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        
        
        if addr not in CLIENTS:
            CLIENTS[addr] = {}
            CLIENTS[addr]["r"] = reader
            CLIENTS[addr]["w"] = writer

            print(f"Client {addr} connected.")

        try:
            while True:
                data = await reader.read(100)
                message = data.decode()
                if not message:
                    break

                print(f"Message received from {addr} : {message}")

                await self.broadcast(message, addr)

        except asyncio.CancelledError:
            pass
        finally:
            del CLIENTS[addr]
            writer.close()
            await writer.wait_closed()
            print(f"Client {addr} disconnected.")

    async def broadcast(self, message, sender_addr):
        for addr, client in CLIENTS.items():
            if addr != sender_addr:
                try:
                    client["w"].write(message.encode())
                    await client["w"].drain()
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
    chat_server = ChatServer('127.0.0.1', 12345)
    asyncio.run(chat_server.run_server())
