from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.forms import WARNING
from notes.models import Note
from pytils.translit import slugify

User = get_user_model()


class TestLogic(TestCase):
    """Тест контента."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых объектов."""
        cls.author = User.objects.create(username="Дарт Вейдер")
        cls.reader = User.objects.create(username="R2D2")
        cls.notes = Note.objects.create(
            title="ttt", text="ttt", slug="ttt", author=cls.author
        )
        cls.note_form = {
            "title": "New title",
            "text": "New text",
            "slug": "new-slug",
        }
        cls.url = reverse("notes:detail", args=(cls.notes.slug,))

    def test_anonymous_user_cant_create_note(self):
        """Анонимный пользователь не может создать заметку"""
        note_count_s = Note.objects.count()
        url = reverse("notes:add", None)
        self.client.post(url, data=self.note_form)
        note_count = Note.objects.count()
        self.assertEqual(note_count, note_count_s)

    def test_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку"""
        note_count_s = Note.objects.count()
        self.client.force_login(self.reader)
        url = reverse("notes:add", None)
        self.client.post(url, data=self.note_form)
        note_count = Note.objects.count()
        note_count_s += 1
        self.assertEqual(note_count, note_count_s)

    def test_not_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        note_count_s = Note.objects.count()
        url = reverse("notes:add", None)
        self.client.force_login(self.author)
        self.note_form["slug"] = self.notes.slug
        response = self.client.post(url, data=self.note_form)
        note_count = Note.objects.count()
        self.assertFormError(
            response, "form", "slug", errors=(self.notes.slug + WARNING)
        )
        self.assertEqual(note_count, note_count_s)

    def test_empty_slug(self):
        """Если при создании заметки не заполнен slug,
        то он формируется автоматически.
        """
        note_count_s = Note.objects.count()
        self.client.force_login(self.author)
        url = reverse("notes:add")
        self.note_form.pop("slug")
        response = self.client.post(url, data=self.note_form)
        self.assertRedirects(response, reverse("notes:success"))
        note_count_s += 1
        note_count = Note.objects.count()
        self.assertEqual(note_count, note_count_s)
        new_note = Note.objects.get(title="New title")
        expected_slug = slugify(self.note_form["title"])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        """Пользователь может и редактировать свои заметки"""
        self.client.force_login(self.author)
        url = reverse("notes:edit", args=(self.notes.slug,))
        response = self.client.post(url, self.note_form)
        self.assertRedirects(response, reverse("notes:success"))
        self.notes.refresh_from_db()
        self.assertEqual(self.notes.title, self.note_form["title"])
        self.assertEqual(self.notes.text, self.note_form["text"])
        self.assertEqual(self.notes.slug, self.note_form["slug"])

    def test_other_user_cant_edit_note(self):
        """Пользователь не может и редактировать чужие заметки"""
        self.client.force_login(self.reader)
        url = reverse("notes:edit", args=(self.notes.slug,))
        response = self.client.post(url, self.note_form)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(slug=self.notes.slug)
        self.assertEqual(self.notes.title, note_from_db.title)
        self.assertEqual(self.notes.text, note_from_db.text)
        self.assertEqual(self.notes.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        """Пользователь может и удалять свои заметки"""
        self.client.force_login(self.author)
        url = reverse("notes:delete", args=(self.notes.slug,))
        response = self.client.post(url)
        self.assertRedirects(response, reverse("notes:success"))
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        """Пользователь не может и удалять чужие заметки"""
        note_count_s = Note.objects.count()
        self.client.force_login(self.reader)
        url = reverse("notes:delete", args=(self.notes.slug,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), note_count_s)
