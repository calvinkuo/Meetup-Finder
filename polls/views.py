from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from address.models import Address
from .models import Question, Comments
from .forms import CommentForm
import datetime

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def get_comments(request):
    addresses = Address.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return HttpResponseRedirect(reverse('polls:index'))
            # s = Comments(organizer = form.cleaned_data['organizer'], name_text=form.cleaned_data['name_text'], comment_text=form.cleaned_data['comment_text'], address = Address.objects.last())
            # s.save()
            # return render(request, 'polls/index.html', {'form': form, 'addresses' : addresses})
    else:
        form = CommentForm()

    return render(request, 'polls/comments.html', {'form': form, 'addresses' : addresses})


class CommentListView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'comment_list'

    def get_queryset(self):
        return Comments.objects.all()


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

