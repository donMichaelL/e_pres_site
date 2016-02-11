from django.test import TestCase
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from .models import Experiment, Checkpoint


class ExperimentlistViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        user_b = User.objects.create_user(username='user_b', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        experiment = Experiment.objects.create(user=user_b, building=b2, name='Second',disaster='eq')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        response = self.client.get(reverse('experiment_list'))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/')

    def test_GET_template_user_show_experiments(self):
        self.log_user()
        response = self.client.get(reverse('experiment_list'))
        self.assertTemplateUsed(response, 'dashboard/experiments/list_experiment.html')

    def test_GET_items_user_see_only_his_experiment(self):
        user = self.log_user()
        response = self.client.get(reverse('experiment_list'))
        self.assertContains(response, 'Experiment')
        self.assertNotContains(response, 'Second')
        self.assertEqual(response.context['object_list'].count(), user.experiment_set.count())

    def test_GET_items_admin_see_all_experiments(self):
        self.client.login(username='myuser', password='password')
        response = self.client.get(reverse('experiment_list'))
        self.assertContains(response, 'Experiment')
        self.assertContains(response, 'Second')
        self.assertEqual(response.context['object_list'].count(), Experiment.objects.count())


class ExperimentNewViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        response = self.client.get(reverse('experiment_new'))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/new/')

    def test_GET_template_new_experiment(self):
        self.log_user()
        response = self.client.get(reverse('experiment_new'))
        self.assertTemplateUsed(response,  'dashboard/experiments/new_experiment.html')

    def test_POST_redirect_user_save_experiment(self):
        user = self.log_user()
        response = self.client.post(reverse('experiment_new'), data={
            'building': user.building_set.first().pk,
            'name': 'Experiment',
            'disaster': 'fl'
        })
        self.assertRedirects(response, reverse('experiment_list'))

    def test_POST_redirect_user_save_experiment(self):
        user = self.log_user()
        response = self.client.post(reverse('experiment_new'), data={
            'building': user.building_set.first().pk,
            'name': 'Experiment',
            'disaster': 'fl'
        })
        self.assertEqual(Experiment.objects.count(), 1)
        self.assertEqual(Experiment.objects.first().disaster, 'fl')


class ExperimentDeleteViewTest(TestCase):
    def setUp(self):
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
        response = self.client.get(reverse('experiment_delete', kwargs={'pk':Experiment.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/delete/' )

    def test_GET_template_user_not_show_other_user_experiment_delete(self):
        user = self.log_user()
        user2 = User.objects.get(username='me2')
        experiment = user2.experiment_set.first()
        response = self.client.get(reverse('experiment_delete', kwargs={"pk": experiment.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_new_experiment(self):
        self.log_user()
        response = self.client.get(reverse('experiment_delete', kwargs={'pk':Experiment.objects.first().pk}))
        self.assertTemplateUsed(response, 'dashboard/experiments/experiment_delete.html')

    def test_POST_redirect_user_delete_experiment(self):
        experiment = self.log_user().experiment_set.first()
        response = self.client.post(reverse('experiment_delete', kwargs={'pk': experiment.pk}))
        self.assertRedirects(response, reverse('experiment_list'))

    def test_POST_save_user_delete_experiment(self):
        experiment = self.log_user().experiment_set.first()
        response = self.client.post(reverse('experiment_delete', kwargs={'pk': experiment.pk}))
        self.assertEqual(self.log_user().experiment_set.count(), 0)


class ExperimentDetailViewTest(TestCase):
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
        response = self.client.get(reverse('experiment_detail', kwargs={'pk':Experiment.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/' )

    def test_GET_template_user_not_show_other_user_experiment_detail(self):
        user = self.log_user()
        user2 = User.objects.get(username='me2')
        experiment = user2.experiment_set.first()
        response = self.client.get(reverse('experiment_detail', kwargs={"pk": experiment.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_admin_user_see_all_experiment_detail(self):
        self.client.login(username='myuser', password='password')
        user2 = User.objects.get(username='me2')
        experiment = user2.experiment_set.first()
        response = self.client.get(reverse('experiment_detail', kwargs={"pk": experiment.pk}))
        self.assertEqual(response.status_code, 200)

    def test_GET_template_detail_experiment(self):
        self.log_user()
        response = self.client.get(reverse('experiment_detail', kwargs={'pk':Experiment.objects.first().pk}))
        self.assertTemplateUsed(response, 'dashboard/experiments/experiment_detail.html')

    def test_POST_redirect_user_update_experiment(self):
        b1 = self.log_user().building_set.first()
        experiment = self.log_user().user.experiment_set.first()
        response = self.client.post(reverse('experiment_detail', kwargs={'pk': experiment.pk}), data={
            'building': b1.pk,
            'name': 'Experiment',
            'disaster': 'fl'
        })
        self.assertRedirects(response, reverse_lazy('experiment_detail', kwargs={'pk': experiment.pk}))

    def test_POST_redirect_user_update_experiment(self):
        b1 = self.log_user().building_set.first()
        experiment = self.log_user().experiment_set.first()
        response = self.client.post(reverse('experiment_detail', kwargs={'pk': experiment.pk}), data={
            'building': b1.pk,
            'name': 'Experiment',
            'disaster': 'fl'
        })
        self.assertEqual(self.log_user().experiment_set.count(), 1)
        self.assertEqual(self.log_user().experiment_set.first().disaster, 'fl')


class CheckpointDeleteTest(TestCase):
    def setUp(self):
        abs_path = finders.find('img/blueprint.jpg')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1', blueprint = abs_path)
        checkpoint = Checkpoint.objects.create(experiment=experiment, floor=floor1, coord_x=100, coord_y=200)
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        floor2 = Floor.objects.create(building=b2, name='fl2', number='1', blueprint = abs_path)
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')
        checkpoint2 = Checkpoint.objects.create(experiment=experiment2, floor=floor1, coord_x=100, coord_y=200)

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        response = self.client.get(reverse('checkpoint_delete', kwargs={'pk_experiment':Experiment.objects.first().pk,'pk': Checkpoint.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/checkpoint/1/delete/')

    def test_GET_user_cannot_delete_other_experiment(self):
        self.log_user()
        user_b = User.objects.get(username='me2')
        exp = user_b.experiment_set.first()
        ch2 = exp.checkpoint_set.first()
        response = self.client.get(reverse('checkpoint_delete', kwargs={'pk_experiment':exp.pk,'pk': ch2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_delete_checkpoint(self):
        exp = self.log_user().experiment_set.first()
        ch = exp.checkpoint_set.first()
        response = self.client.get(reverse('checkpoint_delete', kwargs={'pk_experiment':exp.pk,'pk': ch.pk}))
        self.assertTemplateUsed(response, 'dashboard/experiments/checkpoint_delete.html')

    def test_POST_redirect_user_delete_checkpoint(self):
        exp = self.log_user().experiment_set.first()
        ch = exp.checkpoint_set.first()
        response = self.client.post(reverse('checkpoint_delete', kwargs={'pk_experiment':exp.pk,'pk': ch.pk}))
        # TO-DO
        #self.assertRedirects(response, reverse('experiment_detail', kwargs={'pk': exp.pk}))
        self.assertEqual(response.status_code, 302)

    def test_POST_redirect_user_delete_checkpoint(self):
        exp = self.log_user().experiment_set.first()
        ch = exp.checkpoint_set.first()
        response = self.client.post(reverse('checkpoint_delete', kwargs={'pk_experiment':exp.pk,'pk': ch.pk}))
        self.assertEqual(exp.checkpoint_set.count(), 0)


class CheckpointInsertTest(TestCase):
    def setUp(self):
        abs_path = finders.find('img/blueprint.jpg')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1', blueprint = abs_path)
        exp = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        checkpoint = Checkpoint.objects.create(experiment=exp, floor=floor1, coord_x=100, coord_y=200)

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_POST_redirect_user_insert_checkpoint(self):
        self.log_user()
        exp = self.log_user().experiment_set.first()
        b1 = exp.building
        fl = b1.floor_set.first()
        response = self.client.post(reverse('checkpoint_new', kwargs={'pk': exp.pk}), data={
            'floor': fl.pk,
            'experiment': exp.pk,
            'coord_x': 100,
            'coord_y': 100
        })
        self.assertEqual(response.status_code, 302)
        # TO DO
        #self.assertRedirects(response, reverse('experiment_detail', kwargs={'pk': exp.pk}))

    def test_POST_save_user_checkpoint(self):
        self.log_user()
        exp = self.log_user().experiment_set.first()
        b1 = exp.building
        fl = b1.floor_set.first()
        response = self.client.post(reverse('checkpoint_new', kwargs={'pk': exp.pk}), data={
            'floor': fl.pk,
            'experiment': exp.pk,
            'coord_x': 100,
            'coord_y': 100
        })
        self.assertEqual(exp.checkpoint_set.count(), 2)

    def test_POST_redirect_user_update_checkpoint(self):
        self.log_user()
        exp = self.log_user().experiment_set.first()
        b1 = exp.building
        fl = b1.floor_set.first()
        response = self.client.post(reverse('checkpoint_new', kwargs={'pk': exp.pk}), data={
            'pk': exp.checkpoint_set.first().pk,
            'floor': fl.pk,
            'experiment': exp.pk,
            'coord_x': 200.000,
            'coord_y': 200.000
        })
        self.assertEqual(response.status_code, 302)
        # TO DO
        #self.assertRedirects(response, reverse('experiment_detail', kwargs={'pk': exp.pk}))

    def test_POST_update_user_checkpoint(self):
        self.log_user()
        exp = self.log_user().experiment_set.first()
        b1 = exp.building
        fl = b1.floor_set.first()
        response = self.client.post(reverse('checkpoint_new', kwargs={'pk': exp.pk}), data={
            'pk': exp.checkpoint_set.first().pk,
            'floor': fl.pk,
            'experiment': exp.pk,
            'coord_x': 200,
            'coord_y': 200
        })
        self.assertEqual(exp.checkpoint_set.count(), 1)
        self.assertEqual(exp.checkpoint_set.first().coord_x, 200)


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
        self.assertRedirects(response, reverse('homepage') + '?next=/experiment/1/post')

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
        self.assertTemplateUsed(response, 'dashboard/experiments/post_experiment.html')
