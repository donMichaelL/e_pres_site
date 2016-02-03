from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from .models import Experiment, Checkpoint


class TestUtil(TestCase):
    def log_user(self):
        user = User.objects.create_user(username='me', password='pass')
        self.client.login(username=user.username, password='pass')
        return user

    def GET_check_for_login_and_redirect(self, url, item, redirect_url):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        self.client.logout()
        if not item:
            response = self.client.get(reverse(url))
        else:
            response = self.client.get(reverse(url, kwargs={'pk': experiment.pk}))
        self.assertRedirects(response, reverse('homepage')+ redirect_url)

    def GET_template_the_right_one(self, url, item ,template):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        if not item:
            response = self.client.get(reverse(url))
        else:
            response = self.client.get(reverse(url, kwargs={'pk': experiment.pk}))
        self.assertTemplateUsed(response, template)
