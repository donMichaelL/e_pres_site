from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from buildings.models import Building
from experiments.models import Experiment
from .models import EvaluationTeachersQuestionnaireAnswer, EvaluationTeachersQuestionnaireQuestion, EvaluationStudentsQuestionnaireAnswer, EvaluationStudentsQuestionnaireQuestion, EvaluationQuestionnaireAnswer, EvaluationQuestionnaireQuestion, PreparednessQuestionnaireQuestion, PreparednessQuestionnaireAnswer


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

    def test_POST_user_can_answer_his_prepardness_questionnaire(self):
        user = self.log_user()
        question_pk = PreparednessQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('preparedness_questionnaire_new', kwargs={'pk': user.building_set.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PreparednessQuestionnaireAnswer.objects.count(), 1)

    def test_POST_user_can_answer_his_prepardeness_questionnaire_only_once(self):
        user = self.log_user()
        question_pk = PreparednessQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('preparedness_questionnaire_new', kwargs={'pk': user.building_set.first().pk}), data={
            'answers': dicto
        })
        response = self.client.post(reverse('preparedness_questionnaire_new', kwargs={'pk': user.building_set.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PreparednessQuestionnaireAnswer.objects.count(), 1)

    def test_POST_user_not_answer_other_user_prepardness_questionnaire(self):
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


class EvaluationQuestionnaireViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        EvaluationQuestionnaireQuestion.objects.create(question='Are you sure?')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_redirect_to_login(self):
        response = self.client.get(reverse('evacuation_questionnaire_list', kwargs={'pk':Experiment.objects.first().pk}))
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/evacuation_questionnaire/')

    def test_GET_template_user_not_show_other_user_questionnaire(self):
        user = self.log_user()
        user2 = User.objects.get(username='me2')
        response = self.client.get(reverse('evacuation_questionnaire_list', kwargs={'pk': user2.experiment_set.first().pk}))
        self.assertEqual(response.status_code, 403)

    def test_GET_template_detail_evacuation(self):
        user = self.log_user()
        response = self.client.get(reverse('evacuation_questionnaire_list', kwargs={'pk':user.experiment_set.first().pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/questionnaires/list_evacuationQuestions.html')

    def test_GET_admin_see_everything(self):
        self.client.login(username='myuser', password='password')
        user2 = User.objects.get(username='me2')
        response = self.client.get(reverse('preparedness_questionnaire_list', kwargs={'pk':user2.experiment_set.first().pk}))
        self.assertEqual(response.status_code, 200)


class EvaluationQuestionnaireFormTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        EvaluationQuestionnaireQuestion.objects.create(question='Are you sure?')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        experiment2 = Experiment.objects.create(user=user_b, building=b2, name='Experiment',disaster='eq')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_POST_visitor_cannot_evacuation_questionnaire(self):
        response = self.client.post(reverse('evacuation_questionnaire_new', kwargs={'pk': Experiment.objects.first().pk}), data={
            "answers": "{ 1: 'yes'  }"
        })
        self.assertRedirects(response, reverse('homepage')+ '?next=/experiment/1/evacuation_questionnaire/new/')

    def test_POST_user_can_answer_his_evacuation_questionnaire(self):
        user = self.log_user()
        question_pk = EvaluationQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('evacuation_questionnaire_new', kwargs={'pk': Experiment.objects.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EvaluationQuestionnaireAnswer.objects.count(), 1)

    def test_POST_user_can_answer_his_evacuation_questionnaire_only_once(self):
        user = self.log_user()
        question_pk = EvaluationQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('evacuation_questionnaire_new', kwargs={'pk': Experiment.objects.first().pk}), data={
            'answers': dicto
        })
        response = self.client.post(reverse('evacuation_questionnaire_new', kwargs={'pk': Experiment.objects.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EvaluationQuestionnaireAnswer.objects.count(), 1)

    def test_POST_user_not_answer_other_evacuation_user_questionnaire(self):
        user = self.log_user()
        user2 = User.objects.get(username='me2')
        question_pk = EvaluationQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('evacuation_questionnaire_new', kwargs={'pk': user2.experiment_set.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 403)

    def test_POST_user_not_answer_other_evacuation_user_questionnaire(self):
        self.client.login(username='myuser', password='password')
        user2 = User.objects.get(username='me2')
        question_pk = EvaluationQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('evacuation_questionnaire_new', kwargs={'pk': user2.experiment_set.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EvaluationQuestionnaireAnswer.objects.count(), 1)


class EvaluationStudentsQuestionnaireViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        EvaluationStudentsQuestionnaireQuestion.objects.create(question='Are you sure?')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_visitor_see_template_not_answered_students(self):
        response = self.client.get(reverse('student_questionnaire_list', kwargs={'pk':Experiment.objects.first().pk}))
        question = EvaluationStudentsQuestionnaireQuestion.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['questions'], question)
        self.assertTemplateUsed(response, 'student_questionnaire.html')

    def test_GET_visitor_see_template_answered_students(self):
        response = self.client.get(reverse('student_questionnaire_list', kwargs={'pk':Experiment.objects.first().pk}))
        experiment = Experiment.objects.first()
        question = EvaluationStudentsQuestionnaireQuestion.objects.first()
        EvaluationStudentsQuestionnaireAnswer.objects.create(experiment=experiment, question=question, answer="YES", ip="127.0.0.1")
        response = self.client.get(reverse('student_questionnaire_list', kwargs={'pk':Experiment.objects.first().pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['answered'], True)
        self.assertTemplateUsed(response, 'student_questionnaire.html')

    def test_POST_visitor_post_questionnaire_student(self):
        question_pk = EvaluationStudentsQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('student_questionnaire_list', kwargs={'pk': Experiment.objects.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EvaluationStudentsQuestionnaireAnswer.objects.count(), 1)

    def test_POST_visitor_post_questionnaire_student_only_once(self):
        question_pk = EvaluationStudentsQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('student_questionnaire_list', kwargs={'pk': Experiment.objects.first().pk}), data={
            'answers': dicto
        })
        response = self.client.post(reverse('student_questionnaire_list', kwargs={'pk': Experiment.objects.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EvaluationStudentsQuestionnaireAnswer.objects.count(), 1)


class EvaluationTeachersQuestionnaireViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user_b = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')
        EvaluationTeachersQuestionnaireQuestion.objects.create(question='Are you sure?')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_GET_visitor_see_template_not_answered_teachers(self):
        response = self.client.get(reverse('teachers_questionnaire_list', kwargs={'pk':Experiment.objects.first().pk}))
        question = EvaluationTeachersQuestionnaireQuestion.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['questions'], question)
        self.assertTemplateUsed(response, 'teacher_questionnaire.html')

    def test_GET_visitor_see_template_answered_teachers(self):
        response = self.client.get(reverse('teachers_questionnaire_list', kwargs={'pk':Experiment.objects.first().pk}))
        experiment = Experiment.objects.first()
        question = EvaluationTeachersQuestionnaireQuestion.objects.first()
        EvaluationTeachersQuestionnaireAnswer.objects.create(experiment=experiment, question=question, answer="YES", ip="127.0.0.1")
        response = self.client.get(reverse('teachers_questionnaire_list', kwargs={'pk':Experiment.objects.first().pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['answered'], True)
        self.assertTemplateUsed(response, 'teacher_questionnaire.html')

    def test_POST_visitor_post_questionnaire_teachers(self):
        question_pk = EvaluationTeachersQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('teachers_questionnaire_list', kwargs={'pk': Experiment.objects.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EvaluationTeachersQuestionnaireAnswer.objects.count(), 1)

    def test_POST_visitor_post_questionnaire_teachers_only_once(self):
        question_pk = EvaluationTeachersQuestionnaireQuestion.objects.first().pk
        dicto ='{"'+ str(question_pk) +'":"yes"}'
        response = self.client.post(reverse('teachers_questionnaire_list', kwargs={'pk': Experiment.objects.first().pk}), data={
            'answers': dicto
        })
        response = self.client.post(reverse('teachers_questionnaire_list', kwargs={'pk': Experiment.objects.first().pk}), data={
            'answers': dicto
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EvaluationTeachersQuestionnaireAnswer.objects.count(), 1)
