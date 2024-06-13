from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.tests.base_class_data import BaseClassData

User = get_user_model()


class TestContent(BaseClassData):
    """Тест контента."""

    def test_note_not_in_list_for_another_user(self):
        """В список заметок одного пользователя не попадают
        заметки другого пользователя.
        """
        response = self.client_reader.get(self.url_list)
        object_list = response.context["object_list"]
        assert self.notes not in object_list

    def test_note_in_list_for_author(self):
        """Отдельная заметка передаётся на страницу со списком заметок."""
        response = self.client_author.get(self.url_list)
        object_list = response.context["object_list"]
        # Проверяем, что заметка есть  в контексте страницы:
        assert self.notes in object_list

    def test_create_and_edit_note_page_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        for urls in self.url_add_edit:
            with self.subTest(urls):
                response = self.client_author.get(self)
                response = self.client_author.get(urls)
                self.assertIn("form", response.context, f'На страницу {urls} не передается форма')
                self.assertIsInstance(response.context["form"], NoteForm, f'На страницу {urls} передается неверная форма')
