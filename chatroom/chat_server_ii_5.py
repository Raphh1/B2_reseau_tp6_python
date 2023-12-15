import asyncio

CLIENTS = {}

async def send_message(writer, message):
    writer.write(message.encode())
    await writer.drain()

async def broadcast(message, sender_addr):
    sender_ip, sender_port = sender_addr
    sender_pseudo = CLIENTS[sender_addr]["pseudo"]
    formatted_message = f"{sender_pseudo} a dit : {message}"
    
    for addr, info in CLIENTS.items():
        if addr != sender_addr:
            writer = info["w"]
            await send_message(writer, formatted_message)

async def handle_client(reader, writer):
    print("New connection.")

    data = await reader.read(100)
    message = data.decode()
    if message.startswith("Hello|"):
        pseudo = message[len("Hello|"):]
        addr = writer.get_extra_info('peername')
        CLIENTS[addr] = {"r": reader, "w": writer, "pseudo": pseudo}
        print(f"{pseudo} a rejoint la chatroom.")

        
        await broadcast(f"{pseudo} a rejoint la chatroom.", addr)

    try:
        while True:
            data = await reader.read(100)
            message = data.decode()

            if not message:
                break

            print(f"{pseudo} a dit : {message}")

            
            await broadcast(message, addr)

    except asyncio.CancelledError:
        pass

    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Connexion fermé pour {pseudo}")

async def main():
    server_address = ('127.0.0.1', 12345)
    server = await asyncio.start_server(handle_client, *server_address)

    async with server:
        await server.serve_forever()

asyncio.run(main())
