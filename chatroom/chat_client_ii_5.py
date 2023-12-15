import asyncio
import aioconsole 

async def send_message(writer, message):
    writer.write(message.encode())
    await writer.drain()

async def handle_user_input(writer):
    while True:
        user_input = await aioconsole.ainput()
        await send_message(writer, user_input)

async def handle_server_messages(reader):
    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        print(message)

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 12345)

    
    pseudo = input("Entre ton pseudo : ")
    

    hello_message = f"Hello|{pseudo}"
    await send_message(writer, hello_message)

    input_task = asyncio.create_task(handle_user_input(writer))
    messages_task = asyncio.create_task(handle_server_messages(reader))

    await asyncio.gather(input_task, messages_task)

if __name__ == "__main__":
    asyncio.run(main())
