"""
This module defines the models for the polls app.

It includes the Question and Choice models, which represent poll questions
and the choices associated with them. These models are used to store and
get poll data in the database.

Attributes:
    None
"""

import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """
    Represents a poll question.

    Attributes:
        question_text (str): The text of the poll question.
        pub_date (datetime): The date and time when the question was published.
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField("date ended", null=True)

    def was_published_recently(self):
        """
        Checks if the question was published recently or not.

        Returns:
            bool: True if the question was published within the last day, else False.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

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
        return self.pub_date <= now <= self.end_date


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
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a string representation of the choice.
        """
        return self.choice_text
    