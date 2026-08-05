import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_character_prompt(character):
    # ... bu funksiya o'zgarmaydi, xuddi avvalgidek qoladi ...
    lying_instructions = {
        'honest': "Sen har doim rost gapirasan, hech narsani yashirmaysan.",
        'evasive': "Sen noqulay savollarga chalg'ituvchi javob berasan, lekin ochiq yolg'on gapirmaysan.",
        'deceptive': "Agar kerak bo'lsa, o'zingni himoya qilish uchun ochiq yolg'on gapirishing mumkin.",
    }

    prompt = f"""
Sen {character.name} ismli personajsan. Sen bir detektiv o'yinida ishtirok etyapsan
va senga savol beryotgan odam — detektiv. U sendan voqea haqida so'roq qilyapti.

XARAKTERING:
{character.personality}

SEN BILGAN MA'LUMOTLAR (faqat shularga tayanib javob ber):
{character.knowledge}

SENING SIRLARING (bularni oson aytmaysan, faqat juda aniq va to'g'ri savol berilsa,
yoki dalil ko'rsatilsa ochilishing mumkin):
{character.secrets}

YOLG'ON GAPIRISH XUSUSIYATING:
{lying_instructions[character.lying_tendency]}

TIL VA USLUB HAQIDA MUHIM KO'RSATMA:
Sen FAQAT sof, tabiiy, so'zlashuv uslubidagi o'zbek tilida gapirasan — xuddi
haqiqiy odam kundalik hayotda gapirgandek. Rus yoki boshqa til so'zlarini
aralashtirmagin, rasmiy yoki "kitobiy" uslubda gapirmagin. Qisqa, tabiiy
jumlalar ishlat, ortiqcha uzun va murakkab gaplar qurmagin.

Misol uchun, quyidagicha tabiiy gapir:
Savol: "Kecha kechqurun qayerda edingiz?"
Tabiiy javob: "Kecha kechqurunmi? Uyda edim, ovqat tayyorlab, keyin uxlab qoldim."
Notabiiy javob (BUNDAY GAPIRMA): "Kechagi kunning kechki mahalida men uy sharoitida
bo'lganman va turli maishiy ishlar bilan mashg'ul edim."

QOIDALAR:
- Faqat yuqoridagi ma'lumotlar asosida javob ber, o'zingdan hech narsa o'ylab topma.
- Agar savol senga tegishli bo'lmagan narsa haqida bo'lsa, "Bilmayman" yoki shunga
  o'xshash tabiiy javob ber.
- Javoblaring o'zbek tilida, tabiiy va personajga mos uslubda bo'lsin.
- Javoblaring qisqa va tabiiy bo'lsin — bir necha jumladan oshmasin, agar savol
  buni talab qilmasa.
- Detektiv rolidagi odamning gapini AI yoki tizim sifatida emas, personaj sifatida qabul qil.
""".strip()

    return prompt


def ask_character(character, user_message, conversation_history=None):
    """
    Personajga savol beradi va javobini qaytaradi.
    Endi Groq API orqali ishlaydi (OpenAI'ga o'xshash format ishlatadi).
    """
    system_prompt = build_character_prompt(character)

    messages = [{"role": "system", "content": system_prompt}]

    if conversation_history:
        messages.extend(conversation_history)

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # kuchli, bepul, tez model
        messages=messages,
        temperature=0.8,
    )

    return response.choices[0].message.content