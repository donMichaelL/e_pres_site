from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from buildings.models import Building
from .models import PreparednessQuestionnaireQuestion, PreparednessQuestionnaireAnswer


class PreparednessViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        PreparednessQuestionnaireQuestion.objects.create(question='Are you sure?')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        response = self.client.get(reverse('preparedness_questionnaire_list', kwargs={'pk':Building.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/1/preparedness_questionnaire/')

    def test_GET_template_user_not_show_other_user_questionnaire(self):
        user = self.log_user()
        user2 = User.objects.get(username='me2')
        response = self.client.get(reverse('preparedness_questionnaire_list', kwargs={'pk':user2.building_set.first().pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_detail_preparedness(self):
        user = self.log_user()
        response = self.client.get(reverse('preparedness_questionnaire_list', kwargs={'pk':user.building_set.first().pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/questionnaires/list_preparednessQuestions.html')

    def test_GET_admin_see_everything(self):
        self.client.login(username='myuser', password='password')
        user2 = User.objects.get(username='me2')
        response = self.client.get(reverse('preparedness_questionnaire_list', kwargs={'pk':user2.building_set.first().pk}))
        self.assertEqual(response.status_code, 200)

class PreparednessFormTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        PreparednessQuestionnaireQuestion.objects.create(question='Are you sure?')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_POST_visitor_cannot_prepardness_questionnaire(self):
        response = self.client.post(reverse('preparedness_questionnaire_list', kwargs={'pk': Building.objects.first().pk}), data={
            "answers": "{ 1: 'yes'  }"
        })
        self.assertRedirects(response, reverse('homepage')+ '?next=/building/1/preparedness_questionnaire/')

    def test_POST_user_can_answer_hist_questionnaire(self):
        user = self.log_user()
        question_pk = PreparednessQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('preparedness_questionnaire_new', kwargs={'pk': user.building_set.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PreparednessQuestionnaireAnswer.objects.count(), 1)

    def test_POST_user_not_answer_other_user_questionnaire(self):
        user = self.log_user()
        user2 = User.objects.get(username='me2')
        question_pk = PreparednessQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('preparedness_questionnaire_new', kwargs={'pk': user2.building_set.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 403)

    def test_POST_admin_can_answer_everything(self):
        self.client.login(username='myuser', password='password')
        user2 = User.objects.get(username='me2')
        question_pk = PreparednessQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('preparedness_questionnaire_new', kwargs={'pk': user2.building_set.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PreparednessQuestionnaireAnswer.objects.count(), 1)
