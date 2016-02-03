from django.test import TestCase
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from experiments.models import Experiment, Checkpoint
from .models import Plan, Connection



# models

class PlanModelTest(TestCase):
    def test_plan_model(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        self.assertEqual(Plan.objects.count(), 1)
        self.assertEqual(Plan.objects.first().__unicode__(), 'plan')

    def test_get_absolute_url(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        self.assertEqual(plan.get_absolute_url(), '/experiment/1/plan/1/')


class ConectionModelTest(TestCase):
    def test_connection_model(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1')
        checkpoint = Checkpoint.objects.create(experiment=experiment, floor=floor1, coord_x=100, coord_y=200)
        con = Connection.objects.create(plan=plan, checkpoint=checkpoint, seq=1)
        self.assertEqual(Connection.objects.count(), 1)
        self.assertEqual(Plan.objects.first().__unicode__(), 'plan')
