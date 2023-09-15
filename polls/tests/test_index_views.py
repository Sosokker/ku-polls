from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from ..models import Question


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"]["all_poll"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = Question.objects.create(question_text="Past question.")
        question.pub_date = timezone.now() - timezone.timedelta(days=30)
        question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"]["all_poll"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        future_question = Question.objects.create(question_text="Future question.")
        future_question.pub_date = timezone.now() + timezone.timedelta(days=30)
        future_question.save()
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"]["all_poll"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        past_question = Question.objects.create(question_text="Past question.")
        past_question.pub_date = timezone.now() - timezone.timedelta(days=30)
        past_question.save()

        future_question = Question.objects.create(question_text="Future question.")
        future_question.pub_date = timezone.now() + timezone.timedelta(days=30)
        future_question.save()

        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"]["all_poll"],
            [past_question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = Question.objects.create(question_text="Past question 1.")
        question1.pub_date = timezone.now() - timezone.timedelta(days=30)
        question1.save()

        question2 = Question.objects.create(question_text="Past question 2.")
        question2.pub_date = timezone.now() - timezone.timedelta(days=5)
        question2.save()

        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"]["all_poll"],
            [question2, question1],
        )
