from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class BaseClassData(TestCase):
    """"""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых объектов."""
        cls.author = User.objects.create(username="Дарт Вейдер")
        cls.reader = User.objects.create(username="R2D2")
        cls.notes = Note.objects.create(
            title="ttt", text="ttt", slug="ttt", author=cls.author
        )

        cls.client_reader = cls.client_class()
        cls.client_reader.force_login(cls.reader)
        cls.client_author = cls.client_class()
        cls.client_author.force_login(cls.author)

        cls.url_list = reverse("notes:list")
        cls.url_detail = reverse("notes:detail", args=(cls.notes.slug,))
        cls.url_add = reverse("notes:add")
        cls.url_edit = reverse("notes:edit", args=(cls.notes.slug,))
        cls.url_delete = reverse("notes:delete", args=(cls.notes.slug,))
        cls.url_success = reverse("notes:success")
        cls.url_add_edit = (
            cls.url_add,
            cls.url_edit,
        )
        cls.url_anon = (
            reverse("notes:home", None),
            reverse("users:login", None),
            reverse("users:logout", None),
            reverse("users:signup", None),
        )
        cls.url_red_anon = (
            cls.url_detail,
            cls.url_success,
            cls.url_add,
            cls.url_list,
            cls.url_edit,
            cls.url_delete,
        )
        cls.url_user = (
            cls.url_success,
            cls.url_add,
            cls.url_list,
        )
        cls.url_users = (
            cls.url_detail,
            cls.url_edit,
            cls.url_delete,
        )

        cls.note_form = {
            "title": "New title",
            "text": "New text",
            "slug": "new-slug",
        }
