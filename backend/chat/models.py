from django.db import models
from cases.models import Character


class ChatMessage(models.Model):
    """
    Foydalanuvchi va personaj orasidagi bitta xabar.
    Har bir savol va har bir javob alohida yozuv sifatida saqlanadi.
    """
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='messages')

    ROLE_CHOICES = [
        ('user', 'Foydalanuvchi'),
        ('assistant', 'Personaj'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()

    # Hozircha soddalik uchun sessiyani foydalanuvchi ID'siz kuzatamiz.
    # Keyinroq auth qo'shganimizda bu maydon foydalanuvchiga bog'lanadi.
    session_id = models.CharField(max_length=100, help_text="Brauzer sessiyasini ajratish uchun")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # xabarlar har doim vaqt tartibida chiqadi

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}"