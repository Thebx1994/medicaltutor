from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .learning_models import Concept, Exam, StudentProfile, Subject, Topic
from .question_models import Question, QuestionAttempt, QuizSession


@login_required
def dashboard(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    exam = profile.target_exam
    subjects = Subject.objects.filter(active=True).order_by("order", "name")

    attempts = QuestionAttempt.objects.filter(user=request.user)
    total_attempts = attempts.count()
    correct_attempts = attempts.filter(is_correct=True).count()
    accuracy = round((correct_attempts / total_attempts) * 100, 1) if total_attempts else 0

    concept_rows = (
        Concept.objects.filter(questions__attempts__user=request.user)
        .annotate(
            attempts_count=Count(
                "questions__attempts",
                filter=Q(questions__attempts__user=request.user),
                distinct=True,
            ),
            correct_count=Count(
                "questions__attempts",
                filter=Q(
                    questions__attempts__user=request.user,
                    questions__attempts__is_correct=True,
                ),
                distinct=True,
            ),
        )
        .filter(attempts_count__gt=0)
        .order_by("correct_count", "-attempts_count")[:5]
    )

    return render(request, "medicaltutordjapp/dashboard.html", {
        "profile": profile,
        "exam": exam,
        "subjects": subjects,
        "total_attempts": total_attempts,
        "accuracy": accuracy,
        "concept_rows": concept_rows,
    })


@login_required
def quiz(request):
    subject_id = request.GET.get("subject")
    topic_id = request.GET.get("topic")

    subject = get_object_or_404(Subject, pk=subject_id) if subject_id else None
    topic = get_object_or_404(Topic, pk=topic_id) if topic_id else None

    questions = Question.objects.filter(
        status="approved",
        subject=subject if subject else None,
    ).prefetch_related("options", "concepts")

    if topic:
        questions = questions.filter(topic=topic)
    elif not subject:
        questions = Question.objects.filter(status="approved").prefetch_related("options", "concepts")

    questions = list(questions.order_by("?")[:5])

    if not questions:
        return render(request, "medicaltutordjapp/quiz.html", {
            "questions": [],
            "subject": subject,
            "topic": topic,
            "message": "Todavía no hay preguntas aprobadas para este filtro.",
        })

    if request.method == "POST":
        quiz_session = QuizSession.objects.create(
            user=request.user,
            subject=subject,
            topic=topic,
        )

        correct = 0
        for question in questions:
            selected = request.POST.get(f"question_{question.id}", "")
            correct_option = question.options.filter(is_correct=True).first()
            is_correct = bool(correct_option and selected == str(correct_option.id))
            correct += int(is_correct)

            QuestionAttempt.objects.create(
                user=request.user,
                quiz_session=quiz_session,
                question=question,
                selected_answer={"option_id": selected},
                is_correct=is_correct,
            )

        quiz_session.completed_at = timezone.now()
        quiz_session.score = round((correct / len(questions)) * 100, 2)
        quiz_session.save(update_fields=["completed_at", "score"])

        return render(request, "medicaltutordjapp/quiz_result.html", {
            "quiz_session": quiz_session,
            "correct": correct,
            "total": len(questions),
            "percentage": quiz_session.score,
            "questions": questions,
        })

    return render(request, "medicaltutordjapp/quiz.html", {
        "questions": questions,
        "subject": subject,
        "topic": topic,
    })
