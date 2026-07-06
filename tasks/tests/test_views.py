from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from tasks.models import Position, TaskType, Tag, Task


class TasksViewsTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position",
        )
        self.task_type = TaskType.objects.create(
            name="Test TaskType",
        )
        self.tag = Tag.objects.create(
            name="Test Tag",
        )
        self.worker = get_user_model().objects.create_user(
            username="TestUser",
            password="TestPassword2026",
            email="test@gmail.com",
            first_name="TestFirstName",
            last_name="TestLastName",
            position=self.position,
        )
        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            deadline="2026-12-31",
            is_completed=False,
            task_type=self.task_type,
        )
        self.task.tags.add(self.tag)
        self.task.assignees.add(self.worker)

        self.client.force_login(self.worker)

    def test_index_count(self):
        url = reverse("tasks:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_tasks"], 1)
        self.assertEqual(response.context["num_workers"], 1)
        self.assertEqual(response.context["num_not_completed"], 1)

    def test_login_required_redirect(self):
        self.client.logout()
        url = reverse("tasks:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_worker_list_search(self):
        get_user_model().objects.create_user(
            username="Alex_ba",
            password="TestPasswordALEX",
            email="alex@gmail.com",
            first_name="Alex",
            last_name="Smith",
            position=self.position,
        )
        url = reverse("tasks:worker-list")
        response = self.client.get(url, data={"username": "t"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["worker_list"]), 1)
        self.assertEqual(
            response.context["worker_list"][0].username,
            "TestUser"
        )

    def test_task_list_search(self):
        Task.objects.create(
            name="make model",
            description="Test Description",
            deadline="2026-12-31",
            is_completed=False,
            task_type=self.task_type,
        )
        url = reverse("tasks:task-list")
        response = self.client.get(url, data={"name": "t"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_list"]), 1)
        self.assertEqual(response.context["task_list"][0].name, "Test Task")

    def test_toggle_assign_to_task(self):
        url = reverse("tasks:toggle-assign-task", args=[self.task.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()
        self.assertNotIn(self.worker, self.task.assignees.all())

        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, 302)

        self.task.refresh_from_db()
        self.assertIn(self.worker, self.task.assignees.all())
