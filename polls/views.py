from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .choice_commentary import Commentator
from .models import Choice, Question

commentator_instance = Commentator()


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions.
        """
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


def results(request, choice_id):
    """
    Render result for a selected choice
    @param choice_id - id of a selected choice
    """
    selected_choice = get_object_or_404(Choice, pk=choice_id)
    question = selected_choice.question
    comment = commentator_instance.handle(request, choice_id)
    context = {"question": question, "comment": comment}
    return render(request, "polls/results.html", context)


def vote(request, question_id):
    """
    Render result for a current question
    @param question_id - id of a current question
    """
    question = get_object_or_404(Question, pk=question_id)
    choice_id = request.POST.get("choice")
    try:
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
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
        return HttpResponseRedirect(reverse("polls:results", args=(choice_id)))
