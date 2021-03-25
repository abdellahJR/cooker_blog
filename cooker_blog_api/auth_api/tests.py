from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from .models import User
from rest_framework import status
from rest_framework.test import RequestsClient


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.list_user_url = reverse('list-users')
        self.detail_user_url = reverse('detail-user', kwargs={'id': 1})
        self.refresh_token_url = reverse('token_refresh')
        self.fake = Faker()

        self.user_data = {
            'email': self.fake.email(),
            'username': self.fake.name(),
            'password': self.fake.password(),
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()



class TestUserViews(TestSetUp):

    def test_get_user_list(self):
        res = self.client.get(self.list_user_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_user(self):
        res = self.client.post(self.list_user_url, {'email': self.user_data['email'],'username': self.user_data['username']}, format="json")
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_get_user_detail(self):
        create_user_response = self.client.post(self.list_user_url, {'email': self.user_data['email'],'username': self.user_data['username']}, format="json")
        res = self.client.get(self.detail_user_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_update_user(self):
        create_user_response = self.client.post(self.list_user_url, {'email': self.user_data['email'],'username': self.user_data['username']}, format="json")
        res = self.client.put(self.detail_user_url,  {'email': self.user_data['email'],'username': self.fake.name()}, format="json")
        self.assertNotEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_delete_user(self):
        create_user_response = self.client.post(self.list_user_url, {'email': self.user_data['email'],'username': self.user_data['username']}, format="json")
        res = self.client.delete(self.detail_user_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)




class TestAuthViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_can_login_after_register(self):
        register = self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertIsNotNone(res.data['tokens']['access'])
        self.assertIsNotNone(res.data['tokens']['refresh'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_can_refresh_token(self):
        register_res = self.client.post(self.register_url, self.user_data, format="json")
        login_res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertIsNotNone(login_res.data['tokens']['access'])
        self.assertIsNotNone(login_res.data['tokens']['refresh'])
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        refresh_token_res = self.client.post(self.refresh_token_url, {'refresh':login_res.data['tokens']['refresh']}, format="json")
        self.assertIsNotNone(refresh_token_res.data['access'])
        self.assertEqual(refresh_token_res.status_code, status.HTTP_200_OK)
