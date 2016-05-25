from django.contrib import admin
from .models import PreparednessQuestionnaireQuestion, PreparednessQuestionnaireAnswer, EvaluationQuestionnaireQuestion, EvaluationQuestionnaireAnswer


class PreparednessQuestionnaireAnswerAdmin(admin.ModelAdmin):
    model = PreparednessQuestionnaireAnswer
    list_filter = ('building',)
    list_display = ['__unicode__', 'question', 'answer']


class EvaluationQuestionnaireAnswerAdmin(admin.ModelAdmin):
    model = EvaluationQuestionnaireAnswer
    list_filter = ('experiment',)
    list_display = ['__unicode__', 'question', 'answer']

admin.site.register(PreparednessQuestionnaireQuestion)
admin.site.register(PreparednessQuestionnaireAnswer, PreparednessQuestionnaireAnswerAdmin)

admin.site.register(EvaluationQuestionnaireQuestion)
admin.site.register(EvaluationQuestionnaireAnswer, EvaluationQuestionnaireAnswerAdmin)
