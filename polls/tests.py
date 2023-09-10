import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() should return False for questions whos pub_date is in the
        future.
        """
        future_date = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=future_date)
        self.assertIs(future_question.is_published(), False)

    def test_default_pub_date(self):
        """
        Questions with the default pub_date (now) are displayed on the index page.
        """
        question = Question.objects.create(question_text="Default pub date question.")

        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_is_published_with_past_question(self):
        """
        is_published() should return True for questions whose pub_date is in the
        past.
        """
        past_date = timezone.now() - datetime.timedelta(days=1)
        past_question = Question(pub_date=past_date)
        self.assertIs(past_question.is_published(), True)

    def test_can_vote_with_question_not_ended(self):
        """
        can_vote() should return True for questions that are published and have not
        ended.
        """
        pub_date = timezone.now() - datetime.timedelta(hours=1)
        end_date = timezone.now() + datetime.timedelta(hours=1)
        question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_with_question_ended(self):
        """
        can_vote() should return False for questions that are published but have
        ended.
        """
        pub_date = timezone.now() - datetime.timedelta(hours=2)
        end_date = timezone.now() - datetime.timedelta(hours=1)
        question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(question.can_vote(), False)

    def test_can_vote_with_question_no_end_date(self):
        """
        can_vote() should return True for questions that are published and have no
        specified end date.
        """
        pub_date = timezone.now() - datetime.timedelta(hours=1)
        question = Question(pub_date=pub_date, end_date=None)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_with_question_ending_in_future(self):
        """
        can_vote() should return True for questions that are published and
        the current time is within the allowed voting period.
        """
        pub_date = timezone.now() - datetime.timedelta(hours=1)
        end_date = timezone.now() + datetime.timedelta(hours=2)
        question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(question.can_vote(), True)


def create_question(self, question_text, days, pub_date=None):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + timezone.timedelta(days=days)
    if pub_date is not None:
        time = pub_date
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

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
            response.context["latest_question_list"],
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
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

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
            response.context["latest_question_list"],
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
            response.context["latest_question_list"],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = Question.objects.create(question_text="Future question.")
        future_question.pub_date = timezone.now() + timezone.timedelta(days=5)
        future_question.save()

        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = Question.objects.create(question_text="Past Question.")
        past_question.pub_date = timezone.now() - timezone.timedelta(days=5)
        past_question.save()

        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
