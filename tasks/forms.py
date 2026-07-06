from django import forms
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Task, Worker


class TaskBaseForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
            "assignees": forms.CheckboxSelectMultiple(),
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }


class TaskUpdateForm(TaskBaseForm):
    class Meta(TaskBaseForm.Meta):
        fields = "__all__"


class TaskCreateForm(TaskBaseForm):
    class Meta(TaskBaseForm.Meta):
        fields = (
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "tags",
            "assignees",
        )


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


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
        )


class TaskNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False, label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name..."}
        )
    )


class WorkerUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by username..."}
        )
    )
