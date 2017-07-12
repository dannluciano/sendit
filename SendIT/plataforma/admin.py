from django.contrib import admin
from .models import Question, Submission, CaseTest


class SubmissoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'questao', 'status')
    list_filter = ('status', )


admin.site.register(Question)
admin.site.register(Submission, SubmissoesAdmin)
admin.site.register(CaseTest)
