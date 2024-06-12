# Generated by Django 3.2.15 on 2022-09-04 01:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Note",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="Значение по-умолчанию",
                        help_text="Дайте короткое название заметке",
                        max_length=100,
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Добавьте подробностей", verbose_name="Текст"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        help_text="Укажите адрес для страницы заметки. Используйте только латиницу, цифры, дефисы и знаки подчёркивания",
                        max_length=100,
                        unique=True,
                        verbose_name="Адрес для страницы с заметкой",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
