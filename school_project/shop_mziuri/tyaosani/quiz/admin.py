from django.contrib import admin
from .models import Question, Answer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'question_type', 'language')
    list_filter = ('language', 'question_type')
    search_fields = ('text',)

admin.site.register(Question, QuestionAdmin)