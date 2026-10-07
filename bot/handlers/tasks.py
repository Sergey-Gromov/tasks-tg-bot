"""Обработчики четырёх команд."""

import asyncio

from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import BufferedInputFile, Message

from bot.database import Database
from bot.services.export import split_message, tasks_to_csv

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Привет! Я храню общий список задач команды.\n\n"
        "/add текст задачи — добавить задачу\n"
        "/list — показать все задачи\n"
        "/list_csv — скачать CSV-файл\n\n"
        "Например: /add Подготовить отчёт к пятнице"
    )


@router.message(Command("add"))
async def add(message: Message, command: CommandObject, database: Database) -> None:
    text = (command.args or "").strip()
    if not text:
        await message.answer("Напишите задачу после команды: /add Подготовить отчёт")
        return
    if message.from_user:
        author = message.from_user
        user = f"@{author.username}" if author.username else f"{author.full_name} (id: {author.id})"
    else:
        user = message.sender_chat.title if message.sender_chat else "Неизвестный автор"
    # SQLite синхронный: выполняем его в потоке, чтобы не задерживать бота.
    task_id = await asyncio.to_thread(database.add_task, text, user)
    await message.answer(f"Задача №{task_id} добавлена.")


@router.message(Command("list"))
async def list_tasks(message: Message, database: Database) -> None:
    tasks = await asyncio.to_thread(database.list_tasks)
    if not tasks:
        await message.answer("Список пуст. Добавьте задачу: /add текст задачи")
        return
    text = "Общий список задач:\n\n" + "\n\n".join(
        f"№{task['id']}. {task['text']}\n"
        f"Автор: {task['user']}\nСоздана (UTC): {task['created_at']}"
        for task in tasks
    )
    for chunk in split_message(text):
        await message.answer(chunk)


@router.message(Command("list_csv"))
async def list_csv(message: Message, database: Database) -> None:
    tasks = await asyncio.to_thread(database.list_tasks)
    file = BufferedInputFile(tasks_to_csv(tasks), filename="tasks.csv")
    await message.answer_document(file, caption=f"Общий список задач: {len(tasks)}")
