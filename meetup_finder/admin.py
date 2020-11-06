from django.contrib import admin

from .models import Choice, Question, Events, Response
from django.conf import settings

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


class ResponseInline(admin.TabularInline):
    model = Response


class EventsAdmin(admin.ModelAdmin):
    inlines = [ResponseInline]
    extra = 0


# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
admin.site.register(Events, EventsAdmin)
# admin.site.register(Response)
