from django.db import models

class Question(models.Model):
    QUESTION_TYPES = [
        ('choice', 'Multiple Choice'),
        ('text', 'Text Answer'),
    ]

    LANGUAGE_CHOICES = [
        ('ka', 'Georgian'),
        ('en', 'English'),
        ('ru', 'Russian'),
    ]
    
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ka')

    def __str__(self):
        return f"[{self.language}] {self.text}"


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"