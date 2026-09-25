import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medicaltutordjapp", "0006_alter_quizzes_submission_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Exam",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("code", models.SlugField(max_length=50, unique=True)),
                ("country", models.CharField(blank=True, max_length=100)),
                ("description", models.TextField(blank=True)),
                ("active", models.BooleanField(default=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("code", models.SlugField(max_length=80, unique=True)),
                ("description", models.TextField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("active", models.BooleanField(default=True)),
            ],
            options={"ordering": ("order", "name")},
        ),
        migrations.CreateModel(
            name="ExamSubject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("weight", models.DecimalField(decimal_places=3, default=1, max_digits=6)),
                ("order", models.PositiveIntegerField(default=0)),
                ("exam", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="exam_subjects", to="medicaltutordjapp.exam")),
                ("subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="exam_subjects", to="medicaltutordjapp.subject")),
            ],
            options={"ordering": ("order", "subject__name")},
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=220)),
                ("description", models.TextField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("active", models.BooleanField(default=True)),
                ("subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="topics", to="medicaltutordjapp.subject")),
            ],
            options={"ordering": ("order", "name")},
        ),
        migrations.CreateModel(
            name="Concept",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=250)),
                ("description", models.TextField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("active", models.BooleanField(default=True)),
                ("topic", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="concepts", to="medicaltutordjapp.topic")),
            ],
            options={"ordering": ("order", "name")},
        ),
        migrations.CreateModel(
            name="StudentProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("daily_goal_minutes", models.PositiveIntegerField(default=30)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("target_exam", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="students", to="medicaltutordjapp.exam")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="student_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name="examsubject",
            constraint=models.UniqueConstraint(fields=("exam", "subject"), name="unique_exam_subject"),
        ),
        migrations.AddConstraint(
            model_name="topic",
            constraint=models.UniqueConstraint(fields=("subject", "slug"), name="unique_topic_slug_per_subject"),
        ),
        migrations.AddConstraint(
            model_name="concept",
            constraint=models.UniqueConstraint(fields=("topic", "name"), name="unique_concept_per_topic"),
        ),
    ]
