from django import forms

from projects.models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        fields = ("name",)
        model = Project
