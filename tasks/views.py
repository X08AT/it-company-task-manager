from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from tasks.forms import (
    WorkerForm,
    TaskUpdateForm,
    TaskCreateForm,
    TaskNameSearchForm,
    WorkerUsernameSearchForm,
)
from tasks.models import Task, Worker, Position, TaskType, Tag


@login_required
def index(request):
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()
    num_not_completed = Task.objects.filter(is_completed=False).count()
    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "num_not_completed": num_not_completed,
    }
    return render(request, "tasks/index.html", context)


class PositionListView(LoginRequiredMixin, generic.ListView):
    queryset = Position.objects.annotate(num_workers=Count("workers"))
    template_name = "tasks/position_list.html"
    context_object_name = "position_list"


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("tasks:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("tasks:position-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    queryset = TaskType.objects.annotate(num_tasks=Count("tasks"))
    template_name = "tasks/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    context_object_name = "task_type"
    success_url = reverse_lazy("tasks:task-type-list")


class TagListView(LoginRequiredMixin, generic.ListView):
    queryset = Tag.objects.annotate(num_tasks=Count("tasks"))
    template_name = "tasks/tag_list.html"
    context_object_name = "tag_list"


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("tasks:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("tasks:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("tasks:tag-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    queryset = (Task.objects.select_related("task_type")
                .prefetch_related("tags"))
    paginate_by = 6
    template_name = "tasks/task_list.html"
    context_object_name = "task_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskNameSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskNameSearchForm(self.request.GET)
        return context


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = (Task.objects.select_related("task_type")
                .prefetch_related("assignees__position", "tags"))
    template_name = "tasks/task_detail.html"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    queryset = Worker.objects.select_related("position")
    paginate_by = 6
    template_name = "tasks/worker_list.html"
    context_object_name = "worker_list"

    def get_queryset(self):
        queryset = super().get_queryset().exclude(is_superuser=True)
        form = WorkerUsernameSearchForm(self.request.GET)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            if username:
                queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = WorkerUsernameSearchForm(self.request.GET)
        return context


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Worker.objects.select_related("position").prefetch_related(
        "tasks__task_type"
    )
    template_name = "tasks/worker_detail.html"


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("tasks:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "email", "position"]
    success_url = reverse_lazy("tasks:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasks:worker-list")


class ToggleAssignToTaskView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if task.assignees.filter(pk=request.user.pk).exists():
            task.assignees.remove(request.user)
        else:
            task.assignees.add(request.user)
        return redirect("tasks:task-detail", pk=pk)


class SignUpView(generic.CreateView):
    form_class = WorkerForm
    success_url = reverse_lazy("tasks:index")
    template_name = "registration/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("tasks:index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def form_valid(self, form):
        remember_me = self.request.POST.get("remember_me")

        if remember_me:
            self.request.session.set_expiry(None)
        else:
            self.request.session.set_expiry(0)

        return super().form_valid(form)


def custom_error_500(request):
    return render(request, "500.html", status=500)
