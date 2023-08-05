from django.contrib import admin
from .models import ProblemHistory

class ProblemsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(ProblemHistory)
