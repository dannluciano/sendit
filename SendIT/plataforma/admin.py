from django.contrib import admin
from .models import Questoes, Submissoes


class SubmissoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'questao', 'status')
    list_filter = ('status', )


admin.site.register(Questoes)
admin.site.register(Submissoes, SubmissoesAdmin)
