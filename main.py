"""Точка входа: python main.py."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from bot.config import load_config
from bot.database import Database
from bot.handlers import router
from bot.keyboards import commands


async def main() -> None:
    config = load_config()
    database = Database(config.database_path)
    await asyncio.to_thread(database.initialize)

    # Dispatcher передаёт database обработчикам по имени аргумента.
    dispatcher = Dispatcher(database=database)
    dispatcher.include_router(router)
    # VLESS-клиент предоставляет локальный SOCKS/HTTP-прокси для бота.
    session = AiohttpSession(proxy=config.proxy_url)
    async with Bot(token=config.token, session=session) as bot:
        await bot.set_my_commands(commands)
        await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
