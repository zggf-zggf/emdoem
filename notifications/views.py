from django.shortcuts import render
from notifications.utils import prepare_notifications
from django.template.response import TemplateResponse

# Create your views here.


def show_notifications(view):
    def wrapper(request, *args, **kwargs):
        r = view(request, *args, **kwargs)
        if isinstance(r, TemplateResponse):
            r.context_data['notifications_data'] = prepare_notifications(request.user)
            return r.render()
        else:
            return r
    return wrapper
