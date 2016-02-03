from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class TestUtil(TestCase):
    def log_user(self):
        user = User.objects.create_user(username='me', password='pass')
        self.client.login(username=user.username, password='pass')
        return user

    def GET_check_for_login_and_redirect(self, url, redirect_url):
        response = self.client.get(reverse(url))
        self.assertRedirects(response, reverse('homepage')+ redirect_url)

    def GET_template_the_right_one(self, url, template):
        user = self.log_user()
        response = self.client.get(reverse(url))
        self.assertTemplateUsed(response, template)
