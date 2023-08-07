from django.contrib import admin
from .models import Problemset

class ProblemsetAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Problemset)
