from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Published date", {"fields": ["pub_date"], "classes": ["collapse"]}),
        ("End date", {"fields": ["end_date"], "classes": ["collapse"]}),
        ("Sentiment Vote count", {"fields": ["up_vote_count", "down_vote_count"]}),
        ("Participant count", {"fields": ["participant_count"]}),
    ]
    list_display = ["question_text", "pub_date", "end_date", "was_published_recently", "can_vote"]
    inlines = [ChoiceInline]
    list_filter = ["pub_date", ]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)
    