from django.test import TestCase
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from .models import Experiment, Checkpoint


class ExperimentModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')

    def test_experiment_model(self):
        self.assertEqual(Experiment.objects.count(), 1)
        self.assertEqual(Experiment.objects.first().__unicode__(), 'Experiment')

    def test_experiment_get_absolute_url(self):
        self.assertEqual(Experiment.objects.first().get_absolute_url(), '/experiment/1/')


class CheckpointModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1')
        checkpoint = Checkpoint.objects.create(experiment=experiment, floor=floor1, coord_x=100, coord_y=200)

    def test_checkpoint_model(self):
        self.assertEqual(Checkpoint.objects.count(), 1)
        self.assertEqual(Checkpoint.objects.first().__unicode__(), 'fl1')

    def test_checkpoint_get_experiment_absolute_url(self):
        self.assertEqual(Checkpoint.objects.first().get_experiment_absolute_url(), '/experiment/1/')
