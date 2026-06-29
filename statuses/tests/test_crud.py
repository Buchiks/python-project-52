from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status

User = get_user_model()


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
        username='testuser',
        password='testpass123'
        )
            
        self.status = Status.objects.create(
            name='teststatus',
        )
        self.list_url = reverse("statuses:list")
        self.create_url = reverse("statuses:create")
        self.update_url = reverse('statuses:update', kwargs={
            "pk": self.status.pk
            })
        self.delete_url = reverse('statuses:delete', kwargs={
            "pk": self.status.pk
            })
    
    def test_status_list_not_logged_in(self):
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, 302) 
    
    def test_status_list(self):
        self.client.force_login(self.user)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, 200) 
    
    def test_status_create_not_logged_in(self):
        response = self.client.get(self.create_url)
        
        self.assertEqual(response.status_code, 302)

        response = self.client.post(self.create_url, data={
            "name": "something"
            })
        
        self.assertEqual(response.status_code, 302)

    def test_status_create(self):
        self.client.force_login(self.user)

        response = self.client.post(self.create_url, data={
            "name": "something"
            })
        
        self.assertRedirects(response, self.list_url)
        
        response = self.client.get(self.list_url)

        self.assertContains(response, "something")
    
    def test_update_status_not_allowed(self):
        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 302)
        
        self.client.post(self.update_url, data={
            "name": "something"
            })

        self.assertEqual(response.status_code, 302)

    def test_delete_status_not_allowed(self):
        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 302) 

        self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 302)

    def test_update_allowed(self):
        self.client.force_login(self.user)

        response = self.client.get(self.update_url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.update_url, 
            data={"name": "something"}
            )

        self.assertRedirects(response, self.list_url)

        response = self.client.get(self.list_url)

        self.assertContains(response, "something")
        self.assertNotContains(response, "teststatus")

    def test_delete_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(self.delete_url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.delete_url)

        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

        response = self.client.get(self.list_url)

        self.assertNotContains(response, "teststatus")
    