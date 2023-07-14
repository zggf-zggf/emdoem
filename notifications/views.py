from django.shortcuts import render
from notifications.utils import prepare_notifications

# Create your views here.
def show_notifications(view):
    def wrapper(request, *args, **kwargs):
        r = view(request, *args, **kwargs)
        r.context_data['notifications_data'] = prepare_notifications(request.user)
        return r.render()
    return wrapper
