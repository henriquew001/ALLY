from django.shortcuts import render
from .models import Question, Choice, QuizResult
from .forms import QuizForm
from django.utils.translation import gettext as _
from collections import Counter

def quiz_view(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            counts = {1: 0, 2: 0, 3: 0}
            for field_name, choice_id in form.cleaned_data.items():
                choice = Choice.objects.get(id=choice_id)
                counts[choice.choice_number] += 1

            # Find the most common choice type
            most_common_choice_type = Counter(counts).most_common(1)[0][0]

            # Get the corresponding result
            try:
                if most_common_choice_type == 1:
                    best_match = QuizResult.objects.get(is_choice_1_result=True)
                elif most_common_choice_type == 2:
                    best_match = QuizResult.objects.get(is_choice_2_result=True)
                elif most_common_choice_type == 3:
                    best_match = QuizResult.objects.get(is_choice_3_result=True)
                else:
                    best_match = None
            except QuizResult.DoesNotExist:
                best_match = None

            if best_match:
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
