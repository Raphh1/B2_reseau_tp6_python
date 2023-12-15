import asyncio
import aioconsole

async def async_input():
    while True:
        user_input = await aioconsole.ainput()
        writer.write(user_input.encode())
        await writer.drain()

async def async_receive():
    while True:
        data = await reader.read(1024)
        print(f"Received: {data.decode()}")

async def main():
    global reader, writer
    host = '127.0.0.1'
    port = 8888

    reader, writer = await asyncio.open_connection(host=host, port=port)

    # Run the two functions concurrently
    await asyncio.gather(async_input(), async_receive())

if __name__ == "__main__":
    asyncio.run(main())
