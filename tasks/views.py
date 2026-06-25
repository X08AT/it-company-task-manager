from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import (
    WorkerForm,
    TaskForm,
    TaskNameSearchForm,
    WorkerUsernameSearchForm,
)
from tasks.models import Task, Worker, Position, TaskType


def index(request):
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()
    num_not_completed = Task.objects.filter(is_completed=False).count()
    num_urgent = Task.objects.filter(
        priority="A_URGENT",
        is_completed=False
    ).count()
    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "num_urgent": num_urgent,
        "num_not_completed": num_not_completed,
    }
    return render(request, "tasks/index.html", context)


class PositionListView(generic.ListView):
    queryset = Position.objects.annotate(num_workers=Count("workers"))
    template_name = "tasks/position_list.html"
    context_object_name = "position_list"


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("tasks:position-list")


class TaskTypeListView(generic.ListView):
    queryset = TaskType.objects.annotate(num_tasks=Count("tasks"))
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("tasks:task-type-list")


class TaskListView(generic.ListView):
    queryset = Task.objects.select_related("task_type")
    paginate_by = 5
    template_name = "tasks/task_list.html"
    context_object_name = "task_list"

    def get_queryset(self):
        queryset = self.queryset
        self.form = TaskNameSearchForm(self.request.GET)
        if self.form.is_valid():
            name = self.form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        return context


class TaskDetailView(generic.DetailView):
    queryset = (Task.objects.select_related("task_type")
                .prefetch_related("assignees"))
    template_name = "tasks/task_detail.html"


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class WorkerListView(generic.ListView):
    queryset = Worker.objects.select_related("position")
    paginate_by = 5
    template_name = "tasks/worker_list.html"
    context_object_name = "worker_list"

    def get_queryset(self):
        queryset = self.queryset
        self.form = WorkerUsernameSearchForm(self.request.GET)
        if self.form.is_valid():
            username = self.form.cleaned_data.get("username")
            if username:
                queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        return context


class WorkerDetailView(generic.DetailView):
    queryset = Worker.objects.select_related("position").prefetch_related(
        "tasks__task_type"
    )
    template_name = "tasks/worker_detail.html"


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "email", "position"]
    success_url = reverse_lazy("tasks:worker-list")


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")


def toggle_assign_to_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if task in request.user.tasks.all():
        request.user.tasks.remove(task)
    else:
        request.user.tasks.add(task)
    return redirect("tasks:task-detail", pk=pk)
