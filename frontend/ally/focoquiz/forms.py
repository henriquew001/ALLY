from django import forms
from .models import Choice, Question
from django.db.models import Q

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        questions = Question.objects.all()
        for question in questions:
            choices = Choice.objects.filter(question=question).order_by('choice_number')
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=[(choice.id, choice.text) for choice in choices],
                widget=forms.RadioSelect,
            )
