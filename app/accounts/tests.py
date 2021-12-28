from django.test import TestCase, Client  #python library module for django unittests
from django.contrib.auth.models import User
from django.conf import settings

# Create your tests here.

#User Profile model test case
class ProfileTest(TestCase):

    def test_user_profile(self):
        newuser = User(username="burcak", email="burcak@email.com", password="burcak123")
        newuser.save()

        self.assertTrue(
            hasattr(newuser, 'profile')
        )

#User test cases
class UserTest(TestCase):

    client = Client()

    def setUp(self):
        newuser = User(username="Oguz", email="oguz@email.com", password="oguz123")
        newuser.save()

    def test_user(self):
        user_count = User.objects.all().count()
        print(user_count)
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_login_url(self):
        login_url = "/login/"
        data = {"username":"Oguz", "email":"oguz@email.com", "password":"oguz123"}
        response = self.client.post(login_url, data, follow=True)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_home_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)