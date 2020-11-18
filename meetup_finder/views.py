from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Events, Response, EventComment
from .forms import EventForm, ProfileUpdateForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import UpdateView
import datetime


class EventListView(generic.ListView):
    template_name = 'meetup_finder/index.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return Events.objects.filter(event_date__gt=timezone.now())


def event_details(request, pk, error_message_vote='', error_message_comment=''):
    event = get_object_or_404(Events, pk=pk)
    return render(request, 'meetup_finder/detail.html', {
        'event': event,
        'can_delete': event.user == request.user or request.user.has_perm('meetup_finder.can_delete'),
        'error_message_vote': error_message_vote,
        'error_message_comment': error_message_comment,
        'is_past': event.is_past(),
    })


@login_required
def event_create(request):
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
                return HttpResponseRedirect(reverse('meetup_finder:detail', args=(post.pk, )))
        elif not form.data['geolocation']:
            form.add_error('address', 'Enter a valid address.')
    else:
        form = EventForm()

    return render(request, 'meetup_finder/registration.html', {'form': form})


@login_required
def event_update(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if event.user == request.user or request.user.has_perm('meetup_finder.can_delete'):
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                if form.instance.is_past():
                    form.add_error('event_date', 'This event is in the past.')
                    form.add_error('event_time', 'This event is in the past.')
                else:
                    post = EventForm(request.POST, request.FILES, instance=event).save()
                    form.instance.user = request.user
                    return HttpResponseRedirect(reverse('meetup_finder:detail', args=(post.pk, )))
            elif not form.data['geolocation']:
                form.add_error('address', 'Enter a valid address.')
        else:
            form = EventForm(instance=event)
        return render(request, 'meetup_finder/events_form.html', {'form': form})
    return HttpResponseForbidden()


@login_required
@require_http_methods(["POST"])
def event_delete(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if event.user == request.user or request.user.has_perm('meetup_finder.can_delete'):
        event.delete()
        return HttpResponseRedirect(reverse('meetup_finder:index'))  # Redirect to the homepage.
    return HttpResponseForbidden()


@login_required
def write_comment(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.name = request.user.profile.get_name()
            form.instance.event_id = event_id
            form.save()
        elif len(request.POST.get('comment_field', '').strip()) == 0:  # blank comment
            return event_details(request, event_id,
                                 error_message_comment="Please enter a comment.")
        else:  # too long or other error
            return event_details(request, event_id,
                                 error_message_comment="There was an error saving your comment. Please try again.")
    return HttpResponseRedirect(reverse('meetup_finder:detail', args=(event_id, )))


@login_required
def vote(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    if request.method == 'POST':
        try:
            selected_response = event.response_set.get(pk=request.POST['response'])
        except (KeyError, ValueError, Response.DoesNotExist):
            # Redisplay the form with an error.
            return event_details(request, event_id,
                                 error_message_vote="You didn't select a choice. Please try again.")
        else:
            selected_response.votes += 1
            selected_response.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('meetup_finder:detail', args=(event_id, )))


@login_required
def profile(request):
    context = {}

    if request.method == 'POST':
        context['p_form'] = ProfileUpdateForm(request.POST, request.FILES)
        if context['p_form'].is_valid():
            if context['p_form'].instance.birthday > datetime.date.today():
                context['p_form'].add_error('birthday', 'This date is in the future.')
            else:
                ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile).save()
                messages.success(request, f'Your account has been updated!')
                return HttpResponseRedirect(reverse('meetup_finder:profile'))
        context['show'] = True
    else:
        context['p_form'] = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'meetup_finder/profile.html', context)
