from django.db import models


class Case(models.Model):
    """
    Bitta detektiv ish (masalan: "Qotillik villada").
    Bu — o'yinning eng yuqori darajadagi obyekti.
    """
    title = models.CharField(max_length=200)  # ish nomi
    description = models.TextField()          # o'yinchiga ko'rsatiladigan qisqacha voqea
    solution = models.TextField()              # asl haqiqat — kim, nima uchun (AI hisobotni shu bilan solishtiradi)
    is_active = models.BooleanField(default=True)  # o'yinda ko'rinsinmi yoki yo'q
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Django admin panelida va konsolda ob'ekt shu nom bilan ko'rinadi
        return self.title


class Scene(models.Model):
    """
    Case ichidagi bitta joy/xona (masalan: "Mehmonxona", "Bog'").
    Har bir case bir nechta scene'ga ega bo'lishi mumkin.
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='scenes')
    name = models.CharField(max_length=100)          # masalan: "Kutubxona"
    description = models.TextField()                  # xona haqida qisqacha matn
    background_image = models.ImageField(upload_to='scenes/', blank=True, null=True)

    def __str__(self):
        return f"{self.case.title} — {self.name}"


class Character(models.Model):
    """
    Case ichidagi AI orqali jonlanadigan personaj.
    """
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='characters')
    scene = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True, blank=True, related_name='characters')

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='characters/', blank=True, null=True)

    personality = models.TextField(help_text="Personajning xarakteri, gapirish uslubi")
    knowledge = models.TextField(help_text="Personaj biladigan haqiqiy ma'lumotlar")
    secrets = models.TextField(help_text="Personaj yashiradigan, oson aytmaydigan sirlar")
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