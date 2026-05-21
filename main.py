import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ====================================
# НАСТРОЙКИ
# ====================================

TOKEN = "ТВОЙ_ТОКЕН"

# ====================================
# ЛОГИ
# ====================================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ====================================
# ДАННЫЕ
# ====================================

users = {}
admins = set()

# ====================================
# ЦЕНЫ
# ====================================

year_prices = {
    "2017-2019": 200,
    "2020-2021": 150,
    "2022-2024": 100,
    "2025": 70,
    "2026-20..": 50
}

cups_prices = {
    "1000-5000": 22,
    "5001-10000": 44,
    "10001-20000": 70,
    "20001-30000": 80,
    "30001-40000": 90,
    "40001-50000": 100,
    "50001-60000": 110,
    "60001-100000+": 120


fighters_prices = {
    "40-50": 50,
    "51-60": 60,
    "61-70": 70,
    "71-80": 80,
    "81-100+": 90

# ====================================
# МЕНЮ
# ====================================

def user_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("💰 Продать аккаунт")]
        ],
        resize_keyboard=True
    )


def admin_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("💰 Продать аккаунт")],
            [KeyboardButton("🛠 Админ панель")]
        ],
        resize_keyboard=True
    )

# ====================================
# INLINE КНОПКИ
# ====================================

def year_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("2017-2019", callback_data="year_2017-2019")],
        [InlineKeyboardButton("2020-2021", callback_data="year_2020-2021")],
        [InlineKeyboardButton("2022-2024", callback_data="year_2022-2024")],
        [InlineKeyboardButton("2025", callback_data="year_2025")],
        [InlineKeyboardButton("2026-20..", callback_data="year_2026-20..")],
        [InlineKeyboardButton("⬅ Назад", callback_data="home")]
    ])


def cups_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1000-5000", callback_data="cups_1000-5000")],
        [InlineKeyboardButton("5001-10000", callback_data="cups_5001-10000")],
        [InlineKeyboardButton("10001-20000", callback_data="cups_10001-20000")],
        [InlineKeyboardButton("20001-30000", callback_data="cups_20001-30000")],
        [InlineKeyboardButton("30001-40000", callback_data="cups_30001-40000")],
        [InlineKeyboardButton("40001-50000", callback_data="cups_40001-50000")],
        [InlineKeyboardButton("50001-60000", callback_data="cups_50001-60000")],
        [InlineKeyboardButton("60001-100000+", callback_data="cups_60001-100000+")],
        [InlineKeyboardButton("⬅ Назад", callback_data="back_year")]
    ])


def fighters_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("40-50", callback_data="fighters_40-50")],
        [InlineKeyboardButton("51-60", callback_data="fighters_51-60")],
        [InlineKeyboardButton("61-70", callback_data="fighters_61-70")],
        [InlineKeyboardButton("71-80", callback_data="fighters_71-80")],
        [InlineKeyboardButton("81-100+", callback_data="fighters_81-100+")],
        [InlineKeyboardButton("⬅ Назад", callback_data="back_cups")]
    ])

# ====================================
# START
# ====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    users[user_id] = {
        "year": "",
        "cups": "",
        "fighters": "",
        "total": 0
    }

    menu = admin_menu() if user_id in admins else user_menu()

    await update.message.reply_text(
        "👋 Добро пожаловать\n\n"
        "Нажмите кнопку ниже чтобы оценить аккаунт",
        reply_markup=menu
    )

# ====================================
# АДМИН ПАНЕЛЬ
# ====================================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    admins.add(user_id)

    await update.message.reply_text(
        "✅ Админ панель активирована",
        reply_markup=admin_menu()
    )

# ====================================
# СООБЩЕНИЯ
# ====================================

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id

    # Продать аккаунт
    if text == "💰 Продать аккаунт":

        users[user_id] = {
            "year": "",
            "cups": "",
            "fighters": "",
            "total": 0
        }

        await update.message.reply_text(
            "📅 Выберите год аккаунта",
            reply_markup=year_keyboard()
        )

    # Админ панель
    elif text == "🛠 Админ панель":

        if user_id not in admins:
            return

        await update.message.reply_text(
            f"🛠 Админ панель\n\n"
            f"Админов: {len(admins)}"
        )

# ====================================
# КНОПКИ
# ====================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in users:

        users[user_id] = {
            "year": "",
            "cups": "",
            "fighters": "",
            "total": 0
        }

    data = users[user_id]

    # Домой
    if query.data == "home":

        await query.message.edit_text(
            "🏠 Главное меню"
        )
        return

    # Назад к году
    if query.data == "back_year":

        data["total"] = 0

        await query.message.edit_text(
            "📅 Выберите год аккаунта",
            reply_markup=year_keyboard()
        )
        return

    # Назад к кубкам
    if query.data == "back_cups":

        await query.message.edit_text(
            "🏆 Выберите количество кубков",
            reply_markup=cups_keyboard()
        )
        return

    # Год
    if query.data.startswith("year_"):

        value = query.data.replace("year_", "")

        data["year"] = value
        data["total"] = year_prices[value]

        await query.message.edit_text(
            "🏆 Выберите количество кубков",
            reply_markup=cups_keyboard()
        )
        return

    # Кубки
    if query.data.startswith("cups_"):

        value = query.data.replace("cups_", "")

        data["cups"] = value
        data["total"] += cups_prices[value]

        await query.message.edit_text(
            "👤 Выберите количество бойцов",
            reply_markup=fighters_keyboard()
        )
        return

    # Бойцы
    if query.data.startswith("fighters_"):

        value = query.data.replace("fighters_", "")

        data["fighters"] = value
        data["total"] += fighters_prices[value]

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📨 Оставить заявку",
                    callback_data="send_request"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅ Назад",
                    callback_data="back_cups"
                )
            ]
        ])

        await query.message.edit_text(
            f"💰 Ваш аккаунт стоит: {data['total']}₽\n\n"
            f"Оставьте заявку по кнопке ниже",
            reply_markup=keyboard
        )
        return

    # Отправка заявки
    if query.data == "send_request":

        username = query.from_user.username

        if username:
            username_text = f"@{username}"
        else:
            username_text = f"id:{user_id}"

        request_text = (
            f"📨 НОВАЯ ЗАЯВКА\n\n"
            f"👤 Пользователь: {username_text}\n"
            f"📅 Год: {data['year']}\n"
            f"🏆 Кубки: {data['cups']}\n"
            f"👥 Бойцы: {data['fighters']}\n"
            f"💰 Цена: {data['total']}₽"
        )

        # Нет админов
        if len(admins) == 0:

            await query.message.edit_text(
                "❌ Нет активных админов\n\n"
                "Активируйте админ панель:\n"
                "/ghert868"
            )
            return

        # Отправка админам
        for admin_id in admins:

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "✅ Принять",
                        callback_data=f"accept_{user_id}"
                    ),
                    InlineKeyboardButton(
                        "❌ Отклонить",
                        callback_data=f"decline_{user_id}"
                    )
                ]
            ])

            try:

                await context.bot.send_message(
                    chat_id=admin_id,
                    text=request_text,
                    reply_markup=keyboard
                )

            except Exception as e:
                print(e)

        await query.message.edit_text(
            "✅ Заявка отправлена\n\n"
            "Ожидайте ответа администратора"
        )

        return

    # Принять
    if query.data.startswith("accept_"):

        if user_id not in admins:
            return

        buyer_id = int(
            query.data.replace("accept_", "")
        )

        try:

            await context.bot.send_message(
                buyer_id,
                "✅ Ваша заявка принята"
            )

        except:
            pass

        await query.message.edit_text(
            "✅ Заявка принята"
        )

        return

    # Отклонить
    if query.data.startswith("decline_"):

        if user_id not in admins:
            return

        buyer_id = int(
            query.data.replace("decline_", "")
        )

        try:

            await context.bot.send_message(
                buyer_id,
                "❌ Ваша заявка отклонена"
            )

        except:
            pass

        await query.message.edit_text(
            "❌ Заявка отклонена"
        )

        return

# ====================================
# ОШИБКИ
# ====================================

async def error_handler(update, context):

    print("Ошибка:", context.error)

# ====================================
# ЗАПУСК
# ====================================

def main():

    app = Application.builder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CommandHandler("ghert868", admin_panel)
    )

    # Сообщения
    app.add_handler(
        MessageHandler(
            filters.TEXT,
            messages
        )
    )

    # Кнопки
    app.add_handler(
        CallbackQueryHandler(buttons)
    )

    # Ошибки
    app.add_error_handler(error_handler)

    print("Бот запущен")

    app.run_polling(
        drop_pending_updates=True
    )

# ====================================
# MAIN
# ====================================

if __name__ == "__main__":
    main()
