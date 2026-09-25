from django.contrib import admin
from .models import (
    Concept,
    Exam,
    ExamSubject,
    Payment,
    Plan,
    Subject,
    Topic,
    Voucher,
)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "country", "active")
    list_filter = ("active", "country")
    search_fields = ("name", "code")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "order", "active")
    list_filter = ("active",)
    search_fields = ("name", "code")
    ordering = ("order", "name")


@admin.register(ExamSubject)
class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = ("exam", "subject", "weight", "order")
    list_filter = ("exam", "subject")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "order", "active")
    list_filter = ("subject", "active")
    search_fields = ("name", "slug")
    ordering = ("subject", "order", "name")


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ("name", "topic", "order", "active")
    list_filter = ("topic__subject", "active")
    search_fields = ("name",)
    ordering = ("topic", "order", "name")


@admin.register(Plan)
class PlansAdmin(admin.ModelAdmin):
    list_display = ("plan_id", "plan_name", "receiver_id_card", "qr_code", "phone_number", "price", "max_queries", "max_quizzes")
    list_editable = ("plan_name", "receiver_id_card", "qr_code", "phone_number", "price", "max_queries", "max_quizzes")


@admin.register(Payment)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ("payment_id", "user", "transaction_id", "receiver_id_card", "amount", "payment_date")
    readonly_fields = ("payment_id", "user", "transaction_id", "receiver_id_card", "amount", "payment_date")
    search_fields = ("user__username", "transaction_id")


@admin.register(Voucher)
class VouchersAdmin(admin.ModelAdmin):
    list_display = ("voucher_id", "transaction_id", "card_id", "amount", "created_at", "used")
    readonly_fields = ("voucher_id", "transaction_id", "card_id", "amount", "created_at", "used")
    search_fields = ("transaction_id",)
