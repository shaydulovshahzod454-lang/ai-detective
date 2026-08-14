from django.db import models
from django.contrib.auth.models import User

class Case(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    solution = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ↓ YANGI MAYDON
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_cases',
        null=True, blank=True   # eski case'lar uchun bo'sh qolishi mumkin
    )

    def __str__(self):
        return self.title


class Scene(models.Model):
    """
    Case ichidagi bitta joy/xona (masalan: "Mehmonxona", "Bog'").
    Har bir case bir nechta scene'ga ega bo'lishi mumkin.
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='scenes')
    name = models.CharField(max_length=100)          # masalan: "Kutubxona"
    description = models.TextField(blank=True)                  # xona haqida qisqacha matn
    background_image = models.ImageField(upload_to='scenes/', blank=True, null=True)

    def __str__(self):
        return f"{self.case.title} — {self.name}"


class Character(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='characters')
    scene = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True, blank=True, related_name='characters')

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='characters/', blank=True, null=True)

    personality = models.TextField(help_text="Personajning xarakteri, gapirish uslubi")
    knowledge = models.TextField(help_text="Personaj biladigan haqiqiy ma'lumotlar")
    secrets = models.TextField(help_text="Personaj yashiradigan, oson aytmaydigan sirlar")

    # ↓ YANGI MAYDONLAR
    alibi = models.TextField(
        blank=True,
        help_text="Voqea kuni qayerda, qachon nima qilgani (vaqt bilan yozing, masalan: 20:00 — oshxonada edim)"
    )
    relationships = models.TextField(
        blank=True,
        help_text="Boshqa personajlar bilan munosabati (masalan: Xizmatkorni yoqtirmaydi, chunki...)"
    )

    is_guilty = models.BooleanField(default=False, help_text="Bu personaj aybdormi?")
    lying_tendency = models.CharField(
        max_length=20,
        choices=[
            ('honest', "Har doim rost gapiradi"),
            ('evasive', "Savolni chalg'itadi, lekin ochiq yolg'on gapirmaydi"),
            ('deceptive', "Kerak bo'lsa ochiq yolg'on gapiradi"),
        ],
        default='honest',
    )

    def __str__(self):
        return f"{self.name} ({self.case.title})"

class Clue(models.Model):
    """
    Foydalanuvchi suhbat davomida muhim deb belgilagan dalil.
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='clues')
    session_id = models.CharField(max_length=100)  # qaysi o'yinchiga tegishli

    text = models.TextField(help_text="Foydalanuvchi yozgan dalil matni")
    source_character = models.ForeignKey(
        Character, on_delete=models.SET_NULL, null=True, blank=True,
        help_text="Bu dalil qaysi personajdan olingan"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.text[:50]}"

class CaseCollaborator(models.Model):
    """
    Bitta case'ga qaysi foydalanuvchi tahrirlash huquqiga ega ekanini bildiradi.
    Case egasi (created_by) bu yerda alohida yozilmaydi — u har doim
    avtomatik ravishda to'liq huquqqa ega.
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='collaborators')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaborations')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Bir foydalanuvchi bitta case'ga faqat bir marta qo'shilishi mumkin
        unique_together = ('case', 'user')

    def __str__(self):
        return f"{self.user.username} → {self.case.title}"