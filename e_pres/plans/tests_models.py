from django.test import TestCase
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from experiments.models import Experiment, Checkpoint
from .models import Plan, Connection

class PlanModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        experiment2 = Experiment.objects.create(user=user2, building=b2, name='Second',disaster='eq')
        plan2 = Plan.objects.create(experiment=experiment2, name="plan2")

    def test_plan_model(self):
        self.assertEqual(Plan.objects.count(), 2)
        self.assertEqual(Plan.objects.first().__unicode__(), 'plan')

    def test_get_absolute_url(self):
        self.assertEqual(Plan.objects.first().get_absolute_url(), '/experiment/1/plan/1/')

    def test_plan_model_each_user_different(self):
        user1 = User.objects.get(username='me')
        experiment1 = user1.experiment_set.first()
        user2 = User.objects.get(username='me2')
        experiment2 = user2.experiment_set.first()
        self.assertEqual(Plan.objects.count(), 2)
        self.assertEqual(experiment1.plan_set.count(), 1)
        self.assertEqual(experiment1.plan_set.first().name, 'plan')
        self.assertEqual(experiment2.plan_set.count(), 1)
        self.assertEqual(experiment2.plan_set.first().name, 'plan2')

class ConectionModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1')
        checkpoint = Checkpoint.objects.create(experiment=experiment, floor=floor1, coord_x=100, coord_y=200)
        con = Connection.objects.create(plan=plan, checkpoint=checkpoint, seq=1)

    def test_connection_model(self):
        self.assertEqual(Connection.objects.count(), 1)
        self.assertEqual(Plan.objects.first().__unicode__(), 'plan')
