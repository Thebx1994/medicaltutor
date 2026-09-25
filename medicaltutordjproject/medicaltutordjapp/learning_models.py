from django.conf import settings
from django.db import models


class Exam(models.Model):
    name = models.CharField(max_length=150)
    code = models.SlugField(max_length=50, unique=True)
    country = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=150)
    code = models.SlugField(max_length=80, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "name")

    def __str__(self):
        return self.name


class ExamSubject(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="exam_subjects")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="exam_subjects")
    weight = models.DecimalField(max_digits=6, decimal_places=3, default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "subject__name")
        constraints = [
            models.UniqueConstraint(
                fields=("exam", "subject"),
                name="unique_exam_subject",
            )
        ]

    def __str__(self):
        return f"{self.exam} - {self.subject}"


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="topics")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("subject", "slug"),
                name="unique_topic_slug_per_subject",
            )
        ]

    def __str__(self):
        return f"{self.subject} - {self.name}"


class Concept(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="concepts")
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("topic", "name"),
                name="unique_concept_per_topic",
            )
        ]

    def __str__(self):
        return f"{self.topic} - {self.name}"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    target_exam = models.ForeignKey(
        Exam,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    daily_goal_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - StudentProfile"
