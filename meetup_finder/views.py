from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.utils import timezone
# from django.contrib.auth.decorators import permission_required,user_passes_test
# from address.models import Address
from .models import Events, Response
from .forms import EventForm
# from django.contrib.auth.models import Permission


# class IndexView(generic.ListView):
#     template_name = 'meetup_finder/results.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         return Question.objects.filter(
#             pub_date__lte=timezone.now()
#         ).order_by('-pub_date')[:5]


# class DetailView(generic.DetailView):
#     model = Events
#     template_name = 'meetup_finder/detail.html'
#     context_object_name = 'event'
#
#     def get_queryset(self):
#         return Events.objects.all()


class EventListView(generic.ListView):
    template_name = 'meetup_finder/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return Events.objects.filter(event_date__gt=timezone.now())


# class ResultsView(generic.DetailView):
#     model = Events
#     template_name = 'meetup_finder/results.html'


@require_http_methods(["POST"])
def vote(request, event_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    event = get_object_or_404(Events, pk=event_id)
    try:
        selected_response = event.response_set.get(pk=request.POST['response'])
    except (KeyError, Response.DoesNotExist):
        # Redisplay the event voting form.
        return get_event_details(request, event_id, "You didn't select a choice.")
    else:
        selected_response.votes += 1
        selected_response.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('meetup_finder:detail', args=(event_id, )))


def get_events(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            if form.instance.is_past():
                form.add_error('event_date', 'This event is in the past.')
                form.add_error('event_time', 'This event is in the past.')
            else:
                form.instance.user = request.user
                post = form.save()
                post.response_set.create(response_text='Going', votes=0)
                post.response_set.create(response_text='Not Going', votes=0)
                post.response_set.create(response_text='Maybe', votes=0)
                return HttpResponseRedirect(reverse('meetup_finder:index'))
    else:
        form = EventForm()

    return render(request, 'meetup_finder/registration.html', {'form': form})


def get_event_details(request, pk, error_message=''):
    event = get_object_or_404(Events, pk=pk)
    return render(request, 'meetup_finder/detail.html', {
        'event': event,
        'can_delete': event.user == request.user or request.user.has_perm('meetup_finder.can_delete'),
        'error_message': error_message,
        'is_past': event.is_past(),
    })


@require_http_methods(["POST"])
def event_delete(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if event.user == request.user or request.user.has_perm('meetup_finder.can_delete'):
        event.delete()
        return HttpResponseRedirect(reverse('meetup_finder:index'))  # Redirect to the homepage.
    return HttpResponseForbidden()
