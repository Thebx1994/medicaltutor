from django.conf import settings
from django.db import models

from .learning_models import Concept, Subject, Topic


class Question(models.Model):
    QUESTION_TYPES = (
        ("single_choice", "Single choice"),
        ("multiple_choice", "Multiple choice"),
        ("true_false", "True/False"),
    )
    DIFFICULTIES = (
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    )
    STATUSES = (
        ("draft", "Draft"),
        ("under_review", "Under review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES, default="single_choice")
    stem = models.TextField()
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTIES, default="medium")
    status = models.CharField(max_length=20, choices=STATUSES, default="draft")
    source = models.CharField(max_length=100, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="questions", null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="questions", null=True, blank=True)
    concepts = models.ManyToManyField(Concept, related_name="questions", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.stem[:100]


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.question_id} - {self.text[:60]}"


class QuizSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_sessions")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="quiz_sessions")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name="quiz_sessions")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ("-started_at",)


class QuestionAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="question_attempts")
    quiz_session = models.ForeignKey(QuizSession, on_delete=models.CASCADE, related_name="attempts")
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="attempts")
    selected_answer = models.JSONField(default=dict)
    is_correct = models.BooleanField()
    confidence = models.PositiveSmallIntegerField(null=True, blank=True)
    response_time_ms = models.PositiveIntegerField(null=True, blank=True)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("attempted_at",)
        indexes = [
            models.Index(fields=("user", "attempted_at")),
            models.Index(fields=("question", "attempted_at")),
        ]
