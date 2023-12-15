import aiohttp
import aiofiles
import asyncio
import os
import sys

async def get_content(session, url):
    async with session.get(url) as response:
        return await response.text()

async def write_content(content, filename):
    async with aiofiles.open(filename, 'w', encoding='utf-8') as file:
        await file.write(content)

async def process_url(session, url):
    content = await get_content(session, url)
    filename = os.path.join('/tmp', 'web_' + url.replace('https://', '').replace('/', '_'))
    await write_content(content, filename)

async def main():

    if len(sys.argv) != 2:
        print("Usage: python web_sync_multiple_async.py <file_with_urls>")
        sys.exit(1)

    urls_filename = sys.argv[1]

    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(urls_filename, 'r') as file:
            urls = [line.strip() for line in await file.readlines()]

        tasks = [process_url(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
