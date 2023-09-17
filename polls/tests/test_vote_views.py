from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .base import create_question
from ..models import Vote, Choice


class VoteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.question = create_question(question_text="Test Question", day=0)
        cls.choice1 = Choice.objects.create(question=cls.question, choice_text="Test Choice 1")
        cls.choice2 = Choice.objects.create(question=cls.question, choice_text="Test Choice 2")
        cls.user = User.objects.create_user(username="test_user_123", password="aaa123321aaa")
        cls.client = Client()

    def test_vote_with_valid_choice(self):
        """
        Test the vote view with a valid choice selection.
        """
        self.client.login(username=self.user.username, password="aaa123321aaa")

        response = self.client.post(reverse("polls:vote", args=(self.question.id,)),
                                    {'choice': self.choice1.id})

        self.assertRedirects(response, reverse("polls:results", args=(self.question.id,)))
        self.assertTrue(Vote.objects.filter(user=self.user, question=self.question).exists())

    def test_vote_with_invalid_choice(self):
        """
        Test the vote view with an invalid choice selection.
        """
        self.client.login(username=self.user.username, password="aaa123321aaa")

        response = self.client.post(reverse("polls:vote", args=(self.question.id,)),
                                    {'choice': 1000})

        self.assertRedirects(response, reverse('polls:detail', args=(self.question.id,)))

    def test_vote_without_login(self):
        """
        Test the vote view when the user is not logged in.
        """
        response = self.client.post(reverse("polls:vote", args=(self.question.id,)),
                                    {'choice': self.choice1})

        self.assertRedirects(response, "/accounts/login/?next=/polls/1/vote/")

    def test_vote_voting_not_allowed(self):
        """
        Test the vote view when voting is not allowed for the question.
        """
        self.client.login(username=self.user.username, password="aaa123321aaa")

        self.question_2 = create_question(question_text="Test not allow", day=10)
        self.choice_2 = Choice.objects.create(question=self.question_2, choice_text="Test Choice 2_2")

        response = self.client.post(reverse("polls:vote", args=(self.question_2.id,)), {"choice": self.choice_2.id})

        self.assertRedirects(response, reverse('polls:index'))

    def test_vote_with_no_post_data(self):
        """
        Test the vote view when vote with no post data.
        """
        self.client.login(username=self.user.username, password="aaa123321aaa")

        response = self.client.post(reverse("polls:vote", args=(self.question.id,)))

        self.assertRedirects(response, reverse('polls:detail', args=(self.question.id,)))

    def test_update_vote_when_vote_on_new_choice(self):
        """
        Test the vote when same user vote on same question but change the choice.
        """
        self.client.login(username=self.user.username, password="aaa123321aaa")

        response_1 = self.client.post(reverse("polls:vote", args=(self.question.id,)), {"choice": self.choice1.id})
        self.assertRedirects(response_1, reverse('polls:results', args=(self.question.id,)))

        response_2 = self.client.post(reverse("polls:vote", args=(self.question.id,)), {"choice": self.choice2.id})
        self.assertRedirects(response_2, reverse('polls:results', args=(self.question.id,)))

        self.assertFalse(Vote.objects.filter(user=self.user, question=self.question, choice=self.choice1).exists())
        self.assertTrue(Vote.objects.filter(user=self.user, question=self.question, choice=self.choice2).exists())
