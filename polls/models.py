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
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    Represents a tag for a poll question.
    """
    tag_text = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_text


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
    trend_score = models.FloatField(default=0.0, null=False, blank=False)
    tags = models.ManyToManyField(Tag, blank=True)

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
        """Return time till ending of the poll"""
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
        """Retrieve up vote percentage from calculate_vote_percentage"""
        return self.calculate_vote_percentage()[0]

    @property
    def down_vote_percentage(self):
        """Retrieve down vote percentage from calculate_vote_percentage"""
        return self.calculate_vote_percentage()[1]

    @property
    def participants(self):
        """
        Calculate the number of participants based on the number of votes.
        """
        return self.vote_set.count()

    # ! Most of the code from https://stackoverflow.com/a/70869267
    def upvote(self, user):
        """create new SentimentVote object that represent upvote (vote_types=True)
        return True if user change the vote or vote for the first time else return False
        """
        try:
            self.sentimentvote_set.create(user=user, question=self, vote_types=True)
            self.save()
        except IntegrityError:
            vote = self.sentimentvote_set.filter(user=user)
            if vote[0].vote_types is False:
                vote.update(vote_types=True)
                self.save()
            else:
                return False
        return True

    def downvote(self, user):
        """create new SentimentVote object that represent downvote (vote_types=False)
        return True if user change the vote or vote for the first time else return False
        """
        try:
            self.sentimentvote_set.create(user=user, question=self, vote_types=False)
            self.save()
        except IntegrityError:
            vote = self.sentimentvote_set.filter(user=user)
            if vote[0].vote_types is True:
                vote.update(vote_types=False)
                self.save()
            else:
                return False
        return True

    @property
    def up_vote_count(self):
        """Count up vote of Question"""
        return self.sentimentvote_set.filter(question=self, vote_types=True).count()

    @property
    def down_vote_count(self):
        """Count down vote of Question"""
        return self.sentimentvote_set.filter(question=self, vote_types=False).count()

    def trending_score(self, up=None, down=None):
        """Return trend score base on the criteria below"""
        published_date_duration = timezone.now() - self.pub_date
        score = 0

        if (published_date_duration.seconds < 259200):  # Second unit
            score += 100
        elif (published_date_duration.seconds < 604800):
            score += 75
        elif (published_date_duration.seconds < 2592000):
            score += 50
        else:
            score += 25

        if (up is None) and (down is None):
            score += ((self.up_vote_count/5) - (self.down_vote_count/5)) * 100
        else:
            score += ((up/5) - (down/5)) * 100

        return score

    def get_tags(self, *args, **kwargs):
        return "-".join([tag.tag_text for tag in self.tags.all()])

    def save(self, *args, **kwargs):
        """Modify save method of Question object"""
        # to-be-added instance
        # * https://github.com/django/django/blob/866122690dbe233c054d06f6afbc2f3cc6aea2f2/django/db/models/base.py#L447
        if self._state.adding:
            try:
                self.trend_score = self.trending_score()
            except ValueError:
                self.trend_score = self.trending_score(up=0, down=0)
        super(Question, self).save(*args, **kwargs)


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
    """
    Represents a sentiment vote for a poll question.

    Attributes:
        user (User): The user who cast the sentiment vote.
        question (Question): The poll question for which the sentiment vote is cast.
        vote_types (bool): Indicates whether the sentiment vote is an upvote (True) or a downvote (False).

    Note:
        - When 'vote_types' is True, it represents an upvote or 'Like'.
        - When 'vote_types' is False, it represents a downvote or 'Dislike'.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote_types = models.BooleanField()

    class Meta:
        """
        unique_together (list of str): Ensures that a user can only cast one sentiment vote (upvote or downvote)
        for a specific question.
        """
        unique_together = ['user', 'question']
