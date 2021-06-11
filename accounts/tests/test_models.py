from django.test import TestCase
from django.contrib.auth import get_user_model, login
from accounts.models import Token
from unittest.mock import patch

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_is_valid_with_email(self):
        user = User(email="a@b.com")
        user.full_clean()  # should not raise

    def test_email_is_primary_key(self):
        user = User(email="a@b.com")
        self.assertEqual(user.pk, "a@b.com")

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email="a@b.com")
        user.backend = ""
        request = self.client.request().wsgi_request
        login(request, user)  # should not raise


class TokenModelTest(TestCase):
    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email="a@b.com")
        token2 = Token.objects.create(email="a@b.com")
        self.assertNotEqual(token1.uid, token2.uid)

    def test_creates_token_associated_with_email(self):
        self.client.post("/accounts/send_login_email", data={"email": "a@b.com"})
        token = Token.objects.first()
        self.assertEqual(token.email, "a@b.com")

    @patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post("/accounts/send_login_email", data={"email": "a@b.com"})

        token = Token.objects.first()
        expected_url = f"http://testserver/accounts/login?token={token.uid}"
        (subject, body, from_mail, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)
