# -*- coding: utf-8 -*-
from typing import Optional

from requests import Session


def fetch(query: str, intro: int, session: Session) -> str:
    with session.post(
        "https://yandex.ru/lab/api/yalm/text3",
        json={"query": query, "intro": intro, "filter": 1},
    ) as resp:
        r = resp.json()
    return f"{r['query']}{r['text']}"


def balaboba(
    query: str, *, intro: int = 0, session: Optional[Session] = None
) -> str:
    """Отправка запроса Яндекс Балабобе.

    Args:
        query (str): Текст для Балабобы.
        intro (int, optional): Вариант стилизации.
            0 - Без стиля. По умолчанию.
            1 - Теории заговора.
            2 - ТВ-репортажи.
            3 - Тосты.
            4 - Пацанские цитаты.
            5 - Рекламные слоганы.
            6 - Короткие истории.
            7 - Подписи в Instagram.
            8 - Короче, Википедия.
            9 - Синопсисы фильмов.
            10 - Гороскоп.
            11 - Народные мудрости.
            12 - Балабоба x Garage.
            18 - Новый Европейский Театр.
        session (Optional[Session], optional): По умолчанию None.

    Returns:
        str: Ответ Балабобы.
    """
    if session:
        return fetch(query, intro, session)
    with Session() as session:
        return fetch(query, intro, session)
