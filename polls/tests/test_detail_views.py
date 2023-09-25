from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .base import create_question


class QuestionDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="test_user_123", password="aaa123321aaa")
        cls.client = Client()

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 not found(Redirect to Index).
        """
        future_question = create_question(question_text="Future question.", day=10)
        future_question.save()

        self.client.login(username=self.user.username, password="aaa123321aaa")

        url = reverse("polls:detail", args=(future_question.id,))
        respone = self.client.get(url)
        self.assertEqual(respone.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", day=-10)
        past_question.save()

        self.client.login(username=self.user.username, password='aaa123321aaa')

        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, past_question.question_text)
