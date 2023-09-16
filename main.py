import platform
from datetime import datetime
import logging

import aiohttp
import asyncio


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    return r
                logging.error(f"Error status: {resp.status} for {url}")
                return None
        except aiohttp.ClientConnectorError as err:
            logging.error(f"Connection error: {str(err)}")
            return None


async def get_exchange():
    result = await request('https://api.privatbank.ua/p24api/exchange_rates?date=01.09.2023')
    usd = None
    eur = None
    if result:
        for item in result["exchangeRate"]:
            if item["currency"] == "USD":
                usd = f"USD: sale: {item['saleRate']}, buy: {item['purchaseRate']}"
            elif item["currency"] == "EUR":
                eur = f"EUR: sale: {item['saleRate']}, buy: {item['purchaseRate']}"
        return usd, eur    
    return "Failed to retrieve data"


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(get_exchange())
    print(result)
