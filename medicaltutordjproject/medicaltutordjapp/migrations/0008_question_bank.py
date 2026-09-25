import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medicaltutordjapp", "0007_learning_foundations"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("question_type", models.CharField(choices=[("single_choice", "Single choice"), ("multiple_choice", "Multiple choice"), ("true_false", "True/False")], default="single_choice", max_length=30)),
                ("stem", models.TextField()),
                ("explanation", models.TextField(blank=True)),
                ("difficulty", models.CharField(choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")], default="medium", max_length=10)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("under_review", "Under review"), ("approved", "Approved"), ("rejected", "Rejected")], default="draft", max_length=20)),
                ("source", models.CharField(blank=True, max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("subject", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="questions", to="medicaltutordjapp.subject")),
                ("topic", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="questions", to="medicaltutordjapp.topic")),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="QuizSession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("score", models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ("subject", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="quiz_sessions", to="medicaltutordjapp.subject")),
                ("topic", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="quiz_sessions", to="medicaltutordjapp.topic")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="quiz_sessions", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-started_at",)},
        ),
        migrations.CreateModel(
            name="QuestionOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField()),
                ("is_correct", models.BooleanField(default=False)),
                ("explanation", models.TextField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="options", to="medicaltutordjapp.question")),
            ],
            options={"ordering": ("order", "id")},
        ),
        migrations.CreateModel(
            name="QuestionAttempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("selected_answer", models.JSONField(default=dict)),
                ("is_correct", models.BooleanField()),
                ("confidence", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("response_time_ms", models.PositiveIntegerField(blank=True, null=True)),
                ("attempted_at", models.DateTimeField(auto_now_add=True)),
                ("question", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="attempts", to="medicaltutordjapp.question")),
                ("quiz_session", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attempts", to="medicaltutordjapp.quizsession")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="question_attempts", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("attempted_at",)},
        ),
        migrations.AddField(
            model_name="question",
            name="concepts",
            field=models.ManyToManyField(blank=True, related_name="questions", to="medicaltutordjapp.concept"),
        ),
        migrations.AddIndex(
            model_name="questionattempt",
            index=models.Index(fields=("user", "attempted_at"), name="medicaltut_user_id_8d9c5e_idx"),
        ),
        migrations.AddIndex(
            model_name="questionattempt",
            index=models.Index(fields=("question", "attempted_at"), name="medicaltut_questio_ef7a7c_idx"),
        ),
    ]
