from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser

class UserManagementTests(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(username='admin', password='password', role='Admin')
        self.user1 = CustomUser.objects.create_user(username='user1', password='password', role='Viewer')
        self.user2 = CustomUser.objects.create_user(username='user2', password='password', role='Viewer')

    # 1. Registration
    def test_user_registration(self):
        url = reverse('user-list')
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'new@example.com'}
        # Unauthenticated POST
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    # 2. Admin Listing
    def test_admin_can_list_users(self):
        self.client.login(username='admin', password='password')
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 3 users created in setUp
        self.assertEqual(response.data['count'], 3)

    def test_viewer_cannot_list_users(self):
        self.client.login(username='user1', password='password')
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 3. Profile Access (/me)
    def test_user_can_access_own_profile(self):
        self.client.login(username='user1', password='password')
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user1')

    # 4. Object Permissions
    def test_user_cannot_view_others_detail(self):
        self.client.login(username='user1', password='password')
        url = reverse('user-detail', kwargs={'pk': self.user2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_edit_own_detail(self):
        self.client.login(username='user1', password='password')
        url = reverse('user-detail', kwargs={'pk': self.user1.pk})
        data = {'email': 'updated@example.com'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.email, 'updated@example.com')
