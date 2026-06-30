from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class UsersCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_users_list(self):
        response = self.client.get(reverse("users:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
    
    def test_user_create(self):
        create_url = reverse("users:user_create")
        list_url = reverse("users:index")

        self.client.post(create_url, data={
            "username": "Bob", 
            "password1": "testpass123",
            "password2": "testpass123",
            })
        
        response = self.client.get(list_url)

        self.assertContains(response, "Bob")
    
    def test_login(self):
        response = self.client.post(reverse('user_login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
    
    def test_update_user_not_allowed(self):
        response = self.client.get(reverse(
            'users:user_update', 
            kwargs={"pk": self.user.pk}
            ))

        self.assertEqual(response.status_code, 302) 
    
    def test_delete_user_not_allowed(self):
        response = self.client.get(reverse(
            'users:user_delete', 
            kwargs={"pk": self.user.pk}
            ))

        self.assertEqual(response.status_code, 302) 
    
    def test_update_allowed(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse(
            'users:user_update', 
            kwargs={"pk": self.user.pk}
            ))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('users:user_update', kwargs={"pk": self.user.pk}), 
            data={
                "first_name": "Bob",
                "last_name": self.user.last_name,
                "username": self.user.username,
            })

        self.assertRedirects(response, reverse('users:index'))

        response = self.client.get(reverse('users:index'))

        self.assertContains(response, "Bob")
        self.assertNotContains(response, "Test")
    
    def test_delete_allowed(self):
        self.client.force_login(self.user)
        delete_url = reverse(
            'users:user_delete', 
            kwargs={"pk": self.user.pk}
            )
        response = self.client.post(delete_url)

        self.assertRedirects(response, reverse('users:index'))

        response = self.client.get(reverse('users:index'))

        self.assertNotContains(response, "Test")
    
    def test_logout(self):
        self.client.force_login(self.user)
        logout_url = reverse('user_logout')
        self.client.post(logout_url)

        self.assertNotIn('_auth_user_id', self.client.session)


    
