from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import SignUpForm
from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """View for index.html."""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
            """
            Return the last published questions that is published and haven't ended yet.
            """
            now = timezone.now()
            return Question.objects.filter(
                Q(pub_date__lte=now) & (Q(end_date__gte=now) | Q(end_date=None))
            ).order_by("-pub_date")


class DetailView(LoginRequiredMixin, generic.DetailView):
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

        user = self.request.user
        selected_choice = None
        has_voted = False

        if user.is_authenticated:
            try:
                vote = question.vote_set.get(user=user)
                selected_choice = vote.choice
                has_voted = True
            except Vote.DoesNotExist:
                pass

        context["selected_choice"] = selected_choice
        context["has_voted"] = has_voted

        return context


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def render_to_response(self, context, **response_kwargs):
        return render(self.request, self.template_name, context)


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def vote(request, question_id):
    """
    A function that updates the database. Adds a vote count to the choice that the user votes for
    in a specific question_id.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "You didn't select a choice.")
        return render(request, "polls/detail.html", {"question": question})

    else:
        if question.can_vote():
            if request.method == "POST" and "vote-button" in request.POST:
                if Vote.objects.filter(user=request.user, question=question).exists():
                    old_vote = question.vote_set.get(user=request.user)
                    old_vote.choice = selected_choice
                    old_vote.save()

                    messages.success(request, "You vote successfully🥳")
                    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
                else:
                    messages.success(request, "You vote successfully🥳")
                    Vote.objects.create(choice=selected_choice, user=request.user, question=question).save()
                    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
            else:
                messages.error(request, "You cannot vote by typing the URL.")
                return render(request, "polls/detail.html", {"question": question})
        else:
            messages.error(request, "You can not vote on this question.")
            return HttpResponseRedirect(reverse("polls:index"))