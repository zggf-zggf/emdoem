from django.contrib import admin
from .models import Problem, Category, Solution, Comment, UserToProblem, SolutionVote

# Register your models here.


class ProblemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Category)
admin.site.register(Solution)
admin.site.register(Comment)
admin.site.register(UserToProblem)
admin.site.register(SolutionVote)
