from django.test import TestCase
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from experiments.models import Experiment, Checkpoint
from .models import CheckpointReport


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


class ReportFluxPostExperimentTest(TestCase):
    def setUp(self):
        abs_path = finders.find('img/blueprint.jpg')
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1, blueprint= abs_path)
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        checkpoint = Checkpoint.objects.create(experiment=experiment, floor=floor1, coord_x=100, coord_y=200)
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        floor2 = Floor.objects.create(building=b2, name="First Floor", number=1, blueprint= abs_path)
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')
        checkpoint2 = Checkpoint.objects.create(experiment=experiment2, floor=floor2, coord_x=100, coord_y=200)
        report1 = CheckpointReport.objects.create(experiment=experiment, checkpoint=checkpoint, current_flux=20)

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_return_eror_message(self):
        response = self.client.get(reverse('report_flux_post_experiment', kwargs={'pk_experiment': Experiment.objects.first().pk, 'pk': Checkpoint.objects.first().pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_user_not_show_other_user_experiment_flux_detail(self):
        self.log_user()
        user2 = User.objects.get(username='me2')
        experiment = user2.experiment_set.first()
        response = self.client.get(reverse('report_flux_post_experiment', kwargs={'pk_experiment': experiment.pk, 'pk': experiment.checkpoint_set.first().pk}))
        self.assertEqual(response.status_code, 403)

    # def test_GET_admin_can_see_flux_details_of_everything(self):
    #     self.client.login(username='myuser', password='password')
    #     user2 = User.objects.get(username='me2')
    #     experiment = user2.experiment_set.first()
    #     response = self.client.get(reverse('report_flux_post_experiment', kwargs={'pk_experiment': experiment.pk, 'pk': experiment.checkpoint_set.first().pk}))
    #     self.assertEqual(response.status_code, 200)

    def test_GET_user_see_his_flux_detail(self):
        self.log_user()
        experiment = Experiment.objects.first()
        checkpoint = experiment.checkpoint_set.first()
        response = self.client.get(reverse('report_flux_post_experiment', kwargs={'pk_experiment': experiment.pk, 'pk': checkpoint.pk}))
        self.assertEqual(response.status_code, 200)
