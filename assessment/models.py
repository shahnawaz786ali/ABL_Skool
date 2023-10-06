from django.db import models
from users.models import *

# Create your models here.
class Quiz(models.Model):
    name=models.CharField(max_length=150)
    topic=models.CharField(max_length=150)
    grade=models.CharField(max_length=100,default=0)
    no_of_question=models.IntegerField()
    time=models.IntegerField(help_text="duration of the quiz in minutes")
    required_score_to_pass=models.IntegerField(help_text="required score to pass in %")

    def __str__(self):
        return f"{self.name}-{self.topic}"
    
    def get_questions(self):
        return self.question_set.all()
    
    class Meta:
        verbose_name_plural='Quizes'

class Question(models.Model):
    text=models.CharField(max_length=500)
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text=models.CharField(max_length=500)
    correct=models.BooleanField(default=False)
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question-{self.question.text}, answer-{self.text}, correct-{self.correct}"
    
class Result(models.Model):
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    score=models.FloatField()
    rank = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)
    
    def save(self, *args, **kwargs):
        # Calculate and update the rank when saving a Result instance
        rank = Result.objects.filter(quiz=self.quiz, score__gt=self.score).count() + 1
        self.rank = rank
        super(Result, self).save(*args, **kwargs)

class Assessment(models.Model):
    username = models.CharField(max_length=100)
    camera_image = models.ImageField(upload_to='assessment_images/')
