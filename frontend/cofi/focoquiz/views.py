from django.shortcuts import render, redirect
from .models import Question, Choice, QuizResult
from .forms import QuizForm
from django.http import HttpResponse
from django.db.models import Count
from django.utils.translation import gettext as _

def quiz_view(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            counts = {1: 0, 2: 0, 3: 0}
            for field_name, choice_id in form.cleaned_data.items():
                choice = Choice.objects.get(id=choice_id)
                counts[choice.choice_number] += 1

            results = QuizResult.objects.all()

            best_match = None
            highest_score = -1

            for result in results:
                score = 0
                if result.choice_1_count != 0:
                    score = score + (counts[1] / result.choice_1_count)
                if result.choice_2_count != 0:
                    score = score + (counts[2] / result.choice_2_count)
                if result.choice_3_count != 0:
                    score = score + (counts[3] / result.choice_3_count)

                if score > highest_score:
                    highest_score = score
                    best_match = result

            if best_match is not None:
                return render(request, 'focoquiz/result.html', {'result': best_match.result_text})
            else:
                return render(request, 'focoquiz/error.html', {'error_message': _("No matching result found.")})

    else:
        # Ensure there are 10 questions
        if Question.objects.count() < 10:
            return render(request, 'focoquiz/error.html', {'error_message': _("There are still questions missing for the quiz.")})

        form = QuizForm()
        if len(form.fields) < 10:
            return render(request, 'focoquiz/error.html', {'error_message': _("There are still questions missing for the quiz.")})

    return render(request, 'focoquiz/quiz.html', {'form': form})
