from django.contrib import admin
from .models import SolutionHistory

class SolutionsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(SolutionHistory)
