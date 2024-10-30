import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from projects.forms import ProjectForm
from projects.models import Project


@login_required
def home(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, "ide/home.html", {"projects": projects})


@login_required
def project_new(request):
    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            owner = request.user
            project, created = Project.objects.get_or_create(
                name=name, owner=owner
            )
            return redirect(
                reverse("projects:project-detail", args=[project.name])
            )
        else:
            return render(request, "ide/project-new.html", {"form": form})
    else:
        form = ProjectForm(initial={"name": ""})
        return render(request, "ide/project-new.html", {"form": form})


@login_required
def project_detail(request, project_name):
    project = get_object_or_404(
        Project, name=project_name, owner=request.user
    )
    project_json = json.dumps(project.to_dict())
    context = {"project": project, "project_json": project_json}
    return render(request, "ide/project-detail.html", context)


@login_required
@require_POST
def project_delete(request, project_name):
    project = get_object_or_404(
        Project, name=project_name, owner=request.user
    )
    project.delete()
    return redirect(reverse("projects:home"))
