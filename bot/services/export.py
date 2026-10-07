import csv
import io
from collections.abc import Iterable, Mapping
from typing import Any


def csv_cell(value: Any) -> str:
    text = str(value)
    # Табличные программы не должны выполнять пользовательский текст как формулу.
    if text.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def tasks_to_csv(tasks: Iterable[Mapping]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    fields = ("id", "text", "user", "created_at")
    writer.writerow(fields)
    for task in tasks:
        writer.writerow([csv_cell(task[field]) for field in fields])
    # BOM помогает Excel правильно открыть русские буквы.
    return output.getvalue().encode("utf-8-sig")


def split_message(text: str, limit: int = 3500) -> list[str]:
    # Считаем UTF-16 единицы: эмодзи занимают две единицы в Telegram.
    chunks, current, size = [], [], 0
    for char in text:
        width = len(char.encode("utf-16-le")) // 2
        if size + width > limit:
            chunks.append("".join(current))
            current, size = [], 0
        current.append(char)
        size += width
    if current:
        chunks.append("".join(current))
    return chunks
