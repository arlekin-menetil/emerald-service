from django.contrib import admin

from .models import (
    TelegramChat,
    TelegramChatMember,
    TelegramUser,
)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_id",
        "username",
        "first_name",
        "last_name",
        "is_active",
        "updated_at",
    )

    list_filter = ("is_active",)

    search_fields = (
        "telegram_id",
        "username",
        "first_name",
        "last_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = (
        "chat_id",
        "title",
        "chat_type",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "chat_type",
        "is_active",
    )

    search_fields = (
        "chat_id",
        "title",
        "username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(TelegramChatMember)
class TelegramChatMemberAdmin(admin.ModelAdmin):
    list_display = (
        "chat",
        "user",
        "is_active",
        "joined_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "chat",
    )

    search_fields = (
        "chat__title",
        "chat__chat_id",
        "user__telegram_id",
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    readonly_fields = (
        "joined_at",
        "updated_at",
    )
