from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User

from .base import create_question
from ..views import up_down_vote

# ! https://stackoverflow.com/questions/24588520/testing-several-integrityerrors-in-the-same-django-unittest-test-case
# * https://stackoverflow.com/questions/44450533/difference-between-testcase-and-transactiontestcase-classes-in-django-test
class UpDownVoteViewTest(TransactionTestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.user = User.objects.create_user(username="test_user", password="12345abc")
        cls.q1 = create_question(question_text="test 1")
        cls.client = Client()

    def test_vote_up_once(self):
        self.client.login(username="test_user", password="12345abc")
        self.q1.upvote(self.user)
        self.assertFalse(self.q1.upvote(self.user))

    def test_vote_down_once(self):
        self.client.login(username="test_user", password="12345abc")
        self.q1.downvote(self.user)
        self.assertFalse(self.q1.downvote(self.user))

    def test_can_change_up_to_down(self):
        self.client.login(username="test_user", password="12345abc")
        self.q1.upvote(self.user)
        self.q1.downvote(self.user)
        count_up = self.q1.sentimentvote_set.filter(vote_types=True).count()
        count_down = self.q1.sentimentvote_set.filter(vote_types=False).count()
        self.assertEqual(count_up, 0)
        self.assertEqual(count_down, 1)

    def test_can_change_up_to_down(self):
        self.client.login(username="test_user", password="12345abc")
        self.q1.downvote(self.user)
        self.q1.upvote(self.user)
        count_up = self.q1.sentimentvote_set.filter(vote_types=True).count()
        count_down = self.q1.sentimentvote_set.filter(vote_types=False).count()
        self.assertEqual(count_up, 1)
        self.assertEqual(count_down, 0)