from django.test import TestCase
from django.contrib.auth.models import User
from .models import Building, Floor


class BuildingmodelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')

    def test_building_model(self):
        self.assertEqual(Building.objects.count(), 2)
        self.assertEqual(Building.objects.first().country, 'gr')
        self.assertEqual(Building.objects.first().user.username, 'me')
        self.assertEqual(Building.objects.first().__unicode__(), 'b1')

    def test_building_get_absolute_url(self):
        user = User.objects.get(username='me')
        b1 = user.building_set.first()
        self.assertEqual(b1.get_absolute_url(), '/building/1/')

    def test_building_model_each_user_different(self):
        user1 = User.objects.get(username='me')
        user2 = User.objects.get(username='me2')
        self.assertEqual(Building.objects.count(), 2)
        self.assertEqual(user1.building_set.count(), 1)
        self.assertEqual(user1.building_set.first().name, 'b1')
        self.assertEqual(user2.building_set.count(), 1)
        self.assertEqual(user2.building_set.first().name, 'b2')


class FloormodelTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user1, name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1')
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        floor2 = Floor.objects.create(building=b2, name='fl1', number='1')

    def test_floor_model(self):
        self.assertEqual(Floor.objects.count(), 2)
        self.assertEqual(Floor.objects.first().name, 'fl1')
        self.assertEqual(Floor.objects.first().__unicode__(), 'fl1')

    def test_floor_get_absolute_url(self):
        user = User.objects.get(username='me')
        b1 = user.building_set.first()
        floor1 = b1.floor_set.first()
        self.assertEqual(floor1.get_absolute_url(), '/building/1/floor/1/')

    def test_floor_get_building_url(self):
        user = User.objects.get(username='me')
        b1 = user.building_set.first()
        floor1 = b1.floor_set.first()
        self.assertEqual(floor1.get_building_url(), '/building/1/')
