from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("upvote/<int:question_id>", views.up_down_vote, {'vote_type' : 'upvote'}, name="upvote"),
    path("downvote/<int:question_id>", views.up_down_vote, {'vote_type' : 'downvote'}, name="downvote"),
    path("search", views.search_poll, name="search_poll"),
]
