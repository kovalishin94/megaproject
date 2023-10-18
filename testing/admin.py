from django.contrib import admin
from .models import Test, Question, Choice, Vote, Result


@admin.register(Test)
class AdminTest(admin.ModelAdmin):
    pass


@admin.register(Question)
class AdminQuestion(admin.ModelAdmin):
    list_display = ["title", "order_number"]


@admin.register(Choice)
class AdminChoice(admin.ModelAdmin):
    list_display = ["title", "is_correct", "order_number"]


@admin.register(Vote)
class AdminVote(admin.ModelAdmin):
    list_display = ["employee", "question", "choice"]


@admin.register(Result)
class AdminResult(admin.ModelAdmin):
    list_display = ["employee", "test", "description"]
