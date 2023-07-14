from django.contrib import admin
from notifications.models import NewCommentNotification

# Register your models here.

class NotificationsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(NewCommentNotification)
