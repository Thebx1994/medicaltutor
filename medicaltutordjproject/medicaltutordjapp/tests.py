from django.contrib.auth.models import User
from django.test import TestCase

from .models import (
    Concept,
    Exam,
    ExamSubject,
    Question,
    QuestionAttempt,
    QuestionOption,
    QuizSession,
    Subject,
    Topic,
)


class LearningFoundationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="demo", password="test-pass-123")
        self.exam = Exam.objects.create(name="ENARM", code="enarm", country="Mexico")
        self.subject = Subject.objects.create(name="Fisiología", code="fisiologia")
        self.topic = Topic.objects.create(subject=self.subject, name="Cardiovascular", slug="cardiovascular")
        self.concept = Concept.objects.create(topic=self.topic, name="Gasto cardíaco")
        ExamSubject.objects.create(exam=self.exam, subject=self.subject)

    def test_curriculum_hierarchy(self):
        self.assertEqual(self.topic.subject, self.subject)
        self.assertEqual(self.concept.topic, self.topic)
        self.assertEqual(self.exam.exam_subjects.count(), 1)

    def test_question_attempt_persists_learning_signals(self):
        question = Question.objects.create(
            stem="¿Cuál es la principal variable que determina el gasto cardíaco?",
            explanation="El gasto cardíaco depende de frecuencia cardíaca y volumen sistólico.",
            difficulty="medium",
            status="approved",
            subject=self.subject,
            topic=self.topic,
        )
        question.concepts.add(self.concept)
        QuestionOption.objects.create(question=question, text="Frecuencia cardíaca", is_correct=True, order=1)
        QuestionOption.objects.create(question=question, text="Temperatura", is_correct=False, order=2)

        session = QuizSession.objects.create(
            user=self.user,
            subject=self.subject,
            topic=self.topic,
        )
        attempt = QuestionAttempt.objects.create(
            user=self.user,
            quiz_session=session,
            question=question,
            selected_answer={"option_id": 1},
            is_correct=True,
            confidence=4,
            response_time_ms=4200,
        )

        self.assertEqual(attempt.question, question)
        self.assertEqual(question.concepts.count(), 1)
        self.assertEqual(attempt.confidence, 4)
        self.assertEqual(attempt.response_time_ms, 4200)
