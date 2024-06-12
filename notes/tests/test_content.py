from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    """Тест контента."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых объектов."""
        cls.author = User.objects.create(username="Дарт Вейдер")
        cls.reader = User.objects.create(username="R2D2")
        cls.notes = Note.objects.create(
            title="ttt", text="ttt", slug="ttt", author=cls.author
        )

    def test_note_not_in_list_for_another_user(self):
        """В список заметок одного пользователя не попадают
        заметки другого пользователя
        """
        self.client.force_login(self.reader)
        url = reverse("notes:list")
        response = self.client.get(url)
        object_list = response.context["object_list"]
        assert self.notes not in object_list

    def test_note_in_list_for_author(self):
        """Отдельная заметка передаётся на страницу со списком заметок"""
        self.client.force_login(self.author)
        url = reverse("notes:list")
        response = self.client.get(url)
        object_list = response.context["object_list"]
        # Проверяем, что заметка есть  в контексте страницы:
        assert self.notes in object_list

    def test_create_and_edit_note_page_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы"""
        self.client.force_login(self.author)
        urls = (
            ("notes:add", None),
            ("notes:edit", (self.notes.slug,)),
        )
        for name, args in urls:
            response = self.client.get(self)
            url = reverse(name, args=args)
            response = self.client.get(url)
            self.assertIn("form", response.context)
            self.assertIsInstance(response.context["form"], NoteForm)
