from django.contrib import admin
from .models import Case, Scene, Character


class SceneInline(admin.TabularInline):
    """
    Case tahrirlash sahifasida Scene'larni ham
    o'sha yerning o'zida (jadval ko'rinishida) qo'shish imkonini beradi.
    """
    model = Scene
    extra = 1  # bo'sh qator soni, tezroq qo'shish uchun


class CharacterInline(admin.TabularInline):
    """
    Case tahrirlash sahifasida Character'larni ham
    o'sha yerning o'zida qo'shish imkonini beradi.
    """
    model = Character
    extra = 1


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')  # ro'yxatda qaysi ustunlar ko'rinishi
    inlines = [SceneInline, CharacterInline]              # Case sahifasida Scene va Character ham chiqadi


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('name', 'case')


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'case', 'is_guilty', 'lying_tendency')
    list_filter = ('is_guilty', 'lying_tendency')  # o'ng tomonda filtr paneli chiqadi