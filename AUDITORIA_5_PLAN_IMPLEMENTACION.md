# Auditoría 5 — Plan de implementación de Medical Tutor AI

## Objetivo

Convertir el prototipo actual en un sistema adaptativo de aprendizaje médico sin reconstruirlo desde cero ni romper las funciones existentes.

## Decisión de implementación

La transformación se hará de forma incremental sobre Django existente.

Principios:
- Mantener los modelos legacy durante la migración.
- Introducir primero el dominio educativo: Exam → Subject → Topic → Concept.
- No convertir datos históricos de Quizzes en QuestionAttempt cuando no existan respuestas individuales verificables.
- Mantener GIFT como formato de importación/exportación, no como almacenamiento principal.
- Backend como fuente de verdad para permisos, scoring, progreso, mastery y límites.
- IA separada mediante servicios/proveedores; no debe controlar reglas deterministas.
- Cada etapa debe ser reversible y acompañada de migraciones y tests.

## Estado inicial confirmado

El repositorio usa Django y una única app principal, `medicaltutordjapp`, con modelos legacy de perfil, planes, pagos, vouchers, quizzes y estadísticas.

Se confirmó un bug en `ProcessedSubmission.mark_as_processed()`: se utiliza `transaction.atomic()` sin importar `transaction`. La rama de trabajo corrige este problema sin alterar el esquema legacy.

## Rama de trabajo

`feature/medical-tutor-ai`

## Fases

### Fase 1 — Fundaciones
- Exam
- Subject
- ExamSubject
- Topic
- Concept
- StudentProfile
- migración de base de datos
- importador de `Summaries.json`
- administración Django

### Fase 2 — Question Bank
- Question
- QuestionOption
- relaciones Question ↔ Concept
- dificultad y estado editorial
- importación desde GIFT
- estados DRAFT → UNDER_REVIEW → APPROVED → REJECTED

### Fase 3 — Quiz Engine
- QuizSession
- QuestionAttempt
- respuesta seleccionada
- correctness
- confidence
- response_time_ms
- scoring determinista
- idempotencia

### Fase 4 — Learning Engine
- ConceptMastery
- ReviewSchedule
- actualización de mastery después de cada intento
- spaced repetition
- siguiente actividad recomendada

### Fase 5 — AI Layer
- AIProvider
- Tutor
- Explanation
- QuestionGenerator
- ClinicalCaseGenerator
- FeynmanEvaluator
- almacenamiento estructurado de AIConversation/AIMessage
- límites y rate limiting

### Fase 6 — UX adaptativa
- dashboard
- weak concepts
- reviews due
- daily plan
- next best activity
- progreso por examen/subject/topic/concept

### Fase 7 — Billing
- Subscription
- Usage
- Entitlements
- transición progresiva desde remaining_queries/remaining_quizzes
- Plan/Payment/Voucher conservados durante la migración

### Fase 8 — Seguridad y producción
- eliminar CSRF exemptions innecesarios
- sanitizar Markdown/HTML generado por IA
- permisos server-side
- secretos exclusivamente por entorno
- eliminar __pycache__ y artefactos generados del repositorio
- tests de seguridad y regresión

## Orden de commits previsto

1. Fundaciones de contenido + StudentProfile.
2. Migración + importador de curriculum.
3. Question Bank.
4. QuizSession + QuestionAttempt.
5. Mastery + spaced repetition.
6. Recommendations.
7. AIProvider + AIConversation.
8. Clinical/Feynman.
9. Dashboard adaptativo.
10. Subscription/Usage.
11. Seguridad y limpieza.
12. Retiro progresivo de legacy.

## Criterio de éxito

No se considera terminada una fase solo porque el código exista. Cada fase debe:
- migrar correctamente,
- tener tests,
- preservar las funciones legacy relevantes,
- poder ejecutarse con la base de datos existente,
- no exponer secretos,
- y dejar una ruta clara de rollback.

## Primera implementación realizada

En esta rama se añadieron los modelos fundacionales en `learning_models.py` y se corrigió el import de `transaction` en `models.py`.

Todavía NO se debe ejecutar `makemigrations` sobre producción ni eliminar modelos legacy. El siguiente paso técnico es convertir estos modelos en parte formal del app registry/migraciones, crear la migración y construir el importador del curriculum.

