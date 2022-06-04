from typing import Optional
from django.db.models import QuerySet
from django.db.models.query import QuerySet


def note_filter(
        queryset: QuerySet,
        importance: Optional[bool],
        publicity: Optional[bool],
        status: Optional[int]
                ):
    """
    Фильтрация по признакам:
    :param queryset:
    :param importance: важность True/False
    :param publicity: публичность заметки True/False
    :param status: статус заметки 1 - Активно, 2 - Отложено, 3 - Выполнено
    :return:
    """
    if importance or publicity or status:
        return queryset.filter(
            importance=importance,
            publicity=publicity,
            status=status
        )
    else:
        return queryset

