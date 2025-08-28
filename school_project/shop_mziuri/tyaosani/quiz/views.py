from django.shortcuts import render
from .models import Question, Answer
from .forms import QuizForm
from django.utils.translation import get_language

def quiz_view(request):
    current_language = get_language()  # e.g., 'ka', 'en', 'ru'
    
    # Only show questions in the current language
    questions = Question.objects.filter(language=current_language)
    
    incorrect_answers = []
    correct_count = 0

    if request.method == "POST":
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            total_questions = questions.count()
            
            for question in questions:
                field_name = f'question_{question.id}'
                user_answer = form.cleaned_data.get(field_name)

                if question.question_type == 'choice':
                    correct_answer = Answer.objects.filter(question=question, is_correct=True).first()
                    selected_answer = Answer.objects.filter(id=user_answer).first()
                    
                    if correct_answer and str(correct_answer.id) == user_answer:
                        correct_count += 1
                    else:
                        incorrect_answers.append({
                            'question': question.text,
                            'your_answer': selected_answer.text if selected_answer else "No answer",
                            'correct_answer': correct_answer.text
                        })
                else:  # text answer
                    correct_answers = [ans.text.lower() for ans in Answer.objects.filter(question=question, is_correct=True)]
                    if user_answer.lower() in correct_answers:
                        correct_count += 1
                    else:
                        incorrect_answers.append({
                            'question': question.text,
                            'your_answer': user_answer,
                            'correct_answer': ', '.join(correct_answers)
                        })

            return render(request, 'quiz_result.html', {
                'score': correct_count,
                'total': total_questions,
                'incorrect_answers': incorrect_answers
            })
    else:
        form = QuizForm(questions=questions)

    return render(request, 'quiz.html', {'form': form})