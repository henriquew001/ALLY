from django.contrib import admin
from .models import Question, Choice, QuizResult  # Import your models


class ChoiceInline(admin.TabularInline):  # Or StackedInline, if that's what you're using
    model = Choice
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['text']  # Example; adjust as needed

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['result_text', 'is_choice_1_result', 'is_choice_2_result', 'is_choice_3_result']
