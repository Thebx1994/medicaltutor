from django.core.management.base import BaseCommand
from django.db import transaction

from medicaltutordjapp.learning_models import Concept, Exam, ExamSubject, Subject, Topic
from medicaltutordjapp.question_models import Question, QuestionOption


class Command(BaseCommand):
    help = "Creates a small ENARM demo curriculum and approved questions."

    @transaction.atomic
    def handle(self, *args, **options):
        exam, _ = Exam.objects.get_or_create(
            code="ENARM",
            defaults={
                "name": "ENARM",
                "country": "México",
                "description": "Demo curriculum para preparación médica.",
                "active": True,
            },
        )

        data = {
            "Cardiología": [
                ("Síndrome coronario agudo", [
                    ("¿Cuál es el biomarcador preferido para detectar necrosis miocárdica?", [
                        ("Troponina cardíaca", True),
                        ("Dímero D", False),
                        ("Amilasa", False),
                        ("Bilirrubina", False),
                    ], "La troponina cardíaca es el biomarcador de elección por su alta sensibilidad y especificidad."),
                    ("En un paciente con dolor torácico, ¿qué hallazgo orienta a elevación del ST?", [
                        ("Elevación del segmento ST en derivaciones contiguas", True),
                        ("QT corto aislado", False),
                        ("Onda U prominente", False),
                        ("PR prolongado exclusivamente", False),
                    ], "La elevación del ST en derivaciones anatómicamente contiguas es un hallazgo electrocardiográfico característico del STEMI."),
                ]),
            ],
            "Endocrinología": [
                ("Diabetes mellitus", [
                    ("¿Cuál es el mecanismo principal de la cetoacidosis diabética?", [
                        ("Deficiencia de insulina con aumento de cetogénesis", True),
                        ("Exceso aislado de hormona tiroidea", False),
                        ("Deficiencia primaria de cortisol", False),
                        ("Aumento de síntesis de glucógeno", False),
                    ], "La deficiencia de insulina favorece lipólisis y cetogénesis, produciendo acidosis metabólica."),
                    ("¿Qué hormona disminuye la glucemia al favorecer la captación de glucosa?", [
                        ("Insulina", True),
                        ("Glucagón", False),
                        ("Cortisol", False),
                        ("Adrenalina", False),
                    ], "La insulina facilita la captación y utilización de glucosa y reduce la producción hepática de glucosa."),
                ]),
            ],
            "Infectología": [
                ("Infecciones bacterianas", [
                    ("¿Qué estructura bacteriana contiene peptidoglucano?", [
                        ("Pared celular", True),
                        ("Ribosoma 80S", False),
                        ("Núcleo", False),
                        ("Mitocondria", False),
                    ], "El peptidoglucano es un componente estructural de la pared celular bacteriana."),
                ]),
            ],
        }

        for subject_order, (subject_name, topics) in enumerate(data.items(), start=1):
            subject, _ = Subject.objects.get_or_create(
                code=subject_name[:20].upper().replace(" ", "_"),
                defaults={"name": subject_name, "order": subject_order, "active": True},
            )
            ExamSubject.objects.get_or_create(exam=exam, subject=subject)

            for topic_order, (topic_name, question_data) in enumerate(topics, start=1):
                topic, _ = Topic.objects.get_or_create(
                    subject=subject,
                    slug=topic_name.lower().replace(" ", "-"),
                    defaults={"name": topic_name, "order": topic_order, "active": True},
                )

                for concept_name in [topic_name]:
                    concept, _ = Concept.objects.get_or_create(
                        topic=topic,
                        name=concept_name,
                        defaults={"order": 1, "active": True},
                    )

                for stem, options, explanation in question_data:
                    question, created = Question.objects.get_or_create(
                        stem=stem,
                        defaults={
                            "question_type": "single_choice",
                            "explanation": explanation,
                            "difficulty": "medium",
                            "status": "approved",
                            "source": "Medical Tutor demo",
                            "subject": subject,
                            "topic": topic,
                        },
                    )
                    question.concepts.add(concept)
                    if created:
                        for order, (text, is_correct) in enumerate(options, start=1):
                            QuestionOption.objects.create(
                                question=question,
                                text=text,
                                is_correct=is_correct,
                                order=order,
                            )

        self.stdout.write(self.style.SUCCESS(
            "Demo ENARM creado. Inicia sesión y abre /dashboard/ para probar el flujo."
        ))
