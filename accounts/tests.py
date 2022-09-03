from django.test import TestCase
from rest_framework.test import APITestCase
from accounts.models import Accounts
from rest_framework.authtoken.models import Token
from accounts.ModelSerializers import AccountSerializer
from rest_framework.test import APIClient, APITestCase


class UserModelTest(TestCase):
    @classmethod
    def testDataSeller(cls):
        cls.username = "Henrique"
        cls.password = "1234"
        cls.first_name = "Henrique"
        cls.last_name = "Ferreira"
        cls.is_seller = True
        cls.user = Accounts.objects.create_user(username = cls.username,password=cls.password, first_name=cls.first_name, last_name=cls.last_name, is_seller=cls.is_seller)
    def testDataNotSeller(cls):
        cls.username = "Henrique"
        cls.password = "1234"
        cls.first_name = "Henrique"
        cls.last_name = "Ferreira"
        cls.is_seller = False
        cls.user = Accounts.objects.create_user(username = cls.username,password=cls.password, first_name=cls.first_name, last_name=cls.last_name, is_seller=cls.is_seller)


class UsersViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super = Accounts.objects.create_superuser(username='super', password='1234', first_name='super', last_name='teste')
        cls.seller = Accounts.objects.create_user(username='usernormal', password='1234', first_name='user', last_name='normal', is_seller=True)
        cls.super_token = Token.objects.create(user=cls.super)
        cls.seller_token = Token.objects.create(user=cls.seller)
        cls.users = Accounts.objects.all()
        cls.client: APIClient

    def test_seller_login(self):
        response = self.client.post('/api/login/', {"username": self.seller.username,"password": '1234'})
        expected_response = {"token": self.seller_token.key}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_normal_login(self):
        response = self.client.post('/api/login/', {"username": self.seller.username,"password": '1234'})
        expected_response = {"token": self.seller_token.key}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_login_wrong_credentials(self):
        response = self.client.post('/api/login/', {"username": self.seller.username,"password": '12345'})
        expected_response = {"detail": "invalid username or password"}
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), expected_response)

    def test_update_user_is_active_status_without_token(self):
        response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
        expected_response = {"detail": "Authentication credentials were not provided."}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected_response)

    def test_update_user_is_active_status_with_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token 1' + self.super_token.key)
        response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
        expected_response = {"detail": "Invalid token."}
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), expected_response)


    def test_update_user_is_active_status_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.seller_token.key)
        response = self.client.patch('/api/accounts/2/management/', {"is_active": False})
        expected_response = {"detail": "You do not have permission to change is_active."}
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), expected_response)
