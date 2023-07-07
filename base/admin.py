from django.contrib import admin
from .models import Problem, Category, Content, Solution, Comment, UserToProblem

# Register your models here.

admin.site.register(Problem)
admin.site.register(Category)
admin.site.register(Content)
admin.site.register(Solution)
admin.site.register(Comment)
admin.site.register(UserToProblem)