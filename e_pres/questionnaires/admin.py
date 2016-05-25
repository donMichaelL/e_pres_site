from django.contrib import admin
from .models import PreparednessQuestionnaireQuestion, PreparednessQuestionnaireAnswer, EvaluationQuestionnaireQuestion, EvaluationQuestionnaireAnswer, EvaluationStudentsQuestionnaire, EvaluationStudentsQuestionnaireAnswer


class PreparednessQuestionnaireAnswerAdmin(admin.ModelAdmin):
    model = PreparednessQuestionnaireAnswer
    list_filter = ('building',)
    list_display = ['__unicode__', 'question', 'answer']

admin.site.register(PreparednessQuestionnaireQuestion)
admin.site.register(PreparednessQuestionnaireAnswer, PreparednessQuestionnaireAnswerAdmin)


class EvaluationQuestionnaireAnswerAdmin(admin.ModelAdmin):
    model = EvaluationQuestionnaireAnswer
    list_filter = ('experiment',)
    list_display = ['__unicode__', 'question', 'answer']

admin.site.register(EvaluationQuestionnaireQuestion)
admin.site.register(EvaluationQuestionnaireAnswer, EvaluationQuestionnaireAnswerAdmin)


class EvaluationStudentsQuestionnaireAnswerAdmin(admin.ModelAdmin):
        model = EvaluationStudentsQuestionnaireAnswer
        list_filter = ('experiment',)
        list_display = ['__unicode__', 'question', 'answer', 'ip']

admin.site.register(EvaluationStudentsQuestionnaire)
admin.site.register(EvaluationStudentsQuestionnaireAnswer, EvaluationStudentsQuestionnaireAnswerAdmin)
