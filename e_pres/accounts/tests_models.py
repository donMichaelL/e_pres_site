from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class ProfilemodelTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='me', password='pass')

    def test_create_user(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual('me', User.objects.first().username)

    def test_user_creates_automatically_user_profile(self):
        user = User.objects.get(username='me')
        self.assertEqual(UserProfile.objects.count(), 1)
        user_profile = user.userprofile
        user_profile.organization = 'uoa'
        user_profile.save()
        self.assertEqual('uoa', UserProfile.objects.first().organization)
