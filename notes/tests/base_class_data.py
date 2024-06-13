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
        cls.url_add_edit = (
            reverse("notes:add", args=None),
            reverse("notes:edit", args=(cls.notes.slug,)),
        )
        cls.url_add_edit = (
            ("notes:home", None),
            ("users:login", None),
            ("users:logout", None),
            ("users:signup", None),
        )
        cls.url_add_edit = (
            ("notes:detail", (self.notes.slug,)),
            ("notes:success", None),
            ("notes:add", None),
            ("notes:list", None),
            ("notes:edit", (self.notes.slug,)),
            ("notes:delete", (self.notes.slug,)),
        )
        cls.url_add_edit = (
            ("notes:success", None),
            ("notes:add", None),
            ("notes:list", None),
        )
        cls.url_add_edit = (
            ("notes:detail", (self.notes.slug,)),
            ("notes:edit", (self.notes.slug,)),
            ("notes:delete", (self.notes.slug,)),
        )

        cls.note_form = {
            "title": "New title",
            "text": "New text",
            "slug": "new-slug",
        }
