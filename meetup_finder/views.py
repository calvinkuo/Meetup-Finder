from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from address.models import Address
from .models import Question, Events, Response
from .forms import EventForm
import datetime

class IndexView(generic.ListView):
    template_name = 'meetup_finder/results.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Events
    template_name = 'meetup_finder/detail.html'
    context_object_name = 'event'
    def get_queryset(self):
        return Events.objects.all()

class ResultsView(generic.DetailView):
    model = Events
    template_name = 'meetup_finder/results.html'

def vote(request, event_id):
    event= get_object_or_404(Events, pk=event_id)
    try:
        selected_response = event.response_set.get(pk=request.POST['response'])
    except (KeyError, Response.DoesNotExist):
        # Redisplay the event voting form.
        return render(request, 'meetup_finder/detail.html', {
            'event': event,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_response.votes += 1
        selected_response.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('meetup_finder:detail', args=(event_id, )))

def get_events(request):
    addresses = Address.objects.all()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            post.response_set.create(response_text = 'Going', votes = 0)
            post.response_set.create(response_text = 'Not Going', votes = 0)
            post.response_set.create(response_text = 'Maybe', votes = 0)
            return HttpResponseRedirect(reverse('meetup_finder:index'))
            # s = Comments(organizer = form.cleaned_data['organizer'], name_text=form.cleaned_data['name_text'], comment_text=form.cleaned_data['comment_text'], address = Address.objects.last())
            # s.save()
            # return render(request, 'meetup_finder/index.html', {'form': form, 'addresses' : addresses})
    else:
        form = EventForm()

    return render(request, 'meetup_finder/registration.html', {'form': form, 'addresses' : addresses})


class EventListView(generic.ListView):
    template_name = 'meetup_finder/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return Events.objects.filter(event_date__gte = timezone.now())




def logout_view(request):
    logout(request)
    return HttpResponseRedirect('meetup_finder/account/logout/')