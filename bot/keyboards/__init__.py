"""Меню команд Telegram доступно через кнопку возле поля ввода."""

from aiogram.types import BotCommand

commands = [
    BotCommand(command="start", description="Приветствие и помощь"),
    BotCommand(command="add", description="Добавить: /add текст задачи"),
    BotCommand(command="list", description="Показать все задачи"),
    BotCommand(command="list_csv", description="Скачать задачи в CSV"),
]
