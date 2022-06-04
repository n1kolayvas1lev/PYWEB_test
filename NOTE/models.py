import datetime

from django.db import models
from django.contrib.auth.models import User


def deadline_date():
    deadline_datetime = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%d/%m/%y %H:%M:%S')
    return deadline_datetime


class Note(models.Model):
    active = 1
    delayed = 2
    executed = 3
    status_choices = [
        (active, 'Активно'),
        (delayed, 'Отложено'),
        (executed, 'Выполнено')
    ]
    message = models.TextField(
        default='',
        verbose_name='Текст:'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        editable=False,
    )
    status = models.SmallIntegerField(
        choices=status_choices,
        default=active,
    )
    important = models.BooleanField(
        default=False,
        verbose_name='Важно:'
    )
    public = models.BooleanField(
        default=False,
        verbose_name='Публичная:'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата:'
    )  # Дата создания
    deadline = models.DateTimeField(
        default=deadline_date(),
        verbose_name='Выполнить до:'
    )  # Дедлайн


    class Meta:
        verbose_name = 'заметка'
        verbose_name_plural = 'заметки'
