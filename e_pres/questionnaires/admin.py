from django.contrib import admin
from .models import EvaluationQuestionnaireQuestion, EvacuationQuestionnaire, EvacuationQuestionnaireAnswer


class EvacuationQuestionnaireAnswerAdmin(admin.ModelAdmin):
    model = EvacuationQuestionnaireAnswer
    list_display = ['__unicode__', 'question', 'answer']


admin.site.register(EvaluationQuestionnaireQuestion)
admin.site.register(EvacuationQuestionnaire)
admin.site.register(EvacuationQuestionnaireAnswer, EvacuationQuestionnaireAnswerAdmin)
