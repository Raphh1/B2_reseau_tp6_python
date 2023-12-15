import aiohttp
import aiofiles
import asyncio
import sys

async def get_content(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as err:
        print(f"Error getting content from {url}: {err}")
        sys.exit(1)

async def write_content(content, file_path):
    try:
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
            await file.write(content)
        print(f"Content written to {file_path}")
    except IOError as e:
        print(f"Error writing to {file_path}: {e}")
        sys.exit(1)

async def main():
    if len(sys.argv) != 2:
        print("Usage: python web_sync_async.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    content = await get_content(url)

    file_path = '/tmp/web_page'
    await write_content(content, file_path)

if __name__ == "__main__":
    asyncio.run(main())
