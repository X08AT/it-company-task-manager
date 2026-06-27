from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Position, Tag, TaskType, Task


class AdminSiteTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="AdminPassword2026"
        )
        self.client.force_login(self.admin_user)

        self.position = Position.objects.create(name="Test Position")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            email="worker@gmail.com",
            password="WorkerPassword2026",
            position=self.position,
        )
        self.tag = Tag.objects.create(name="Test Tag")
        self.task_type = TaskType.objects.create(name="Test Task Type")

        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            deadline="2026-12-31",
            task_type=self.task_type,
        )
        self.task.tags.add(self.tag)
        self.task.assignees.add(self.worker)

    def test_task_admin_changelist_and_renders_custom_fields(self):
        url = reverse("admin:tasks_task_changelist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Test Task")
        self.assertContains(response, "worker")
        self.assertContains(response, "Test Tag")

    def test_worker_admin_changelist_page(self):
        url = reverse("admin:tasks_worker_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.worker.username)
        self.assertContains(response, self.worker.position.name)

    def test_worker_admin_change_page(self):
        url = reverse("admin:tasks_worker_change", args=(self.worker.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.worker.position.name)

    def test_worker_admin_add_page(self):
        url = reverse("admin:tasks_worker_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.worker.position.name)
