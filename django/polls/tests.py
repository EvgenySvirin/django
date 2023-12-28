import datetime

from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .choice_commentary import Commentator
from .models import Choice, Question
from .views import get_commentator_instance


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_question_with_choices(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text=question_text, pub_date=time)
    question.choice_set.create(choice_text="First choice", votes=0)
    question.choice_set.create(choice_text="Second choice", votes=0)
    return question


class IndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )


class DetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_404_question(self):
        """
        Tests no question
        """
        url = reverse("polls:detail", args=(1,))
        response = self.client.get(url)
        self.assertEquals(404, response.status_code)


class ResultsViewTests(TestCase):
    def test_200_choice(self):
        """
        Existing choice returns 200
        """
        question = create_question_with_choices(
            question_text="Past question 1.", days=-30
        )
        choice_id = 1
        response = self.client.get(reverse("polls:results", args=(choice_id,)))
        self.assertEquals(200, response.status_code)

    def test_404_choice(self):
        """
        Not existing choice returns 404
        """
        question = create_question_with_choices(
            question_text="Past question 1.", days=-30
        )
        choice_id = 3
        response = self.client.get(reverse("polls:results", args=(choice_id,)))
        self.assertEquals(404, response.status_code)

    def test_votes_count1(self):
        """
        One choice 1 time
        """
        question = create_question_with_choices(
            question_text="Past question 1.", days=-30
        )
        choice_id = 1
        response = self.client.get(reverse("polls:results", args=(choice_id,)))
        self.assertEquals(200, response.status_code)

    def test_votes_count2(self):
        """
        First choice 3 times
        Second choice 1 time
        """
        question = create_question_with_choices(
            question_text="Past question 1.", days=-30
        )
        choice_id = 1
        response = self.client.get(reverse("polls:results", args=(choice_id,)))
        response = self.client.get(reverse("polls:results", args=(choice_id,)))
        response = self.client.get(reverse("polls:results", args=(choice_id,)))
        choice_id = 2
        response = self.client.get(reverse("polls:results", args=(choice_id,)))

        choice1 = get_object_or_404(Choice, pk=1)
        choice2 = get_object_or_404(Choice, pk=2)
        self.assertEquals(3, choice1.votes)
        self.assertEquals(1, choice2.votes)
        self.assertEquals(200, response.status_code)


class CommentatorTests(TestCase):
    def test_comment(self):
        """
        Test one comment
        """

        def preach_bro(request):
            return "Preach bro, preach"

        comment_dict2 = {1: preach_bro}
        commentator = Commentator()
        commentator.comment_dict = comment_dict2

        self.assertEquals(preach_bro(None), commentator.handle(None, 1))
        self.assertEquals(None, commentator.handle(None, 2))
