from django.contrib import admin
from factguesser.models import Proposition, Answer

# Registering models for Admin view.
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('proposition', 'answer')

class PropositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'truthvalue', 'owner')
    
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Proposition, PropositionAdmin)