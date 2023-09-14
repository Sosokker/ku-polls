from django.utils import timezone
from django.contrib.auth.models import User

from ..models import Question, Vote, Choice


def create_question(question_text, day=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + timezone.timedelta(days=day)
    return Question.objects.create(question_text=question_text, pub_date=time)