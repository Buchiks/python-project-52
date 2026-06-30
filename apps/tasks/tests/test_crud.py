from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.statuses.models import Status
from apps.tasks.models import Task

User = get_user_model()


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
        username='testuser',
        password='testpass123'
        )
        self.exec = User.objects.create_user(
        username='executor',
        password='testpass123'
        )
            
        self.status = Status.objects.create(
            name='teststatus',
        )

        self.task = Task.objects.create(
            name="testtask",
            author=self.user,
            executor=self.exec,
            status=self.status
        )

        self.list_url = reverse("tasks:list")
        self.create_url = reverse("tasks:create")
        self.update_url = reverse('tasks:update', kwargs={
            "pk": self.task.pk
            })
        self.delete_url = reverse('tasks:delete', kwargs={
            "pk": self.task.pk
            })
    
    def test_list_not_logged_in(self):
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, 302) 
    
    def test_list(self):
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, 200) 
    
    def test_create_not_logged_in(self):
        response = self.client.get(self.create_url)
        
        self.assertEqual(response.status_code, 302)

        response = self.client.post(self.create_url, data={
            "name": "something",
            "executor": self.exec.pk,
            "status": self.status.pk
            })
        
        self.assertEqual(response.status_code, 302)

    def test_create(self):
        self.client.force_login(self.user)

        response = self.client.post(self.create_url, data={
            "name": "something",
            "executor": self.exec.pk,
            "status": self.status.pk
            })
        
        self.assertRedirects(response, self.list_url)
        
        response = self.client.get(self.list_url)

        self.assertContains(response, "something")
    
    def test_update_not_allowed(self):
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 302)
        
        self.client.post(self.update_url, data={
            "name": "something",
            "executor": self.exec.pk,
            "status": self.status.pk
            })

        self.assertEqual(response.status_code, 302)

    def test_delete_not_allowed(self):
        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 302) 

        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 302)

    def test_update_allowed(self):
        self.client.force_login(self.user)

        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.update_url, 
            data={
                "name": "something",
                "executor": self.exec.pk,
                "status": self.status.pk
                }
            )

        self.assertRedirects(response, self.list_url)

        response = self.client.get(self.list_url)

        self.assertContains(response, "something")
        self.assertNotContains(response, "testtask")

    def test_delete_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.delete_url)

        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

        response = self.client.get(self.list_url)

        self.assertNotContains(response, "testtask")
    