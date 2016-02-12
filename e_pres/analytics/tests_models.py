from django.test import TestCase
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from experiments.models import Experiment, Checkpoint
from .models import CheckpointReport


class CheckpointReportModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1')
        checkpoint = Checkpoint.objects.create(experiment=experiment, floor=floor1, coord_x=100, coord_y=200)
        report = CheckpointReport.objects.create(experiment=experiment, checkpoint=checkpoint, current_flux=50, fail=False)

    def test_checpoint_report_model(self):
        self.assertEqual(CheckpointReport.objects.count(), 1)
        self.assertEqual(CheckpointReport.objects.first().current_flux, 50)
