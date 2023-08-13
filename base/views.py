from django.shortcuts import render

# Create your views here.
def page_404(request, exception):
    return render(request, 'base/404.html', status=404)

def page_403(request, exception):
    return render(request, 'base/403.html', status=403)
