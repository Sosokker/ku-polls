from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.generic import TemplateView

from .models import Choice, Question


class HomeView(TemplateView):
    """
    Provide a view for Home page(first page).
    """

    template_name = 'polls/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_questions = Question.objects.all()
        #* Check if the question is published and can be voted. Then, sort by pub_date
        published_questions = [q for q in all_questions if q.is_published() and q.can_vote()]
        latest_published_questions = sorted(published_questions, key=lambda q: q.pub_date, reverse=True)[:5]

        context['latest_question_list'] = latest_published_questions
        context['total_open_polls'] = sum(1 for q in published_questions if q.end_date is None)
        context['total_polls'] = all_questions.count()
        return context


class IndexView(generic.ListView):
    """
    Provide a view for Index page that list all polls.
    """

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(generic.DetailView):
    """
    Provide a view for detail page, a detail for each poll contain poll question
    and poll choices.
    """

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """
    Provide a view for result page that show up when user submit on of the choices.
    """

    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """
    A function that update the database. Add vote count to choice that user vote
    in specific question_id.
    """

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    