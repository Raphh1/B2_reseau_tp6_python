import asyncio

async def send_message(writer, message):
    writer.write(message.encode())
    await writer.drain()

async def receive_messages(reader):
    while True:
        data = await reader.read(100)
        if not data:
            break
        print(data.decode())

async def user_input(writer):
    while True:
        message = input()
        await send_message(writer, message)

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 12345)

    try:
        # Saisie du pseudo
        pseudo = input("Entrez votre pseudo : ")
        await send_message(writer, f"Hello|{pseudo}")

        # Tâches asynchrones pour la saisie utilisateur et la réception de messages
        input_task = asyncio.create_task(user_input(writer))
        receive_task = asyncio.create_task(receive_messages(reader))

        # Attendre que l'une des tâches se termine
        await asyncio.gather(input_task, receive_task)

    except asyncio.CancelledError:
        pass

    finally:
        writer.close()
        await writer.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
