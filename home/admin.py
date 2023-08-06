from django.contrib import admin
from .models import Announcement

# Register your models here.
class HomeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Announcement)
