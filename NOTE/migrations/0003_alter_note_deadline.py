# Generated by Django 4.0.4 on 2022-06-04 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NOTE', '0002_alter_note_deadline_alter_note_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='deadline',
            field=models.DateTimeField(default='05/06/22 10:59:21', verbose_name='Выполнить до:'),
        ),
    ]
