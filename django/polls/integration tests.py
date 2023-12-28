import datetime

from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .choice_commentary import Commentator
from .models import Choice, Question
from .views import get_commentator_instance


class IntegrationalTests(TestCase):
    def test_listen_choices1(self):
        """
        Test runtime listen
        """
        commentator = get_commentator_instance()
        commentator.choices_listener = {1: 0}

        question = create_question_with_choices(
            question_text="Past question 1.", days=-30
        )
        choice_id = 1
        response = self.client.get(reverse("polls:results", args=(choice_id,)))

        self.assertEquals(1, commentator.choices_listener[1])

    def test_listen_choices2(self):
        """
        Test runtime listen with two choices
        """
        commentator = get_commentator_instance()
        commentator.choices_listener = {1: 0}

        question = create_question_with_choices(
            question_text="Past question 1.", days=-30
        )
        choice_id = 1
        response = self.client.get(reverse("polls:results", args=(choice_id,)))
        response = self.client.get(reverse("polls:results", args=(choice_id,)))
        response = self.client.get(reverse("polls:results", args=(choice_id,)))
        response = self.client.get(reverse("polls:results", args=(2,)))
        self.assertEquals(3, commentator.choices_listener[1])

    def test_seq_responses(self):
        """
        Test runtime listen with two choices
        """
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question_with_choices(
            question_text="Past question.", days=-30
        )
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

        url = reverse("polls:detail", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)

        response = self.client.get(reverse("polls:results", args=(1,)))
        self.assertEquals(200, response.status_code)
