from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from experiments.models import Experiment, Checkpoint
from .models import Plan, Connection

class PlanNewViewTest(TestCase):
    def log_user(self):
        user = User.objects.create_user(username='me', password='pass')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        self.client.logout()
        response = self.client.get(reverse('new_plan', kwargs={'pk_experiment': experiment.pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/plan/new/')

    def test_GET_user_cannot_add_plan_to_other_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        user_b = User.objects.create_user(username='user_b', password='pass')
        b2 = Building.objects.create(user=user, name='b1', country='gr')
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')
        response = self.client.get(reverse('new_plan', kwargs={'pk_experiment': experiment2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_new_plan(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        response = self.client.get(reverse('new_plan', kwargs={'pk_experiment': experiment.pk}))
        self.assertTemplateUsed(response, 'dashboard/plans/new_plan.html')

    def test_POST_redirect_user_insert_plan(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        response = self.client.post(reverse('new_plan', kwargs={'pk_experiment': experiment.pk}), data={
            'name': 'Plan'
        })
        self.assertRedirects(response, reverse('experiment_list'))

    def test_POST_save_user_delete_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        response = self.client.post(reverse('new_plan', kwargs={'pk_experiment': experiment.pk}), data={
            'name': 'Plan'
        })
        self.assertEqual(Plan.objects.count(), 1)
        self.assertEqual(Plan.objects.first().name, 'Plan')


class PlanDetailViewTest(TestCase):
    def log_user(self):
        user = User.objects.create_user(username='me', password='pass')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        self.client.logout()
        response = self.client.get(reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk':plan.pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/plan/1/')

    def test_GET_user_cannot_see_plan_to_other_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan1 = Plan.objects.create(experiment=experiment, name="plan")
        user_b = User.objects.create_user(username='user_b', password='pass')
        b2 = Building.objects.create(user=user, name='b1', country='gr')
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')
        plan2 = Plan.objects.create(experiment=experiment2, name="plan")
        response = self.client.get(reverse('plan_detail', kwargs={'pk_experiment': experiment2.pk, 'pk':plan2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_detail_plan(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        response = self.client.get(reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk':plan.pk}))
        self.assertTemplateUsed(response, 'dashboard/plans/plan_detail.html')

    def test_POST_redirect_user_update_plan(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        response = self.client.post(reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk': plan.pk}), data={
            'name': 'Plan1'
        })
        self.assertRedirects(response, reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk':plan.pk}))

    def test_POST_redirect_user_update_plan(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        response = self.client.post(reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk': plan.pk}), data={
            'name': 'Plan1'
        })
        self.assertEqual(Plan.objects.count(), 1)
        self.assertEqual(Plan.objects.first().name, 'Plan1')



class PlanDeleteViewTest(TestCase):
    def log_user(self):
        user = User.objects.create_user(username='me', password='pass')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        self.client.logout()
        response = self.client.get(reverse('plan_delete', kwargs={'pk_experiment': experiment.pk, 'pk':plan.pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/plan/1/delete/')

    def test_GET_user_cannot_delete_plan_to_other_experiment(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan1 = Plan.objects.create(experiment=experiment, name="plan")
        user_b = User.objects.create_user(username='user_b', password='pass')
        b2 = Building.objects.create(user=user, name='b1', country='gr')
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')
        plan2 = Plan.objects.create(experiment=experiment2, name="plan")
        response = self.client.get(reverse('plan_delete', kwargs={'pk_experiment': experiment2.pk, 'pk':plan2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_delete_plan(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        response = self.client.get(reverse('plan_delete', kwargs={'pk_experiment': experiment.pk, 'pk':plan.pk}))
        self.assertTemplateUsed(response,  'dashboard/plans/plan_delete.html')

    def test_POST_redirect_user_delete_plan(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        response = self.client.post(reverse('plan_delete', kwargs={'pk_experiment': experiment.pk, 'pk': plan.pk}))
        self.assertRedirects(response, reverse('plan_delete', kwargs={'pk_experiment': experiment.pk, 'pk':plan.pk}))

    def test_POST_redirect_user_delete_plan(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        response = self.client.post(reverse('plan_delete', kwargs={'pk_experiment': experiment.pk, 'pk': plan.pk}))
        self.assertEqual(Plan.objects.count(), 0)

















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
