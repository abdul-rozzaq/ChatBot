from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BotUser(BaseModel):
    ROLE_CHOICES = [
        ("user", "Foydalanuvchi"),
        ("admin", "Admin"),
    ]

    LANGUAGE_CHOICES = [
        ("uz", "O'zbekcha"),
        ("ru", "Русский"),
        ("en", "English"),
    ]

    telegram_id = models.BigIntegerField(unique=True)

    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    username = models.CharField(max_length=256, null=True, blank=True)

    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="uz")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    def __str__(self):
        return f"{self.first_name} ({self.telegram_id})"


class ChatMessage(BaseModel):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    content = models.TextField()

    def __str__(self):
        return str(self.user)
