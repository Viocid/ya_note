from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.tests.base_class_data import BaseClassData

User = get_user_model()


class TestRoutes(BaseClassData):
    """Тест маршрутов."""

    def test_pages_availability(self):
        """Доступ страниц анонимному пользователю."""
        for url in self.url_anon:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        """Перенаправления анонимного пользователя."""
        login_url = reverse("users:login")
        for url in self.url_red_anon:
            with self.subTest(url=url):
                redirect_url = f"{login_url}?next={url}"
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_author_availability_for_edit_and_delete(self):
        """Авторизованный пользователь не может зайти на страницу.
        редактирования или удаления чужих записок.
        """
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for url in self.url_users:
                with self.subTest(user=user, url=url):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_availability_for_done_and_add(self):
        """Авторизованный пользователь может зайти на страницу.
        со списком заметок, добавления новой заметки.
        страница успешного добавления заметки.
        """
        user = self.reader
        for url in self.url_user:
            with self.subTest(user=user, url=url):
                response = self.client_reader.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
