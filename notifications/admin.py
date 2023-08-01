from django.contrib import admin
from notifications.models import NewCommentNotification, Notification, NewSolutionNotification, NewProblemNotification

# Register your models here.

class NotificationsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(NewCommentNotification)
admin.site.register(NewSolutionNotification)
admin.site.register(NewProblemNotification)
admin.site.register(Notification)
