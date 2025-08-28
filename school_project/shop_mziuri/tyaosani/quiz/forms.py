from django import forms
from .models import Question, Answer

class QuizForm(forms.Form):
    """
    Dynamic quiz form that generates fields based on the given questions.
    """
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        if questions:
            for question in questions:
                field_name = f'question_{question.id}'
                if question.question_type == 'choice':
                    choices = [(answer.id, answer.text) for answer in question.answers.all()]
                    self.fields[field_name] = forms.ChoiceField(
                        label=question.text,
                        choices=choices,
                        widget=forms.RadioSelect,
                        required=True
                    )
                else:
                    self.fields[field_name] = forms.CharField(
                        label=question.text,
                        widget=forms.TextInput(attrs={'class': 'form-control'}),
                        required=True
                    )