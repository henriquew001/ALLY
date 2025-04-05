from django.db import models

class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    choice_number = models.IntegerField(default=0)
    def __str__(self):
      return self.text

class QuizResult(models.Model):
    result_text = models.TextField()
    is_choice_1_result = models.BooleanField(default=False)
    is_choice_2_result = models.BooleanField(default=False)
    is_choice_3_result = models.BooleanField(default=False)

    def __str__(self):
        return self.result_text
