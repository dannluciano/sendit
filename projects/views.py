import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from projects.forms import ProjectForm
from projects.models import Project


def get_browser_icon_name(user_agent):
    browser_patterns = (
        ("Edge", r"Edg/([\d.]+)"),
        ("Chrome", r"Chrome/([\d.]+)"),
        ("Firefox", r"Firefox/([\d.]+)"),
        ("Safari", r"Version/([\d.]+).*Safari/"),
    )

    browser_name = "Unknown"

    for name, pattern in browser_patterns:
        match = re.search(pattern, user_agent)
        if match:
            browser_name = name
            break

    browser_icon_dict = {
        "Edge": "logo-edge",
        "Chrome": "logo-chrome",
        "Firefox": "logo-firefox",
        "Safari": "compass-outline",
        "Unknown": "earth-outline",
    }

    return browser_icon_dict[browser_name]


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
    context = {
        "project": project,
        "project_payload": project.to_dict(),
        "browser_icon": get_browser_icon_name(
            request.META.get("HTTP_USER_AGENT", "")
        ),
    }
    return render(request, "ide/project-detail.html", context)


@login_required
@require_POST
def project_delete(request, project_name):
    project = get_object_or_404(
        Project, name=project_name, owner=request.user
    )
    project.delete()
    return redirect(reverse("projects:home"))
