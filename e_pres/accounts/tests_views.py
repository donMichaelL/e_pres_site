from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from .models import UserProfile


class HomepageTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_template_visitor_returns_login(self):
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'account/login.html')

    def test_GET_template_user_to_building_page(self):
        self.log_user()
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'dashboard/buildings/list_building.html')


class ProfilepageTest(TestCase):
    def log_user(self):
        user = User.objects.create_user(username='me', password='pass')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_template_visior_redirect_to_home_page(self):
        response = self.client.get(reverse('profile_settings'))
        self.assertRedirects(response, reverse('homepage')+'?next=/profile/')

    def test_GET_template_user_to_profile_page(self):
        self.log_user()
        response = self.client.get(reverse('profile_settings'))
        self.assertTemplateUsed(response, 'dashboard/profile.html')

    def test_POST_redirect_user_to_profile_page(self):
        user = self.log_user()
        response = self.client.post(reverse('profile_settings'), data={
            'first_name': 'Michael',
            'last_name': 'Loukeris',
            'email': 'email@email.com',
            'organization': 'uoa'
        })
        self.assertRedirects(response, reverse('profile_settings'))

    def test_POST_save_user_to_profile_page(self):
        user = self.log_user()
        response = self.client.post(reverse('profile_settings'), data={
            'first_name': 'Michael',
            'last_name': 'Loukeris',
            'email': 'email@email.com',
            'organization': 'uoa'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual('Michael', User.objects.first().first_name)
        self.assertEqual('uoa', UserProfile.objects.first().organization)


class PasswordchangeTest(TestCase):
    def log_user(self):
        user = User.objects.create_user(username='me', password='pass')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_template_visitor_redirect_to_home_page(self):
        response = self.client.get(reverse('account_change_password'))
        self.assertRedirects(response, reverse('homepage')+'?next=/accounts/password/change/')

    def test_GET_template_user_to_password_change_page(self):
        self.log_user() 
        response = self.client.get(reverse('account_change_password'))
        self.assertTemplateUsed(response, 'account/password_change.html')
