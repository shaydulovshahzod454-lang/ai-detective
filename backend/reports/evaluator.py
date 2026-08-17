from chat.ai_service import client
import json


def sanitize_feedback(feedback, case, is_correct):
    """
    Agar o'yinchi XATO topgan bo'lsa, feedback matnida haqiqiy aybdorning
    ismi tasodifan chiqib qolmaganini tekshiradi. Agar chiqsa — umumiy,
    xavfsiz xabar bilan almashtiradi.

    Bu — AI prompt'iga qo'shimcha, ikkinchi himoya qatlami: LLM 100%
    ishonchli emas, shuning uchun eng kritik holatni (aybdor ismining
    sizib chiqishi) kod darajasida ham tekshiramiz.
    """
    if is_correct:
        return feedback

    guilty_characters = case.characters.filter(is_guilty=True)
    for character in guilty_characters:
        if character.name.lower() in feedback.lower():
            return (
                "Bu safar noto'g'ri topdingiz. Personajlar bilan yana gaplashib, "
                "ularning aytganlarini diqqat bilan qayta tahlil qiling."
            )

    return feedback


def evaluate_report(case, accused_character_name, reasoning):
    prompt = f"""
Sen detektiv o'yinining "sudyasi"san. Sening vazifang — o'yinchi yozgan hisobotni
haqiqiy yechim bilan solishtirib, baho berish.

HAQIQIY YECHIM (bu QATTIQ MAXFIY, hech qachon to'g'ridan-to'g'ri yoki
bilvosita oshkor qilma):
{case.solution}

O'YINCHI HISOBOTI:
Aybdor deb ko'rsatilgan: {accused_character_name}
Asoslash: {reasoning}

VAZIFANG:
1. O'yinchi to'g'ri odamni aybdor deb ko'rsatganmi, tekshir.
2. Uning asoslashi haqiqiy sabab bilan mos keladimi, baholab ber.

FEEDBACK YOZISHDA QATTIQ QOIDALAR:
- Agar o'yinchi TO'G'RI topgan bo'lsa: tabriklab, nima uchun to'g'ri
  ekanini tushuntirsang bo'ladi (chunki o'yin allaqachon tugadi).
- Agar o'yinchi XATO topgan bo'lsa: FAQAT shuni ayt — bu odam aybdor
  emasligini, va o'yinchini boshqa personajlar bilan yana gaplashib,
  ularning javoblarini diqqat bilan qayta ko'rib chiqishga undang.
  QATʼIYAN TAQIQLANADI:
  * haqiqiy aybdorning ismini aytish
  * haqiqiy sababni, motivni yoki unga oid har qanday tafsilotni
    aytish yoki unga ishora qilish (masalan sabab pul, kek, sevgi,
    ish haqi va h.k. bo'lsa — buni umuman tilga OLMA)
  * qaysi personajga yoki qaysi mavzuga e'tibor berish kerakligini
    aniq ko'rsatish
  Faqat umumiy, hech qanday maxsus yo'nalish bermaydigan rag'batlantiruvchi
  gap yoz.
3. Qisqa va o'zbek tilida yoz.

JAVOBINI FAQAT quyidagi JSON formatida qaytar, boshqa hech qanday matn yozma:
{{
  "is_correct": true yoki false,
  "feedback": "o'zbek tilidagi tushunarli fikr-mulohaza"
}}
""".strip()

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)
    is_correct = result['is_correct']
    feedback = result['feedback']

    # Ikkinchi himoya qatlami — kod darajasida tekshirish
    feedback = sanitize_feedback(feedback, case, is_correct)

    return is_correct, feedback