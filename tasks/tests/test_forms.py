from django.contrib.auth import get_user_model
from django.test import TestCase

from tasks.forms import (WorkerForm,
                         TaskCreateForm,
                         TaskUpdateForm,
                         TaskNameSearchForm,
                         WorkerUsernameSearchForm
                         )
from tasks.models import Position, TaskType, Tag, Task


class FormTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position",
        )

        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )
        self.task_tag = Tag.objects.create(
            name="Test Task Tag",
        )
        self.worker = get_user_model().objects.create_user(
            username="TestUsername2",
            email="test2@gmail.com",
            first_name="TestFirstName2",
            last_name="TestLastName2",
            password="TestPassword2026",
            position=self.position,
        )

    def test_worker_form_valid(self):
        form_data = {
            "username": "TestUsername",
            "email": "test@gmail.com",
            "first_name": "TestFirstName",
            "last_name": "TestLastName",
            "position": self.position.id,
            "password1": "TestPassword2026",
            "password2": "TestPassword2026",
        }
        form = WorkerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_form_invalid(self):
        form_data = {
            "username": "TestUsername",
            "email": "",
            "first_name": "",
            "last_name": "",
            "position": self.position.id,
            "password1": "TestPassword2026",
            "password2": "TestPassword2026",
        }
        form = WorkerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["This field is required."])
        self.assertEqual(
            form.errors["first_name"],
            ["This field is required."]
        )
        self.assertEqual(form.errors["last_name"], ["This field is required."])

    def test_task_create_form_valid(self):
        form_data = {
            "name": "Test Task",
            "description": "Test Task Description",
            "deadline": "2026-12-31",
            "priority": Task.Priority.MEDIUM.value,
            "task_type": self.task_type.id,
            "tags": [self.task_tag.pk],
            "assignees": [self.worker.pk],
        }
        form = TaskCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_create_form_exclude_completed(self):
        form = TaskCreateForm()
        self.assertNotIn("is_completed", form.fields)

    def test_task_update_form_include_completed(self):
        form = TaskUpdateForm()
        self.assertIn("is_completed", form.fields)

    def test_task_name_search_form_can_be_empty(self):
        form_data = {
            "name": "",
        }
        form = TaskNameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_username_search_form_can_be_empty(self):
        form_data = {
            "username": "",
        }
        form = WorkerUsernameSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
