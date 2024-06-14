from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note
from notes.tests.base_class_data import BaseClassData
from pytils.translit import slugify

User = get_user_model()


class TestLogic(BaseClassData):
    """Тест логики."""

    def test_anonymous_user_cant_create_note(self):
        """Анонимный пользователь не может создать заметку"""
        note_count_s = Note.objects.count()
        self.client.post(self.url_add, data=self.note_form)
        note_count = Note.objects.count()
        self.assertEqual(note_count, note_count_s)

    def test_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку"""
        note_count_s = Note.objects.count()
        self.client_reader.post(self.url_add, data=self.note_form)
        note_from_db = Note.objects.get(slug=self.notes.slug)
        note_count = Note.objects.count()
        note_count_s += 1
        self.assertEqual(note_count, note_count_s)
        self.assertEqual(self.notes.title, note_from_db.title)
        self.assertEqual(self.notes.text, note_from_db.text)
        self.assertEqual(self.notes.slug, note_from_db.slug)
        self.assertEqual(self.notes.author, note_from_db.author)

    def test_not_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        note_count_s = Note.objects.count()
        self.note_form["slug"] = self.notes.slug
        response = self.client_author.post(self.url_add, data=self.note_form)
        note_count = Note.objects.count()
        self.assertEqual(note_count, note_count_s)
        self.assertFormError(
            response, "form", "slug", errors=(self.notes.slug + WARNING)
        )

    def test_empty_slug(self):
        """Если при создании заметки не заполнен slug,
        то он формируется автоматически.
        """
        Note.objects.all().delete()
        note_count_s = Note.objects.count()
        self.note_form.pop("slug")
        response = self.client_author.post(self.url_add, data=self.note_form)
        self.assertRedirects(response, reverse("notes:success"))
        note_count_s += 1
        note_count = Note.objects.count()
        self.assertEqual(note_count, note_count_s)
        new_note = Note.objects.get()
        expected_slug = slugify(self.note_form["title"])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        """Пользователь может и редактировать свои заметки"""
        response = self.client_author.post(self.url_edit, self.note_form)
        self.assertRedirects(response, reverse("notes:success"))
        self.notes.refresh_from_db()
        self.assertEqual(self.notes.title, self.note_form["title"])
        self.assertEqual(self.notes.text, self.note_form["text"])
        self.assertEqual(self.notes.slug, self.note_form["slug"])
        self.assertEqual(self.notes.author, self.author)

    def test_other_user_cant_edit_note(self):
        """Пользователь не может и редактировать чужие заметки"""
        response = self.client_reader.post(self.url_edit, self.note_form)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(slug=self.notes.slug)
        self.assertEqual(self.notes.title, note_from_db.title)
        self.assertEqual(self.notes.text, note_from_db.text)
        self.assertEqual(self.notes.slug, note_from_db.slug)
        self.assertEqual(self.notes.author, note_from_db.author)

    def test_author_can_delete_note(self):
        """Пользователь может и удалять свои заметки"""
        response = self.client_author.post(self.url_delete)
        self.assertRedirects(response, reverse("notes:success"))
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        """Пользователь не может и удалять чужие заметки"""
        note_count_s = Note.objects.count()
        response = self.client_reader.post(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), note_count_s)
