import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Building, Floor


class BuildingpageViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user_b = User.objects.create_user(username='user_b', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_403_visitor(self):
        response = self.client.get(reverse('building_rest_list'))
        self.assertEqual(response.status_code, 403)

    def test_GET_user_get_his_buildings(self):
        user = self.log_user()
        response = self.client.get(reverse('building_rest_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], "b1")

    def test_GET_user_dont_get_others_buildings(self):
        user = self.log_user()
        response = self.client.get(reverse('building_rest_list'))
        self.assertEqual(len(response.json()), 1)
        self.assertNotEqual(response.json()[0]['name'], "b2")

    def test_GET_admin_get_all_buildings(self):
        self.client.login(username='myuser', password='password')
        response = self.client.get(reverse('building_rest_list'))
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['name'], "b1")
        self.assertEqual(response.json()[1]['name'], "b2")
