import asyncio
import aioconsole

async def async_input(writer):
    while True:
        try:
            user_input = await aioconsole.ainput()
            writer.write(user_input.encode())
            await writer.drain()
        except asyncio.CancelledError:
            break

async def async_receive(reader):
    while True:
        try:
            data = await reader.read(1024)
            print(f"Received: {data.decode()}")
        except asyncio.CancelledError:
            break

async def main():
    host = '127.0.0.1'
    port = 12345

    try:
        reader, writer = await asyncio.open_connection(host=host, port=port)

        # Run the two functions concurrently
        await asyncio.gather(async_input(writer), async_receive(reader))
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
