from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy

from .forms import SignUpForm
from .models import Choice, Question


class IndexView(generic.ListView):
    """View for index.html."""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question = self.object

        context["question_text"] = question.question_text
        context["short_description"] = question.short_description
        context["long_description"] = question.long_description
        context["pub_date"] = question.pub_date
        context["end_date"] = question.end_date
        context["up_vote_count"] = question.up_vote_count
        context["down_vote_count"] = question.down_vote_count
        context["participant_count"] = question.participant_count

        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.object
        return context

    def render_to_response(self, context, **response_kwargs):
        return render(self.request, self.template_name, context)


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


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
