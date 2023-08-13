from django.contrib import admin
from .models import Problemset, ProblemsetDuringEditing

class ProblemsetAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Problemset)
admin.site.register(ProblemsetDuringEditing)
