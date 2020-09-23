from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


class SetUpTests(TestCase):
    def setUp(self):
        client = Client()
        john = User.objects.create_user(username="John", password="newpass1234")
        john.save()

class SigninViewTests(SetUpTests):
    def test_signin_template_rendered(self):
        """
        The page is rendered upon user request.
        """
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
