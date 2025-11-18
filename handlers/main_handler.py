from aiogram import Router, types
from aiogram.filters import Command
import random
import datetime

router = Router()

# --- БАЗА ФРАЗ ---
answers = [
    "Да.",
    "Нет.",
    "Хуй его знает, брат.",
    "Определённо да.",
    "Никаких шансов.",
    "Вселенная говорит ДА.",
    "Лучше не спрашивай такое.",
    "Шансы 50/50.",
    "Сегодня — да.",
    "Сегодня — нет.",
    "Да, но будь осторожен.",
    "Не сегодня.",
    "Интуиция шепчет: да.",
]

eightball = [
    "Бесспорно.",
    "Определённо да.",
    "Никаких сомнений.",
    "Да — однозначно.",
    "Можешь быть уверен.",
    "Как мне кажется — да.",
    "Пока не ясно, попробуй снова.",
    "Спроси позже.",
    "Лучше не говорить.",
    "Говно вопрос, спроси ещё раз.",
    "Не рассчитывай на это.",
    "Мой ответ — нет.",
    "Сомнительно.",
]

predictions_for_users = [
    "{user} сегодня найдёт удачу.",
    "{user} сегодня заебёт всех вопросами.",
    "{user} сегодня будет максимально счастлив.",
    "{user} сегодня словит кринж.",
    "{user} сегодня избежит проблем.",
    "{user} сегодня сделает правильный выбор.",
    "{user} сегодня пойдёт ва-банк.",
]

fortune_cache = {}

# ------------- /ask -------------
@router.message(Command("ask"))
async def ask(message: types.Message):
    text = message.text or ""
    parts = text.split(" ", 1)

    if len(parts) == 1:
        return await message.reply("❓ Ты не написал вопрос.\nПример: `/ask будет успех?`")

    question = parts[1].strip()
    answer = random.choice(answers)

    await message.reply(
        f"❓ Вопрос: {question}\n🔮 Предсказание: {answer}"
    )

# ------------- /fortune -------------
@router.message(Command("fortune"))
async def fortune(message: types.Message):
    user = message.from_user
    if user is None:
        return await message.reply("Не удалось определить пользователя, попробуй ещё раз.")
    user_id = user.id
    today = datetime.date.today()

    if user_id in fortune_cache and fortune_cache[user_id]["date"] == today:
        return await message.reply(f"🌟 Твоё предсказание на сегодня:\n{fortune_cache[user_id]['text']}")

    luck = random.randint(0, 100)
    mood = random.choice(["🔥 огонь", "💀 хардкор", "😎 чилл", "✨ магия", "⚡ заряд", "💫 космос"])

    text = (
        f"✨ Удача: {luck}%\n"
        f"💫 Вайб дня: {mood}\n"
        f"🧿 Совет: оставайся на сильном вайбе."
    )

    fortune_cache[user_id] = {"date": today, "text": text}

    await message.reply(f"🌟 Твоё предсказание на сегодня:\n{text}")

# ------------- /8ball -------------
@router.message(Command("8ball"))
async def ball(message: types.Message):
    answer = random.choice(eightball)
    await message.reply(f"🎱 Магический шар говорит: {answer}")

# ------------- /predict -------------
@router.message(Command("predict"))
async def predict(message: types.Message):
    if not message.entities or len(message.entities) < 2:
        return await message.reply("Используй так:\n/predict @username")

    try:
        entity = message.entities[1]
        user = getattr(entity, "user", None)
    except:
        return await message.reply("Тегни человека нормально, брат.")

    text_content = message.text or ""
    if user is not None:
        name = user.full_name
    else:
        offset = getattr(entity, "offset", 0)
        length = getattr(entity, "length", len(text_content) - offset)
        name = text_content[offset: offset + length]

    text = random.choice(predictions_for_users).format(user=name)
    await message.reply(f"🔮 {text}")

# ------------- /rate_question -------------
@router.message(Command("rate_question"))
async def rate_question(message: types.Message):
    rate = random.randint(0, 100)
    await message.reply(f"📊 Оценка твоего вопроса: {rate}/100")

# ------------- /help -------------
@router.message(Command("help"))
async def help_cmd(message: types.Message):
    text = (
        "📘 Список команд:\n\n"
        "/ask - задать вопрос\n"
        "/fortune - предсказание дня\n"
        "/8ball - магический шар\n"
        "/predict @user - предсказать судьбу человека\n"
        "/rate_question - оценить вопрос\n"
        "/help - список команд"
    )
    await message.reply(text)

# ----------- РЕГИСТРАЦИЯ ХЕНДЛЕРОВ -----------
def register_handlers_main(dp):
    dp.include_router(router)
