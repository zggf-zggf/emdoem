from django.http import Http404
from django.shortcuts import render, redirect
from base.models import Problem, Content
from .forms import UploadForm, ContentForm

# Create your views here.


def problem_base(request):
    problems = Problem.objects.all()
    context = {'problems': problems}
    return render(request, "problemBase/problemBase.html", context)


def problem_page(request, pk):
    problem = Problem.objects.get(pk=pk)

    if problem is not None:
        context = {'name': problem.name, 'content': problem.content, 'pk': pk}
    else:
        raise Http404("Problem does not exist!")

    return render(request, "problemBase/problemStatement.html", context)


# To do: uploadowanie zdjęcia z poziomu strony, a nie przez panel admina.
def upload_problem_page(request):
    upload_form = UploadForm()

    if request.method == 'POST':
        upload_form = UploadForm(request.POST)

        if upload_form.is_valid() and \
                (upload_form['content_text'].value() is not None or upload_form['image'].value() is not None):

            print(upload_form['content_text'].value())
            problem = upload_form.save(commit=False)
            content = Content()
            content.content = upload_form['content_text'].value()
            content.image = upload_form['image'].value()
            content.save()

            problem.content = content

            problem.save()
            return redirect('problems:problem_base')

    context = {'upload_form': upload_form}

    return render(request, "problemBase/problemUpload.html", context)
