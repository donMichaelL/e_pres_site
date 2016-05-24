from django.contrib import admin
from .models import PreparednessQuestionnaireQuestion, PreparednessQuestionnaireAnswer


class PreparednessQuestionnaireAnswerAdmin(admin.ModelAdmin):
    model = PreparednessQuestionnaireAnswer
    list_display = ['__unicode__', 'question', 'answer']


admin.site.register(PreparednessQuestionnaireQuestion)
admin.site.register(PreparednessQuestionnaireAnswer, PreparednessQuestionnaireAnswerAdmin)
