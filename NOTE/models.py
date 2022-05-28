import datetime

from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    note_datetime = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%d/%m/%y %H:%M:%S')
    active = 'a'
    delayed = 'd'
    executed = 'e'
    status_choices = [
        (active, 'Активно'),
        (delayed, 'Отложено'),
        (executed, 'Выполнено')
    ]
    message = models.TextField(default='', verbose_name='Текст:')
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Добавляем автора в статью.
    status = models.CharField(
        max_length=1,
        choices=status_choices,
        default=active,
    )
    important = models.BooleanField(default=False, verbose_name='Важно:')
    public = models.BooleanField(default=False, verbose_name='Публичная:')
    created_at = models.DateTimeField(note_datetime, verbose_name='Дата:')


    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
