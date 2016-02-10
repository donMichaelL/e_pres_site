from django.test import TestCase
from django.contrib.staticfiles import finders
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

    def test_GET_template_visitor_redirect_to_login(self):
        response = self.client.get(reverse('building_list'))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/')

    def test_GET_template_user_show_buildings(self):
        user = self.log_user()
        response = self.client.get(reverse('building_list'))
        self.assertTemplateUsed(response, 'dashboard/buildings/list_building.html')

    def test_GET_items_user_see_only_his_buildings(self):
        user = self.log_user()
        response = self.client.get(reverse('building_list'))
        self.assertContains(response, 'b1')
        self.assertNotContains(response, 'b2')
        self.assertEqual(response.context['object_list'].count(), user.building_set.count())

    def test_GET_items_admin_see_all_building(self):
        self.client.login(username='myuser', password='password')
        response = self.client.get(reverse('building_list'))
        self.assertContains(response, 'b1')
        self.assertContains(response, 'b2')
        self.assertEqual(response.context['object_list'].count(), Building.objects.count())


class BuildingInsertViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

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


class BuildingDeleteViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        Building.objects.create(user=user, name='b1', country='gr')
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_template_visitor_redirect_to_login(self):
        response = self.client.get(reverse('building_delete', kwargs={"pk": Building.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/1/delete/')

    def test_GET_template_user_show_delete_form(self):
        b1 = self.log_user().building_set.first()
        response = self.client.get(reverse('building_delete', kwargs={"pk": b1.pk}))
        self.assertTemplateUsed(response, 'dashboard/buildings/building_delete.html')

    def test_GET_template_user_not_show_other_user_building_delete(self):
        self.log_user()
        user2 = User.objects.get(username='me2')
        b2 = user2.building_set.first()
        response = self.client.get(reverse('building_delete', kwargs={"pk": b2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_POST_redirect_after_delete_success(self):
        b1 = self.log_user().building_set.first()
        response = self.client.post(reverse('building_delete', kwargs={"pk": b1.pk}))
        self.assertRedirects(response, reverse('building_list'))

    def test_POST_delete_after_delete_success(self):
        b1 = self.log_user().building_set.first()
        response = self.client.post(reverse('building_delete', kwargs={"pk": b1.pk}))
        self.assertEqual(Building.objects.count(), 1)


class BuildingUpdateViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        Building.objects.create(user=user, name='b1', country='gr')
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_template_visitor_redirect_to_login(self):
        response = self.client.get(reverse('building_detail', kwargs={"pk": Building.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/1/')

    def test_GET_template_user_not_show_other_user_building_detail(self):
        self.log_user()
        user2 = User.objects.get(username='me2')
        b2 = user2.building_set.first()
        response = self.client.get(reverse('building_detail', kwargs={"pk": b2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_admin_show_every_user_building(self):
        self.client.login(username='myuser', password='password')
        user2 = User.objects.get(username='me2')
        b2 = user2.building_set.first()
        response = self.client.get(reverse('building_detail', kwargs={"pk": b2.pk}))
        self.assertEqual(response.status_code, 200)


    def test_GET_template_user_show_detail(self):
        b1 = self.log_user().building_set.first()
        response = self.client.get(reverse('building_detail', kwargs={"pk": b1.pk}))
        self.assertTemplateUsed(response, 'dashboard/buildings/building_detail.html')

    def test_POST_redirect_user_updates_building(self):
        b1 = self.log_user().building_set.first()
        response = self.client.post(reverse('building_detail', kwargs={"pk": b1.pk}), data={
            'name': 'Building',
            'country': 'gr',
        })
        self.assertRedirects(response, reverse('building_detail', kwargs={"pk": b1.pk}))

    def test_POST_update_user_updates_building(self):
        b1 = self.log_user().building_set.first()
        response = self.client.post(reverse('building_detail', kwargs={"pk": b1.pk}), data={
            'name': 'Building',
            'country': 'gr',
        })
        self.assertEqual(Building.objects.count(), 2)
        self.assertEqual(Building.objects.first().name, 'Building')


class FloorNewViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        abs_path = finders.find('img/blueprint.jpg')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_template_visitor_redirect_to_login(self):
        response = self.client.get(reverse('floor_new', kwargs={"pk": Building.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/1/floor/new/')

    def test_GET_template_user_not_insert_in_other_user_building(self):
        self.log_user()
        user2 = User.objects.get(username='me2')
        b2 = user2.building_set.first()
        response = self.client.get(reverse('floor_new', kwargs={"pk": b2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_admin_insert_building(self):
        self.client.login(username=u'myuser', password='password')
        user2 = User.objects.get(username='me2')
        b2 = user2.building_set.first()
        response = self.client.get(reverse('floor_new', kwargs={"pk": b2.pk}))
        self.assertEqual(response.status_code, 200)

    def test_GET_template_user_show_insert_floor(self):
        self.log_user()
        response = self.client.get(reverse('floor_new', kwargs={"pk": self.log_user().building_set.first().pk}))
        self.assertTemplateUsed(response, 'dashboard/floors/new_floor.html')

    def test_POST_redirect_user_insert_building(self):
        abs_path = finders.find('img/blueprint.jpg')
        b1 = self.log_user().building_set.first()
        with open(abs_path) as fp:
            response = self.client.post(reverse('floor_new', kwargs={"pk": b1.pk}), data={
                'name': 'Floor',
                'number': 1,
                'blueprint': fp
            })
        self.assertRedirects(response, reverse('building_detail', kwargs={"pk": b1.pk}))

    def test_POST_save_user_floor_building_ennn(self):
        abs_path = finders.find('img/blueprint.jpg')
        b1 = self.log_user().building_set.first()
        with open(abs_path) as fp:
            response = self.client.post(reverse('floor_new', kwargs={"pk": b1.pk}), data={
                'name': 'Floor',
                'number': 1,
                'blueprint': fp
            })
        self.assertEqual(b1.floor_set.count(), 1)
        self.assertEqual(b1.floor_set.first().name, 'Floor')


class FloorUpdateViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        abs_path = finders.find('img/blueprint.jpg')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1, blueprint= abs_path)
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        floor2 = Floor.objects.create(building=b2, name="Second Floor", number=1, blueprint= abs_path)

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_template_visitor_redirect_to_login(self):
        response = self.client.get(reverse('floor_detail', kwargs={"pk_building":Floor.objects.first().building.pk ,"pk": Floor.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/1/floor/1/')

    def test_GET_template_user_not_see_detail_in_other_user_building_floor(self):
        self.log_user()
        user2 = User.objects.get(username='me2')
        b2 = user2.building_set.first()
        response = self.client.get(reverse('floor_detail', kwargs={"pk_building":b2.pk ,"pk": b2.floor_set.first().pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_admin_see_every_user_detail(self):
        self.client.login(username='myuser', password='password')
        user2 = User.objects.get(username='me2')
        b2 = user2.building_set.first()
        response = self.client.get(reverse('floor_detail', kwargs={"pk_building":b2.pk ,"pk": b2.floor_set.first().pk}))
        self.assertEqual(response.status_code, 200)

    def test_GET_template_user_show_detail_floor(self):
        b1 = self.log_user().building_set.first()
        floor1 = b1.floor_set.first()
        response = self.client.get(reverse('floor_detail', kwargs={"pk_building":b1.pk ,"pk": floor1.pk}))
        self.assertTemplateUsed(response, 'dashboard/floors/floor_detail.html')

    def test_POST_save_user_update_floor(self):
        abs_path = finders.find('img/blueprint.jpg')
        b1 = self.log_user().building_set.first()
        floor1 = b1.floor_set.first()
        with open(abs_path) as fp:
            response = self.client.post(reverse('floor_detail', kwargs={"pk_building":b1.pk ,"pk": floor1.pk}), data={
                'name': 'Floor',
                'number': 1,
                'blueprint': fp
            })
        self.assertRedirects(response, reverse('building_detail', kwargs={"pk": b1.pk}))

    def test_POST_redirect_user_update_building_floor(self):
        abs_path = finders.find('img/blueprint.jpg')
        b1 = self.log_user().building_set.first()
        floor1 = b1.floor_set.first()
        with open(abs_path) as fp:
            response = self.client.post(reverse('floor_detail', kwargs={"pk_building":b1.pk ,"pk": floor1.pk}), data={
                'name': 'updated',
                'number': 1,
                'blueprint': fp
            })
        self.assertEqual(b1.floor_set.count(), 1)
        self.assertEqual(b1.floor_set.first().name, 'updated')


class FloorDeleteViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        abs_path = finders.find('img/blueprint.jpg')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1, blueprint= abs_path)
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        floor2 = Floor.objects.create(building=b2, name="Second Floor", number=1, blueprint= abs_path)

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_template_visitor_redirect_to_login(self):
        response = self.client.get(reverse('floor_delete', kwargs={"pk_building":Floor.objects.first().building.pk ,"pk": Floor.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/1/floor/1/delete/')

    def test_GET_template_user_not_delete_in_other_user_building_floor(self):
        self.log_user()
        user2 = User.objects.get(username='me2')
        b2 = user2.building_set.first()
        response = self.client.get(reverse('floor_delete', kwargs={"pk_building":b2.pk ,"pk": b2.floor_set.first().pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_admin_can_delete_any_floor(self):
        self.client.login(username='myuser', password='password')
        user2 = User.objects.get(username='me2')
        b2 = user2.building_set.first()
        response = self.client.get(reverse('floor_delete', kwargs={"pk_building":b2.pk ,"pk": b2.floor_set.first().pk}))
        self.assertEqual(response.status_code, 200)

    def test_GET_template_user_show_delete_floor(self):
        b1 = self.log_user().building_set.first()
        floor1 = b1.floor_set.first()
        response = self.client.get(reverse('floor_delete', kwargs={"pk_building":b1.pk ,"pk": floor1.pk}))
        self.assertTemplateUsed(response, 'dashboard/floors/floor_delete.html')

    def test_POST_redirect_user_delete_floor(self):
        b1 = self.log_user().building_set.first()
        floor1 = b1.floor_set.first()
        response = self.client.post(reverse('floor_delete', kwargs={"pk_building":b1.pk ,"pk": floor1.pk}))
        self.assertRedirects(response, reverse('building_detail', kwargs={"pk": b1.pk}))

    def test_POST_save_user_delete_floor(self):
        b1 = self.log_user().building_set.first()
        floor1 = b1.floor_set.first()
        response = self.client.post(reverse('floor_delete', kwargs={"pk_building":b1.pk ,"pk": floor1.pk}))
        self.assertEqual(b1.floor_set.count(), 0)
