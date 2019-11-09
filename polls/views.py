from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
# from django.template import loader

from .models import Choice, Question


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # template = loader.get_template('polls/index.html')
    context_object_name = 'latest_question_list'
    # return render(request, 'polls/index.html', context)

    def get_queryset(self):
        """ return last five published questions """
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    # question = get_object_or_404(Question, pk=question_id)
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    # question = get_object_or_404(Question, pk=question_id)
    # response = "You're looking at the results of question %s"
    # return HttpResponse(response % question_id)
    # return render(request, 'polls/results.html', {'question': question})
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did not select.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # redirect needed to prevent repost of form if user uses back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id)))
