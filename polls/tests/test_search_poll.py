from django.test import TestCase
from django.urls import reverse

from ..models import Question


class SearchPollTest(TestCase):
    """Test if user search with normal string. It must return same queryset as filter question objects"""
    def test_search_normal_poll(self):
        data_1 = {'q': 'what'}
        data_2 = {'q': 'prefer'}
        q_1 = 'what'
        q_2 = 'prefer'
        response_1 = self.client.get(reverse("polls:search_poll"), data_1)
        response_2 = self.client.get(reverse("polls:search_poll"), data_2)
        self.assertQuerysetEqual(response_1.context['results'], Question.objects.filter(question_text__icontains=q_1))
        self.assertQuerysetEqual(response_2.context['results'], Question.objects.filter(question_text__icontains=q_2))

    def test_search_with_empty(self):
        """Test if user search with empty string. It must return all question"""
        data = {'q': ''}
        response = self.client.get(reverse("polls:search_poll"), data)
        self.assertQuerysetEqual(response.context['results'], Question.objects.all())
