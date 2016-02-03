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


class FloorUtil(TestUtil):
    def GET_template_visitor_redirect_to_login(self, url, item, redirect_url):
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1)
        self.client.logout()
        if not item:
            response = self.client.get(reverse(url, kwargs={"pk": b1.pk}))
        else:
            response = self.client.get(reverse(url, kwargs={"pk_building":b1.pk ,"pk": floor1.pk}))
        self.assertRedirects(response, reverse('homepage')+ redirect_url)

    def GET_template_user_not_actions_in_other_user_building(self, url, item):
        abs_path = finders.find('img/blueprint.jpg')
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1, blueprint= abs_path)
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        floor2 = Floor.objects.create(building=b2, name="First Floor", number=1, blueprint= abs_path)
        if not item:
            response = self.client.get(reverse(url, kwargs={"pk": b2.pk}))
        else:
            response = self.client.get(reverse(url, kwargs={"pk_building":b2.pk ,"pk": floor2.pk}))
        self.assertEqual(response.status_code, 403)

    def GET_template_user_show_template(self, url, item, template):
        abs_path = finders.find('img/blueprint.jpg')
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1, blueprint= abs_path)
        if not item:
            response = self.client.get(reverse(url, kwargs={"pk": b1.pk}))
        else:
            response = self.client.get(reverse(url, kwargs={"pk_building":b1.pk ,"pk": floor1.pk}))
        self.assertTemplateUsed(response, template)

    def POST_redirect_user(self, url, item):
        abs_path = finders.find('img/blueprint.jpg')
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1, blueprint= abs_path)
        abs_path = finders.find('img/blueprint.jpg')
        with open(abs_path) as fp:
            if not item:
                response = self.client.post(reverse(url, kwargs={"pk": b1.pk}), data={
                    'name': 'Floor',
                    'number': 1,
                    'blueprint': fp
                })
            else:
                response = self.client.post(reverse(url, kwargs={"pk_building":b1.pk ,"pk": floor1.pk}), data={
                    'name': 'Floor',
                    'number': 1,
                    'blueprint': fp
                })
        self.assertRedirects(response, reverse('building_detail', kwargs={"pk": b1.pk}))

    def POST_save_user(self, url, item, delete):
        abs_path = finders.find('img/blueprint.jpg')
        b1 = Building.objects.create(user=self.log_user(), name='b1', country='gr')
        if item:
            floor1 = Floor.objects.create(building=b1, name="First Floor", number=1, blueprint= abs_path)
        with open(abs_path) as fp:
            if not item:
                response = self.client.post(reverse(url, kwargs={"pk": b1.pk}), data={
                    'name': 'Floor',
                    'number': 1,
                    'blueprint': fp
                })
            else:
                response = self.client.post(reverse('floor_detail', kwargs={"pk_building":b1.pk ,"pk": floor1.pk}), data={
                        'name': 'Floor',
                        'number': 1,
                        'blueprint': fp
                })

        self.assertEqual(b1.floor_set.count(), 1)
        self.assertEqual(b1.floor_set.first().name, 'Floor')
