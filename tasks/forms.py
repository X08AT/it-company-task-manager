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


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["is_completed"]
        widgets = {
            "assignees": forms.CheckboxSelectMultiple(),
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }


class WorkerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "position"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True


class TaskNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False, label="",
        widget=forms.TextInput(attrs={"placeholder": "Search tasks by name..."})
    )


class WorkerUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search worker by username..."})
    )
