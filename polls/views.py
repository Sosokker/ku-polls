import logging
from typing import Any

from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import SignUpForm, PollSearchForm, PollCreateForm
from .models import Choice, Question, Vote


logger = logging.getLogger("django")


class IndexView(generic.ListView):
    """View for index.html."""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last published questions that is published and haven't ended yet.
        """
        now = timezone.now()
        all_poll_queryset = Question.objects.filter(
            Q(pub_date__lte=now) & ((Q(end_date__gte=now) | Q(end_date=None)))
        ).order_by("-pub_date")

        trend_poll_queryset = Question.objects.filter(
            Q(pub_date__lte=now) & ((Q(end_date__gte=now) | Q(end_date=None))) & Q(trend_score__gte=100)
        ).order_by("trend_score")[:3]

        queryset = {'all_poll': all_poll_queryset,
                    'trend_poll': trend_poll_queryset, }
        return queryset


class DetailView(LoginRequiredMixin, generic.DetailView):
    """
    Provide a view for detail page, a detail for each poll contain poll question
    and poll choices.
    """

    model = Question
    template_name = "polls/detail.html"

    def get(self, request, *args, **kwargs):
        """
        Overide get method, If user search poll that don't avaialable
        then, redirect to Index Page.
        """
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect("polls:index")

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        now = timezone.now()
        return Question.objects.filter(
            Q(pub_date__lte=now) & (Q(end_date__gte=now) | Q(end_date=None))
        ).order_by("-pub_date")

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
    """
    Provide a view for Result page, a Result for the poll contain poll participants
    number and other statistic such as up, down vote
    """
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user_voted = None
        question = self.get_object()
        if question.sentimentvote_set.filter(user=self.request.user, question=question, vote_types=True).exists():
            user_voted = 'upvote'
        elif question.sentimentvote_set.filter(user=self.request.user, question=question, vote_types=False).exists():
            user_voted = 'downvote'

        context['user_voted'] = user_voted
        return context


class SignUpView(generic.CreateView):
    """
    View that responsible for Sign Up page.
    """
    form_class = SignUpForm
    success_url = reverse_lazy('polls:index')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get("username"), form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid


@login_required
def vote(request, question_id):
    """
    A function that updates the database. Adds a vote count to the choice that the user votes for
    in a specific question_id.
    """
    ip = get_client_ip(request)
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            logger.error(f"User {request.user.username} ({ip}) didn't select choice.")
            messages.error(request, "You didn't select a choice.")
            return redirect("polls:detail", question_id)

        logger.info(f"User {request.user.username} ({ip}) select choice {selected_choice}")

        if question.can_vote():
            # ! Return 1. object element 2. boolean status of creation
            vote, created = Vote.objects.update_or_create(
                user=request.user,
                question=question,
                defaults={'choice': selected_choice}
            )

            if created:
                logger.info(f"User {request.user.username} ({ip}) vote on choice {selected_choice}")
                messages.success(request, "You voted successfully🥳")
            else:
                logger.info(f"User {request.user.username} ({ip}) update his answer to {selected_choice}")
                messages.success(request, "You updated your vote🥳")

            return redirect("polls:results", question_id)
        else:
            messages.error(request, "You cannot vote on this question.")
            return redirect("polls:index")
    else:
        messages.error(request, "Invalid request method.")
        return redirect("polls:index")


@login_required
def up_down_vote(request, question_id, vote_type):
    """
    A function that control the upvote and downvote request.
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        if vote_type == "upvote":
            if question.upvote(request.user):
                messages.success(request, "You upvoted this Poll😊")
        elif vote_type == "downvote":
            if question.downvote(request.user):
                messages.success(request, "You downvoted this Poll😭")

    return redirect(reverse("polls:results", args=(question_id,)))


# https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
def get_client_ip(request):
    """
    Use with logger to get ip of user.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def search_poll(request):
    """
    A function that handle the rendering of search result after user search with
    search bar.
    """
    form = PollSearchForm

    results = []
    q = ''
    now = timezone.now()
    if 'q' in request.GET:
        form = PollSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            # Case insensitive (icontains)
            results = Question.objects.filter(
                Q(question_text__icontains=q) & Q(pub_date__lte=now)
                & ((Q(end_date__gte=now) | Q(end_date=None)))
            )
    # * If user search with empty string then show every poll.
    if q == '':
        results = Question.objects.filter(
            Q(pub_date__lte=now) & ((Q(end_date__gte=now) | Q(end_date=None)))
        ).order_by("-pub_date")
    return render(request, 'polls/search.html', {'form': form, 'results': results, 'q': q})


@login_required
def create_poll(request):
    ip = get_client_ip(request)
    if request.method == 'POST':
        form = PollCreateForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            pub_date = form.cleaned_data['pub_date']
            end_date = form.cleaned_data['end_date']
            short_description = form.cleaned_data['short_description']
            long_description = form.cleaned_data.get('long_description', '')
            user_choices = form.cleaned_data['user_choice']
            tags = form.cleaned_data['tags']

            question = Question.objects.create(
                question_text=question_text,
                pub_date=pub_date,
                end_date=end_date,
                short_description=short_description,
                long_description=long_description,
            )

            choices = user_choices.split(',')  # Split with comma
            for choice_text in choices:
                Choice.objects.create(question=question, choice_text=choice_text.strip())

            # Add  tags to the question
            question.tags.set(tags)
            logger.info(f"User {request.user.username} ({ip}) create poll : {question_text}")
            return redirect('polls:index')

    else:
        form = PollCreateForm()

    return render(request, 'polls/creation.html', {'form': form})
