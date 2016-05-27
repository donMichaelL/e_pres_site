from django.test import TestCase
from django.contrib.auth.models import User
from buildings.models import Building
from experiments.models import Experiment
from .models import EvaluationTeachersQuestionnaireAnswer, EvaluationTeachersQuestionnaireQuestion, EvaluationStudentsQuestionnaireAnswer, EvaluationStudentsQuestionnaireQuestion, EvaluationQuestionnaireAnswer, EvaluationQuestionnaireQuestion, PreparednessQuestionnaireQuestion, PreparednessQuestionnaireAnswer

class PreparednessQuestionnaireQuestionTest(TestCase):
    def setUp(self):
        PreparednessQuestionnaireQuestion.objects.create(question="Are you sure")

    def test_preparedness_questionnaire_question_model(self):
        self.assertEqual(PreparednessQuestionnaireQuestion.objects.count(), 1)


class PreparednessQuestionnaireAnserTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        question = PreparednessQuestionnaireQuestion.objects.create(question="Are you sure")
        PreparednessQuestionnaireAnswer.objects.create(building=b1, question=question, answer="YES")

    def test_preparedness_questionnaire_answer_model(self):
        self.assertEqual(PreparednessQuestionnaireAnswer.objects.count(), 1)


class EvaluationQuestionnaireQuestionTest(TestCase):
    def setUp(self):
        EvaluationQuestionnaireQuestion.objects.create(question="Are you sure")

    def test_evaluation_questionnaire_question_model(self):
        self.assertEqual(EvaluationQuestionnaireQuestion.objects.count(), 1)


class EvaluationQuestionnaireAnswerTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        question = EvaluationQuestionnaireQuestion.objects.create(question="Are you sure")
        EvaluationQuestionnaireAnswer.objects.create(experiment=experiment, question=question, answer="YES")

    def test_evaluation_questionnaire_answer_model(self):
        self.assertEqual(EvaluationQuestionnaireAnswer.objects.count(), 1)


class EvaluationStudentsQuestionnaireQuestionTest(TestCase):
    def setUp(self):
        EvaluationStudentsQuestionnaireQuestion.objects.create(question="Are you sure")

    def test_evaluation_questionnaire_stundent_question_model(self):
        self.assertEqual(EvaluationStudentsQuestionnaireQuestion.objects.count(), 1)


class EvaluationStudentsQuestionnaireAnswerTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        question = EvaluationStudentsQuestionnaireQuestion.objects.create(question="Are you sure")
        EvaluationStudentsQuestionnaireAnswer.objects.create(experiment=experiment, question=question, answer="YES", ip="127.0.0.1")

    def test_evaluation_questionnaire__stundent_answer_model(self):
        self.assertEqual(EvaluationStudentsQuestionnaireAnswer.objects.count(), 1)


class EvaluationTeachersQuestionnaireQuestionTest(TestCase):
    def setUp(self):
        EvaluationTeachersQuestionnaireQuestion.objects.create(question="Are you sure")

    def test_evaluation_questionnaire_teacher_question_model(self):
        self.assertEqual(EvaluationTeachersQuestionnaireQuestion.objects.count(), 1)


class EvaluationStudentsQuestionnaireAnswerTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        experiment = Experiment.objects.create(user=user, building=b1, name='Experiment',disaster='eq')
        question = EvaluationTeachersQuestionnaireQuestion.objects.create(question="Are you sure")
        EvaluationTeachersQuestionnaireAnswer.objects.create(experiment=experiment, question=question, answer="YES", ip="127.0.0.1")

    def test_evaluation_questionnaire_teacher_answer_model(self):
        self.assertEqual(EvaluationTeachersQuestionnaireAnswer.objects.count(), 1)
