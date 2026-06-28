from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from tasks.models import Task
from statuses.models import Status
from labels.models import Label

User = get_user_model()


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
        username='testuser',
        password='testpass123'
        )

        self.exec = User.objects.create_user(
        username='executor',
        password='testpass123'
        )
            
        self.label = Label.objects.create(
            name='testlabel',
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

        self.label_tasked = Label.objects.create(
            name='label_with_task',
        )
        self.task.labels.add(self.label_tasked)   

        self.list_url = reverse("labels:list")
        self.create_url = reverse("labels:create")
        self.update_url = reverse('labels:update', kwargs={
            "pk": self.label.pk
            })
        self.delete_url = reverse('labels:delete', kwargs={
            "pk": self.label.pk
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
            })
        
        self.assertEqual(response.status_code, 302)

    def test_create(self):
        self.client.force_login(self.user)

        response = self.client.post(self.create_url, data={
            "name": "something",
            })
        
        self.assertRedirects(response, self.list_url)
        
        response = self.client.get(self.list_url)

        self.assertContains(response, "something")
    
    def test_update_not_allowed(self):
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 302)
        
        self.client.post(self.update_url, data={
            "name": "something",
            })

        self.assertEqual(response.status_code, 302)

    def test_delete_not_allowed(self):
        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 302) 

        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.post(reverse(
            'labels:delete', 
            kwargs={"pk": self.label_tasked.pk}
            ))
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(pk=self.label_tasked.pk).exists())

    def test_update_allowed(self):
        self.client.force_login(self.user)

        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.update_url, 
            data={
                "name": "something",
                }
            )

        self.assertRedirects(response, self.list_url)

        response = self.client.get(self.list_url)

        self.assertContains(response, "something")
        self.assertNotContains(response, "testlabel")

    def test_delete_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.delete_url)

        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

        response = self.client.get(self.list_url)

        self.assertNotContains(response, "testlabel")
    
