from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from NOTE.models import Note

URL = '/notes/'


class TestToDoViews(APITestCase):
    """
    - Автор видит конкретную свою запись любую +
    - Автор видит конкретную чужую публичную запись +
    - Автор не видит конкретную чужую непубличную запись +
    - Автор изменяет свою запись +
    - Автор не может изменить чужую запись (публичную, непубличная) +
    - Автор может удалить свою запись +
    - Автор не может удали чужую запись (публичную, непубличная) +
    """

    @classmethod
    def setUpTestData(cls):
        """
        Создание тестовой базы
        :return: None
        """
        test_user_1 = User(username="test_user_1", password="password1",)
        test_user_2 = User(username="test_user_2", password="password2",)
        test_user_1, test_user_2 = User.objects.bulk_create([test_user_1, test_user_2])

        note_1 = Note(message="note_1", author=test_user_1, status=1, important=True, public=True)
        note_2 = Note(message="note_2", author=test_user_1, status=2, important=False, public=False)
        note_3 = Note(message="note_3", author=test_user_2, status=3, important=True, public=False)
        note_4 = Note(message="note_4", author=test_user_2, status=1, important=False, public=True)
        note_1, note_2, note_3, note_4 = Note.objects.bulk_create([note_1, note_2, note_3, note_4])

    def test_get_personal_Note(self):
        """
        - Автор видит конкретную свою запись любую
        :return: None
        """
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(URL)
        queryset = Note.objects.filter(Q(author=user.id))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(queryset.count(), 2)

    def test_get_public_Note(self):
        """
        - Автор видит конкретную чужую публичную запись
        :return:None
        """
        user = User.objects.get(username='test_user_1')
        user2 = User.objects.get(username='test_user_2')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(URL)
        queryset = Note.objects.filter(Q(author=user2.id) & Q(public=True))
        print(queryset)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(queryset.count(), 1)

    def test_get_foreign_private_Note(self):
        """
        - Автор не видит конкретную чужую непубличную запись
        :return: None
        """
        pk = 3
        url = f'/notes/{pk}'
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_patch_own_Note(self):
        """
        - Автор изменяет свою запись
        :return:
        """
        pk = 1
        url = f'/notes/{pk}'
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'note': 'update note 1', 'important': False}
        response = client.patch(url, data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_patch_foreign_Note(self):
        """
        - Автор не может изменить чужую запись (публичную, непубличная)
        :return:
        """
        pk = 3
        url = f'/notes/{pk}'
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        data = {'note': 'update note 4'}
        response = client.patch(url, data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_foreign_Note(self):
        """
        - Автор не может удали чужую запись (публичную, непубличная)
        :return: None
        """
        pk = 3
        url = f'/notes/{pk}'
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_delete_own_Note(self):
        """
        - Автор может удалить свою запись
        :return: None
        """
        pk = 4
        url = f'/notes/{pk}'
        user = User.objects.get(username='test_user_1')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
