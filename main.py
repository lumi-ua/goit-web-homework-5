import asyncio
import platform
from datetime import datetime, timedelta
import logging
import sys


import aiohttp



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


def get_date(days: int):
    date = datetime.now().date()
    result = (date - timedelta(days=days)).strftime("%d.%m.%Y")
    return result

async def get_exchange(days: int):

    base = 'https://api.privatbank.ua/p24api/exchange_rates?date='
    
    if days > 10:
        logging.warning("Sorry, the number should not exceed 10, keep today's exchange rate")
        days  = 0

    d = get_date(days)
    result = await request(base + d)

    usd = None
    eur = None
    if result:
        for item in result["exchangeRate"]:
            if item["currency"] == "USD":
                usd = f"USD: sale: {item['saleRate']}, buy: {item['purchaseRate']}"
            elif item["currency"] == "EUR":
                eur = f"EUR: sale: {item['saleRate']}, buy: {item['purchaseRate']}"
        return usd, eur, d
    return "Failed to retrieve data"


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <days>")
        sys.exit(1)

    try:
        days = int(sys.argv[1])  # Получаем количество дней из аргументов командной строки
    except ValueError:
        print("Invalid number of days.")
        sys.exit(1)

    if days < 1:
        print("Number of days must be greater than 0.")
        sys.exit(1)

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = asyncio.run(get_exchange(days))
    print(result)
