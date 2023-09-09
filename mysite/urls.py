from django.contrib import admin
from django.urls import include, path

from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='polls:index'), name='home_redirect'),
    path("polls/", include("polls.urls")),
    path('admin/', admin.site.urls),
]
