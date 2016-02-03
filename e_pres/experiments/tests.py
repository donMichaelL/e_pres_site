from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from .models import Experiment, Checkpoint
from .test_utils import TestUtil


class ExperimentlistViewTest(TestUtil):
    def test_GET_redirect_to_login(self):
        self.GET_check_for_login_and_redirect('experiment_list', False, '?next=/experiment/' )

    def test_GET_template_user_show_experiments(self):
        self.GET_template_the_right_one('experiment_list', False, 'dashboard/experiments/list_experiment.html')

    def test_GET_items_user_see_only_his_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        # another user
        user_b = User.objects.create_user(username='user_b', password='pass')
        b1 = Building.objects.create(user=user_b, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user_b, building=b1, name='Second',disaster='eq')
        response = self.client.get(reverse('experiment_list'))
        self.assertContains(response, 'Experiment')
        self.assertNotContains(response, 'Second')
        self.assertEqual(response.context['object_list'].count(), user.experiment_set.count())


class ExperimentNewViewTest(TestUtil):
    def test_GET_redirect_to_login(self):
        self.GET_check_for_login_and_redirect('experiment_new', False, '?next=/experiment/new/' )

    def test_GET_template_new_experiment(self):
        self.GET_template_the_right_one('experiment_new', False, 'dashboard/experiments/new_experiment.html')

    def test_POST_redirect_user_save_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        response = self.client.post(reverse('experiment_new'), data={
            'building': b1.pk,
            'name': 'Experiment',
            'disaster': 'fl'
        })
        self.assertRedirects(response, reverse('experiment_list'))

    def test_POST_redirect_user_save_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        response = self.client.post(reverse('experiment_new'), data={
            'building': b1.pk,
            'name': 'Experiment',
            'disaster': 'fl'
        })
        self.assertEqual(Experiment.objects.count(), 1)
        self.assertEqual(Experiment.objects.first().disaster, 'fl')


class ExperimentDeleteViewTest(TestUtil):
    def test_GET_redirect_to_login(self):
        self.GET_check_for_login_and_redirect('experiment_delete', True, '?next=/experiment/1/delete/' )

    def test_GET_template_new_experiment(self):
        self.GET_template_the_right_one('experiment_delete', True, 'dashboard/experiments/experiment_delete.html')

    def test_POST_redirect_user_delete_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        response = self.client.post(reverse('experiment_delete', kwargs={'pk': experiment.pk}))
        self.assertRedirects(response, reverse('experiment_list'))

    def test_POST_save_user_delete_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        response = self.client.post(reverse('experiment_delete', kwargs={'pk': experiment.pk}))
        self.assertEqual(Experiment.objects.count(), 0)


class ExperimentDetailViewTest(TestUtil):
    def test_GET_redirect_to_login(self):
        self.GET_check_for_login_and_redirect('experiment_detail', True, '?next=/experiment/1/' )

    def test_GET_template_detail_experiment(self):
        self.GET_template_the_right_one('experiment_detail', True, 'dashboard/experiments/experiment_detail.html')

    def test_POST_redirect_user_update_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        response = self.client.post(reverse('experiment_detail', kwargs={'pk': experiment.pk}), data={
            'building': b1.pk,
            'name': 'Experiment',
            'disaster': 'fl'
        })
        self.assertRedirects(response, reverse('experiment_detail', kwargs={'pk': experiment.pk}))

    def test_POST_redirect_user_update_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        response = self.client.post(reverse('experiment_detail', kwargs={'pk': experiment.pk}), data={
            'building': b1.pk,
            'name': 'Experiment',
            'disaster': 'fl'
        })
        self.assertEqual(Experiment.objects.count(), 1)
        self.assertEqual(Experiment.objects.first().disaster, 'fl')





# models
class ExperimentModelTest(TestCase):
    def test_experiment_model(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        self.assertEqual(Experiment.objects.count(), 1)
        self.assertEqual(Experiment.objects.first().__unicode__(), 'Experiment')

    def test_experiment_get_absolute_url(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        self.assertEqual(experiment.get_absolute_url(), '/experiment/1/')


class CheckpointModelTest(TestCase):
    def test_checkpoint_model(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1')
        checkpoint = Checkpoint.objects.create(experiment=experiment, floor=floor1, coord_x=100, coord_y=200)
        self.assertEqual(Checkpoint.objects.count(), 1)
        self.assertEqual(Checkpoint.objects.first().__unicode__(), 'fl1')
