from django import forms
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Task, Worker


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "assignees": forms.CheckboxSelectMultiple(),
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }


class TaskCreateForm(TaskUpdateForm):
    class Meta(TaskUpdateForm.Meta):
        exclude = ["is_completed"]


class WorkerForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ("username", "email", "first_name", "last_name", "position")


class TaskNameSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)


class WorkerUsernameSearchForm(forms.Form):
    username = forms.CharField(max_length=255, required=False)
