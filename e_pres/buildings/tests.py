from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Building, Floor


class BuildingpageView(TestCase):
    def log_user(self):
        user = User.objects.create_user(username='me', password='pass')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_template_visitor_redirect_to_login(self):
        response = self.client.get(reverse('building_list'))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/')

    def test_GET_template_user_show_buildings(self):
        user = self.log_user()
        response = self.client.get(reverse('building_list'))
        self.assertTemplateUsed(response, 'dashboard/buildings/list_building.html')

    def test_GET_items_user_see_only_his_buildings(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        # another user
        user_b = User.objects.create_user(username='user_b', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        response = self.client.get(reverse('building_list'))
        self.assertContains(response, 'b1')
        self.assertNotContains(response, 'b2')
        self.assertEqual(response.context['object_list'].count(), user.building_set.count())




# models
class BuildingmodelTest(TestCase):
    def test_building_model(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        self.assertEqual(Building.objects.count(), 1)
        self.assertEqual(Building.objects.first().country, 'gr')
        self.assertEqual(Building.objects.first().user.username, 'me')
        self.assertEqual(Building.objects.first().__unicode__(), 'b1')

    def test_building_get_absolute_url(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        self.assertEqual(b1.get_absolute_url(), '/building/1/')

    def test_building_model_each_user_different(self):
        user1 = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user1, name='b1', country='gr')
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        self.assertEqual(Building.objects.count(), 2)
        self.assertEqual(user1.building_set.count(), 1)
        self.assertEqual(user1.building_set.first().name, 'b1')
        self.assertEqual(user2.building_set.count(), 1)
        self.assertEqual(user2.building_set.first().name, 'b2')

class FloormodelTest(TestCase):
    def test_floor_model(self):
        user1 = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user1, name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1')
        floor2 = Floor.objects.create(building=b1, name='fl2', number='2')
        self.assertEqual(Floor.objects.count(), 2)
        self.assertEqual(Floor.objects.first().name, 'fl1')
        self.assertEqual(floor1.building, b1)
        self.assertEqual(floor1.__unicode__(), 'fl1')
        self.assertEqual(Floor.objects.last().name, 'fl2')
        self.assertEqual(floor2.building, b1)
        self.assertEqual(floor2.__unicode__(), 'fl2')


    def test_floor_get_absolute_url(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1')
        self.assertEqual(floor1.get_absolute_url(), '/building/1/floor/1/')

    def test_floor_get_building_url(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1')
        self.assertEqual(floor1.get_building_url(), '/building/1/')
