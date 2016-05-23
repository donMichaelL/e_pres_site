from django.contrib import admin
from .models import PreparednessQuestionnaireQuestion, PreparednessQuestionnaire, PreparednessQuestionnaireAnswer


class PreparednessQuestionnaireAnswerAdmin(admin.ModelAdmin):
    model = PreparednessQuestionnaireAnswer
    list_display = ['__unicode__', 'question', 'answer']


admin.site.register(PreparednessQuestionnaireQuestion)
admin.site.register(PreparednessQuestionnaire)
admin.site.register(PreparednessQuestionnaireAnswer, PreparednessQuestionnaireAnswerAdmin)
