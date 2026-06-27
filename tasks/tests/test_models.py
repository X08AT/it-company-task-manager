from django.contrib.auth import get_user_model
from django.test import TestCase

from tasks.models import Position, TaskType, Tag, Task


class TestModels(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Test Position")
        self.task_type = TaskType.objects.create(name="Test Task Type")
        self.tag = Tag.objects.create(name="Test Tag")
        self.worker = get_user_model().objects.create_user(
            username="TestUser",
            email="Test@gmail.com",
            password="TestPassword2026",
            first_name="TestFirstName",
            last_name="TestLastName",
            position=self.position,
        )
        self.task = Task.objects.create(
            name="Test Task",
            description="Test description for task",
            deadline="2026-12-31",
            is_completed=False,
            task_type=self.task_type,
        )
        self.task.tags.add(self.tag)
        self.task.assignees.add(self.worker)

    def test_position_str(self):
        self.assertEqual(str(self.position), "Test Position")

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Test Task Type")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "Test Tag")

    def test_worker_str(self):
        expected_str = "TestUser (TestFirstName TestLastName)"
        self.assertEqual(str(self.worker), expected_str)

    def test_task_str(self):
        self.assertEqual(str(self.task), "Test Task")

    def test_create_task_and_assignee(self):
        self.task.assignees.add(self.worker)
        self.assertIn(self.worker, self.task.assignees.all())
        self.assertIn(self.task, self.worker.tasks.all())

    def test_create_task_and_tag(self):
        self.task.tags.add(self.tag)
        self.assertIn(self.tag, self.task.tags.all())
        self.assertIn(self.task, self.tag.tasks.all())
