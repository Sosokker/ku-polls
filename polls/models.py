"""
This module defines the models for the polls app.

It includes the Question and Choice models, which represent poll questions
and the choices associated with them. These models are used to store and
get poll data in the database.

Attributes:
    None
"""

from django.db import models, IntegrityError
from django.utils import timezone
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    Represents a tag for a poll question.
    """
    tag_text = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Represents a poll question.

    Attributes:
        question_text (str): The text of the poll question.
        pub_date (datetime): The date and time when the question was published.
        end_date (datetime): The date and time when the question will end.
        long_description (str): The long description of the poll question.
        short_description (str): The short description of the poll question.
        up_vote_count (int): The number of up votes the question has received.
        down_vote_count (int): The number of down votes the question has received.
        participant_count (int): The number of participants in the poll.
    """

    question_text = models.CharField(max_length=100)
    pub_date = models.DateTimeField("date published", default=timezone.now, editable=True)
    end_date = models.DateTimeField("date ended", null=True)
    short_description = models.CharField(max_length=200, default="Cool kids have polls")
    long_description = models.TextField(max_length=2000, default="No description provide for this poll.")
    tags = models.ManyToManyField(Tag, blank=True)

    up_vote_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2147483647)])
    down_vote_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2147483647)])
    participant_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2147483647)])

    def was_published_recently(self):
        """
        Checks if the question was published recently or not.

        Returns:
            bool: True if the question was published within the last day, else False.
        """
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        """
        Returns a string representation of the question.
        """
        return self.question_text

    def is_published(self):
        """
        Checks if the question is published or not.

        Returns:
            bool: True if the question is published, else False.
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """
        Checks if the question can be voted on or not.

        Returns:
            bool: True if the question is published and not ended, else False.
        """
        now = timezone.now()
        if self.end_date is None:
            return self.pub_date <= now
        else:
            return self.pub_date <= now <= self.end_date

    def calculate_time_left(self):
        """
        Calculate the time left until the end date.

        Returns:
            str: A formatted string representing the time left.
        """
        if self.end_date is None:
            return "No end date"

        now = timezone.now()
        time_left = self.end_date - now

        days, seconds = divmod(time_left.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        time_left_str = ""
        if days > 0:
            time_left_str += f"{int(days)} Days "
        elif hours > 0:
            time_left_str += f"{int(hours)} Hours "
        elif minutes > 0:
            time_left_str += f"{int(minutes)} Mins "
        elif seconds > 0:
            time_left_str += f"{int(seconds)} Sec "

        return time_left_str.strip()

    @property
    def time_left(self):
        return self.calculate_time_left()

    def calculate_vote_percentage(self):
        """Calculate the percentage of up votes and down votes."""
        total_vote = self.up_vote_count + self.down_vote_count
        if total_vote == 0:
            return (0, 0)

        up_vote_percentage = self.up_vote_count / total_vote * 100
        down_vote_percentage = self.down_vote_count / total_vote * 100

        return (int(up_vote_percentage), int(down_vote_percentage))

    @property
    def up_vote_percentage(self):
        return self.calculate_vote_percentage()[0]

    @property
    def down_vote_percentage(self):
        return self.calculate_vote_percentage()[1]

    @property
    def participants(self):
        """
        Calculate the number of participants based on the number of votes.
        """
        return self.vote_set.count()

    # ! Most of the code from https://stackoverflow.com/a/70869267
    def upvote(self, user):
        try:
            self.sentimentvote_set.create(user=user, question=self, vote_types=True)
            self.up_vote_count += 1
            self.save()
        except IntegrityError:
            vote = self.sentimentvote_set.filter(user=user)
            if vote[0].vote_types == False:
                vote.update(vote_types=True)
                self.save()
            else:
                return 'already_upvoted'
        return 'ok'


    def downvote(self, user):
        try:
            self.sentimentvote_set.create(user=user, question=self, vote_types=False)
            self.up_vote_count += 1
            self.save()
        except IntegrityError:
            vote = self.sentimentvote_set.filter(user=user)
            if vote[0].vote_types == True:
                vote.update(vote_types=False)
                self.save()
            else:
                return 'already_downvoted'
        return 'ok'


class Choice(models.Model):
    """
    Represents a choice for a poll question.

    Attributes:
        question (Question): The poll question to which the choice belongs.
        choice_text (str): The text of the choice.
        votes (int): The number of votes the choice has received.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        return self.vote_set.count()

    def __str__(self):
        """
        Returns a string representation of the choice.
        """
        return f"{self.choice_text} get ({self.votes})"


class Vote(models.Model):
    """Represent Vote of User for a poll question."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} voted for {self.choice} in {self.question}"
    

# ! Most of the code from https://stackoverflow.com/a/70869267
class SentimentVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote_types = models.BooleanField()

    class Meta:
        unique_together = ['user', 'question']