from unittest.mock import patch, call
from django.test import TestCase
import accounts.views


class SendLoginEmailViewTest(TestCase):
    @patch("accounts.views.send_mail")
    def test_send_email_to_address_from_post(self, mock_send_mail):
        self.client.post("/accounts/send_login_email", data={"email": "a@b.com"})

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, "Your login link for Superlists")
        self.assertEqual(from_email, "mailbot.mc@gmail")
        self.assertEqual(to_list, ["a@b.com"])

    def test_adds_success_message(self):
        response = self.client.post(
            "/accounts/send_login_email", data={"email": "a@b.com"}, follow=True
        )

        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Check your email, we've sent you a link you can use to log in.",
        )
        self.assertEqual(message.tags, "success")


@patch("accounts.views.auth")
class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.get("/accounts/login?token=abc123")
        self.assertRedirects(response, "/")

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get("/accounts/login?token=abc123")
        self.assertEqual(mock_auth.authenticate.call_args, call(uid="abc123"))

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get("/accounts/login?uid=abc123")
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value),
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get("/accounts/login?uid=abc123")
        self.assertEqual(mock_auth.login.called, False)
