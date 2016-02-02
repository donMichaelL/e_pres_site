from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User
from .models import Building, Floor
from .forms import BuildingForm


class TestUtil(TestCase):
    def log_user(self):
        user = User.objects.create_user(username='me', password='pass')
        self.client.login(username=user.username, password='pass')
        return user


class BuildingpageView(TestUtil):
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


class BuildingInsertView(TestUtil):
    def test_GET_template_visitor_redirect_to_login(self):
        response = self.client.get(reverse('building_new'))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/new/')

    def test_GET_template_user_show_insert_form(self):
        user = self.log_user()
        response = self.client.get(reverse('building_new'))
        self.assertTemplateUsed(response, 'dashboard/buildings/new_building.html')

    def test_POST_redirect_user_insert_building(self):
        user = self.log_user()
        response = self.client.post(reverse('building_new'), data={
            'name': 'Building',
            'country': 'gr',
        })
        self.assertRedirects(response, reverse('building_list'))

    def test_POST_save_user_insert_building(self):
        user = self.log_user()
        response = self.client.post(reverse('building_new'), data={
            'name': 'Building',
            'country': 'gr',
        })
        self.assertEqual(Building.objects.count(), 1)
        self.assertEqual(Building.objects.first().name, 'Building')


class BuildingDeleteView(TestUtil):
    def test_GET_template_visitor_redirect_to_login(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        self.client.logout()
        response = self.client.get(reverse('building_delete', kwargs={"pk": b1.pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/1/delete/')

    def test_GET_template_user_show_delete_form(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        response = self.client.get(reverse('building_delete', kwargs={"pk": b1.pk}))
        self.assertTemplateUsed(response, 'dashboard/buildings/building_delete.html')

    def test_GET_template_user_not_show_other_user_building_delete(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        response = self.client.get(reverse('building_delete', kwargs={"pk": b2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_POST_redirect_after_delete_success(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        response = self.client.post(reverse('building_delete', kwargs={"pk": b1.pk}))
        self.assertRedirects(response, reverse('building_list'))

    def test_POST_delete_after_delete_success(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        response = self.client.post(reverse('building_delete', kwargs={"pk": b1.pk}))
        self.assertEqual(Building.objects.count(), 0)


class BuildingUpdateView(TestUtil):
    def test_GET_template_visitor_redirect_to_login(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        self.client.logout()
        response = self.client.get(reverse('building_detail', kwargs={"pk": b1.pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/1/')

    def test_GET_template_user_not_show_other_user_building_detail(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        response = self.client.get(reverse('building_detail', kwargs={"pk": b2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_user_show_detail(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        response = self.client.get(reverse('building_detail', kwargs={"pk": b1.pk}))
        self.assertTemplateUsed(response, 'dashboard/buildings/building_detail.html')

    def test_POST_redirect_user_updates_building(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        response = self.client.post(reverse('building_detail', kwargs={"pk": b1.pk}), data={
            'name': 'Building',
            'country': 'gr',
        })
        self.assertRedirects(response, reverse('building_detail', kwargs={"pk": b1.pk}))

    def test_POST_update_user_updates_building(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        response = self.client.post(reverse('building_detail', kwargs={"pk": b1.pk}), data={
            'name': 'Building',
            'country': 'gr',
        })
        self.assertEqual(Building.objects.count(), 1)
        self.assertEqual(Building.objects.first().name, 'Building')



class FloorNewView(TestUtil):
    def test_GET_template_visitor_redirect_to_login(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1)
        self.client.logout()
        response = self.client.get(reverse('floor_new', kwargs={"pk": b1.pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/1/floor/new/')

    def test_GET_template_user_not_insert_in_other_user_building(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1)
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        floor2 = Floor.objects.create(building=b2, name="First Floor", number=1)
        response = self.client.get(reverse('floor_new', kwargs={"pk": b2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_user_show_insert_floor(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1)
        response = self.client.get(reverse('floor_new', kwargs={"pk": b1.pk}))
        self.assertTemplateUsed(response, 'dashboard/floors/new_floor.html')

    def test_POST_redirect_user_insert_building(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        abs_path = finders.find('img/blueprint.jpg')
        with open(abs_path) as fp:
            response = self.client.post(reverse('floor_new', kwargs={"pk": b1.pk}), data={
                'name': 'Floor',
                'number': 1,
                'blueprint': fp
            })
        self.assertRedirects(response, reverse('building_detail', kwargs={"pk": b1.pk}))

    def test_POST_save_user_floor_building(self):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        abs_path = finders.find('img/blueprint.jpg')
        with open(abs_path) as fp:
            response = self.client.post(reverse('floor_new', kwargs={"pk": b1.pk}), data={
                'name': 'Floor',
                'number': 1,
                'blueprint': fp
            })
        self.assertEqual(b1.floor_set.count(), 1)
        self.assertEqual(b1.floor_set.first().name, 'Floor')





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
