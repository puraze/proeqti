from django import forms
from .models import Question, Answer

class QuizForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in Question.objects.all():
            if question.question_type == 'choice':
                choices = [(answer.id, answer.text) for answer in Answer.objects.filter(question=question)]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect
                )
            else:
                self.fields[f'question_{question.id}'] = forms.CharField(
                    label=question.text,
                    widget=forms.Textarea
                )
