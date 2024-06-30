import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from projects.forms import ProjectForm
from projects.models import Project, create_project


@login_required
def home(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, "ide/home.html", {"projects": projects})


@login_required
def project_new(request):
    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            create_project(form.cleaned_data["name"], request.user)
            return redirect(reverse("projects:home"))
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
