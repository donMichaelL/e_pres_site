from django.test import TestCase
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User
from buildings.models import Building, Floor
from experiments.models import Experiment, Checkpoint
from .models import Plan, Connection


class PlanNewViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user, name='b1', country='gr')
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        response = self.client.get(reverse('new_plan', kwargs={'pk_experiment': Experiment.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/plan/new/')

    def test_GET_user_cannot_add_plan_to_other_experiment(self):
        self.log_user()
        user_b = User.objects.get(username='me2')
        experiment2 = user_b.experiment_set.first()
        response = self.client.get(reverse('new_plan', kwargs={'pk_experiment': experiment2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_new_plan(self):
        self.log_user()
        response = self.client.get(reverse('new_plan', kwargs={'pk_experiment': Experiment.objects.first().pk}))
        self.assertTemplateUsed(response, 'dashboard/plans/new_plan.html')

    def test_POST_redirect_user_insert_plan(self):
        user = self.log_user()
        experiment = self.log_user().experiment_set.first()
        response = self.client.post(reverse('new_plan', kwargs={'pk_experiment': experiment.pk}), data={
            'name': 'Plan'
        })
        self.assertRedirects(response, reverse('experiment_list'))

    def test_POST_save_user_delete_experiment(self):
        user = self.log_user()
        experiment = self.log_user().experiment_set.first()
        response = self.client.post(reverse('new_plan', kwargs={'pk_experiment': experiment.pk}), data={
            'name': 'Plan'
        })
        self.assertEqual(Plan.objects.count(), 1)
        self.assertEqual(Plan.objects.first().name, 'Plan')


class PlanDetailViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user, name='b1', country='gr')
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')
        plan2 = Plan.objects.create(experiment=experiment2, name="plan")

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        experiment = Experiment.objects.first()
        response = self.client.get(reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk':experiment.plan_set.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/plan/1/')

    def test_GET_user_cannot_see_plan_to_other_experiment(self):
        self.log_user()
        user_b = User.objects.get(username='me2')
        experiment2 = user_b.experiment_set.first()
        response = self.client.get(reverse('plan_detail', kwargs={'pk_experiment': experiment2.pk, 'pk':experiment2.plan_set.first().pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_detail_plan(self):
        experiment = self.log_user().experiment_set.first()
        response = self.client.get(reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk':experiment.plan_set.first().pk}))
        self.assertTemplateUsed(response, 'dashboard/plans/plan_detail.html')

    def test_POST_redirect_user_update_plan(self):
        experiment = self.log_user().experiment_set.first()
        response = self.client.post(reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk': experiment.plan_set.first().pk}), data={
            'name': 'Plan1'
        })
        self.assertRedirects(response, reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk':experiment.plan_set.first().pk}))

    def test_POST_redirect_user_update_plan(self):
        experiment = self.log_user().experiment_set.first()
        response = self.client.post(reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk': experiment.plan_set.first().pk}), data={
            'name': 'updated'
        })
        self.assertEqual(experiment.plan_set.count(), 1)
        self.assertEqual(experiment.plan_set.first().name, 'updated')


class PlanDeleteViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user, name='b1', country='gr')
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')
        plan2 = Plan.objects.create(experiment=experiment2, name="plan")

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        experiment = Experiment.objects.first()
        response = self.client.get(reverse('plan_delete', kwargs={'pk_experiment': experiment.pk, 'pk':experiment.plan_set.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/plan/1/delete/')

    def test_GET_user_cannot_delete_plan_to_other_experiment(self):
        self.log_user()
        user_b = User.objects.get(username='me2')
        experiment2 = user_b.experiment_set.first()
        response = self.client.get(reverse('plan_delete', kwargs={'pk_experiment': experiment2.pk, 'pk':experiment2.plan_set.first().pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_delete_plan(self):
        experiment = self.log_user().experiment_set.first()
        response = self.client.get(reverse('plan_delete', kwargs={'pk_experiment': experiment.pk, 'pk':experiment.plan_set.first().pk}))
        self.assertTemplateUsed(response, 'dashboard/plans/plan_delete.html')

    def test_POST_redirect_user_delete_plan(self):
        experiment = self.log_user().experiment_set.first()
        response = self.client.post(reverse('plan_delete', kwargs={'pk_experiment': experiment.pk, 'pk': experiment.plan_set.first().pk}))
        self.assertRedirects(response, reverse('experiment_list'))


    def test_POST_redirect_user_delete_plan(self):
        experiment = self.log_user().experiment_set.first()
        response = self.client.post(reverse('plan_delete', kwargs={'pk_experiment': experiment.pk, 'pk': experiment.plan_set.first().pk}))
        self.assertEqual(experiment.plan_set.count(), 0)


class ConnectionDeleteViewTest(TestCase):
    def setUp(self):
        abs_path = finders.find('img/blueprint.jpg')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan1 = Plan.objects.create(experiment=experiment, name="plan")
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1, blueprint= abs_path)
        checkpoint = Checkpoint.objects.create(experiment=experiment, floor=floor1, coord_x=100, coord_y=200)
        con = Connection.objects.create(plan=plan1, checkpoint=checkpoint, seq=1)
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user, name='b1', country='gr')
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')
        plan2 = Plan.objects.create(experiment=experiment2, name="plan")

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        response = self.client.get(reverse('plan_delete_connections', kwargs={'pk_experiment': Experiment.objects.first().pk, 'pk':Plan.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/plan/1/delete/connections/')

    def test_GET_user_cannot_delete_plan_to_other_experiment(self):
        user = self.log_user()
        user_b = User.objects.get(username='me2')
        experiment2 = user_b.experiment_set.first()
        plan2 = experiment2.plan_set.first()
        response = self.client.get(reverse('plan_delete_connections', kwargs={'pk_experiment': experiment2.pk, 'pk':plan2.pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_delete_plan(self):
        user = self.log_user()
        experiment = self.log_user().experiment_set.first()
        plan = experiment.plan_set.first()
        response = self.client.get(reverse('plan_delete_connections', kwargs={'pk_experiment': experiment.pk, 'pk':plan.pk}))
        self.assertTemplateUsed(response,  'dashboard/plans/connections_delete.html')

    def test_POST_redirect_user_delete_plan(self):
        user = self.log_user()
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        #experiment = user.experiment_set.first()
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        #experiment = Experiment.objects.first()
        #plan = experiment.plan_set.first()
        plan = Plan.objects.create(experiment=experiment, name="plan")
        response = self.client.post(reverse('plan_delete_connections', kwargs={'pk_experiment': experiment.pk, 'pk': plan.pk}))
        self.assertRedirects(response, reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk':plan.pk}))

    def test_POST_save_user_delete_plan(self):
        user = self.log_user()
        experiment = user.experiment_set.first()
        plan = experiment.plan_set.first()
        response = self.client.post(reverse('plan_delete_connections', kwargs={'pk_experiment': experiment.pk, 'pk': plan.pk}))
        self.assertEqual(Connection.objects.count(), 0)


class ConnectionInsertViewTest(TestCase):
    def log_user(self):
        user = User.objects.create_user(username='me', password='pass')
        self.client.login(username=user.username, password='pass')
        return user

    # def test_POST_redirect_user_insert_connection_plan(self):
    #     user = self.log_user()
    #     abs_path = finders.find('img/blueprint.jpg')
    #     b1 = Building.objects.create(user=user, name='b1', country='gr')
    #     experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
    #     plan = Plan.objects.create(experiment=experiment, name="plan")
    #     floor1 = Floor.objects.create(building=b1, name='fl1', number='1', blueprint=abs_path)
    #     checkpoint = Checkpoint.objects.create(experiment=experiment, floor=floor1, coord_x=100, coord_y=200)
    #     response = self.client.post(reverse('plan_add_connection', kwargs={'pk_experiment': experiment.pk, 'pk': plan.pk}), data={
    #         'form-TOTAL_FORMS': '1',
    #         'form-INITIAL_FORMS': '0',
    #         'form-MAX_NUM_FORMS': '1',
    #         'form-0-checkpoint': checkpoint.pk,
    #         'form-0-seq': 1
    #     })
    #     self.assertRedirects(response, reverse('plan_detail', kwargs={'pk_experiment': experiment.pk, 'pk':plan.pk}))

    def test_POST_save_user_connection_plan(self):
        user = self.log_user()
        abs_path = finders.find('img/blueprint.jpg')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        plan = Plan.objects.create(experiment=experiment, name="plan")
        floor1 = Floor.objects.create(building=b1, name='fl1', number='1', blueprint=abs_path)
        checkpoint = Checkpoint.objects.create(experiment=experiment, floor=floor1, coord_x=100, coord_y=200)
        response = self.client.post(reverse('plan_add_connection', kwargs={'pk_experiment': experiment.pk, 'pk': plan.pk}), data={
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '1',
            'form-0-checkpoint': checkpoint.pk,
            'form-0-seq': 1
        })
        self.assertEqual(Connection.objects.count(), 1)
        self.assertEqual(Connection.objects.first().seq, 1)
