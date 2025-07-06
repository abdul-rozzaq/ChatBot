from django.contrib import admin

from bot.models import BotUser, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ["role", "content", "created_at"]
    can_delete = False
    show_change_link = True


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ["pk", "telegram_id", "first_name", "last_name", "username", "language", "role"]
    search_fields = ["telegram_id", "first_name", "last_name", "username"]
    list_filter = ["language", "role"]
    readonly_fields = ["telegram_id"]
    inlines = [ChatMessageInline]
    ordering = ["-pk"]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "role", "content", "created_at"]
    list_filter = ["user", "role"]
    search_fields = ["user__telegram_id", "content"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
