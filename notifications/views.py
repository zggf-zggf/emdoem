from django.shortcuts import render
from notifications.utils import prepare_notifications
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
import json
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

@login_required(login_url='account:login')
def read_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    if notification.user != request.user:
        raise PermisionDenied()
    notification.is_read = True
    notification.save()

@login_required(login_url='account:login')
def read_all_notifications(request):
    Notification.objects.filter(user=request.user).update(is_read=True)
    response_data = {}
    response_data['result'] = "success"
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )
