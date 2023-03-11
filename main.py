import time

import asyncio
import aiohttp


async def get_ethusdt(session: aiohttp.ClientSession) -> float:
    """Запрос к binance api"""
    async with session.get('https://www.binance.com/api/v3/ticker/price?symbol=ETHUSDT') as response:
        binance_response = await response.json()
        return float(binance_response['price'])


async def get_max_change_in_percentage(start_price: float, max_price: float, min_price: float) -> float:
    max_change = (max_price / start_price - 1) * 100
    min_change = (start_price / min_price - 1) * 100
    return max(min_change, max_change)


async def check_ethusdt() -> None:
    """Проверка курса ETHUSDT за 60 минут"""
    async with aiohttp.ClientSession() as session:
        start_price = max_price = min_price = await get_ethusdt(session)
        timer = time.time()
        while True:

            current_price = await get_ethusdt(session)
            if min_price > current_price:
                min_price = current_price
            if max_price < current_price:
                max_price = current_price
            if (max_price / start_price > 1.01 or start_price / min_price > 1.01) and timer > 3600:
                print(f'Начальная цена - {start_price}\n'
                      f'Максимальная цена - {max_price}, минимальная цена - {min_price}'
                      f'Максимальное изменение -'
                      f' {await get_max_change_in_percentage(start_price, max_price, min_price)}')
                timer = 0


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(check_ethusdt())




