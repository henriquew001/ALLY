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
    choice_1_count = models.IntegerField(default=0)
    choice_2_count = models.IntegerField(default=0)
    choice_3_count = models.IntegerField(default=0)
    def __str__(self):
      return self.result_text
