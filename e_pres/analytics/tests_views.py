from django.test import TestCase
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from .models import Experiment, Checkpoint


class PostExperimentViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Second',disaster='eq')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        response = self.client.get(reverse('post_experiment', kwargs={'pk': Experiment.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage') + '?next=/experiment/1/post-execution')

    def test_GET_template_user_not_show_other_user_post_experiment(self):
        self.log_user()
        user2 = User.objects.get(username='me2')
        experiment = user2.experiment_set.first()
        response = self.client.get(reverse('post_experiment', kwargs={'pk': experiment.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_admin_can_see_every_post_experiment(self):
        self.client.login(username='myuser', password='password')
        user2 = User.objects.get(username='me2')
        experiment = user2.experiment_set.first()
        response = self.client.get(reverse('post_experiment', kwargs={"pk": experiment.pk}))
        self.assertEqual(response.status_code, 200)

    def test_GET_template_detail_experiment(self):
        self.log_user()
        response = self.client.get(reverse('post_experiment', kwargs={'pk':Experiment.objects.first().pk}))
        self.assertTemplateUsed(response, 'dashboard/analytics/post_experiment.html')
