from django.contrib import admin
from .models import Problem, Category, Solution, Comment, UserToProblem, SolutionVote, User

# Register your models here.


class ProblemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(User)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(Category)
admin.site.register(Solution)
admin.site.register(Comment)
admin.site.register(UserToProblem)
admin.site.register(SolutionVote)
