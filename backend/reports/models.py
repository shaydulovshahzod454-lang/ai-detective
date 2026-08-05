from django.db import models
from cases.models import Case


class Report(models.Model):
    """
    Foydalanuvchi yozgan yakuniy hisobot va AI'ning bahosi.
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='reports')
    session_id = models.CharField(max_length=100)

    accused_character_name = models.CharField(max_length=100, help_text="Foydalanuvchi kim aybdor deb hisoblaydi")
    reasoning = models.TextField(help_text="Foydalanuvchining asoslashi")

    # AI bahosi shu yerga saqlanadi
    is_correct = models.BooleanField(null=True, blank=True)
    ai_feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Hisobot: {self.case.title} — {self.session_id}"