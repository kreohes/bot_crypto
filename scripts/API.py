import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.coingecko.com/api/v3/coins/list') as resp:
            response = await resp.read()
            print(response)


asyncio.run(main())
