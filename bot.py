import os
import random
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота (замените на ваш)
BOT_TOKEN = "8207712999:AAFq7CTfKvAYpK4cW8VnZ-b7LLHP4ZKCFS0"

# Чтение советов из файлов
def read_advice_files():
    """Чтение советов из файлов и возврат в виде кортежей"""
    
    # Чтение вредных советов
    try:
        with open('harmful_advice.txt', 'r', encoding='utf-8') as file:
            harmful_advice = tuple(line.strip() for line in file if line.strip())
    except FileNotFoundError:
        harmful_advice = (
            "Никогда не делайте резервные копии важных файлов",
            "Всегда оставляйте пароли на видном месте",
            "Пейте кофе перед сном для бодрости",
            "Откладывайте все дела на последний момент",
            "Никогда не читайте инструкции",
            "Храните все деньги дома под матрасом",
            "Ешьте фастфуд каждый день для экономии времени",
            "Не занимайтесь спортом - это утомительно",
            "Всегда соглашайтесь на сверхурочную работу без оплаты",
            "Говорите начальнику всё, что думаете"
        )
    
    # Чтение полезных советов
    try:
        with open('useful_advice.txt', 'r', encoding='utf-8') as file:
            useful_advice = tuple(line.strip() for line in file if line.strip())
    except FileNotFoundError:
        useful_advice = (
            "Регулярно делайте резервные копии важных данных",
            "Используйте сложные пароли и двухфакторную аутентификацию",
            "Соблюдайте режим сна 7-8 часов в сутки",
            "Планируйте задачи заранее и распределяйте время",
            "Читайте инструкции перед использованием новых устройств",
            "Диверсифицируйте инвестиции для снижения рисков",
            "Питайтесь сбалансированно и пейте足够 воды",
            "Занимайтесь физической активностью 30 минут в день",
            "Учитесь говорить 'нет' когда это необходимо",
            "Постоянно обучайтесь новым навыкам и знаниям"
        )
    
    return harmful_advice, useful_advice

# Загрузка советов
HARMFUL_ADVICE, USEFUL_ADVICE = read_advice_files()

# Словарь для хранения состояния пользователей
user_states = {}

# Клавиатура с кнопками
reply_keyboard = [
    ["🎁 Бесплатный совет", "💎 Платный совет"],
    ["ℹ️ О боте"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    welcome_text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Я - бот советчик! Выбери тип совета:\n"
        "🎁 Бесплатный совет - случайный вредный совет\n"
        "💎 Платный совет - полезный совет (виртуальная оплата)\n\n"
        "Просто нажми на кнопку ниже!"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    
    if text == "🎁 Бесплатный совет":
        await send_free_advice(update, context)
    elif text == "💎 Платный совет":
        await send_paid_advice(update, context)
    elif text == "ℹ️ О боте":
        await about_bot(update, context)
    else:
        await update.message.reply_text(
            "Используйте кнопки для навигации 👇",
            reply_markup=markup
        )

async def send_free_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка бесплатного (вредного) совета"""
    advice = random.choice(HARMFUL_ADVICE)
    
    response = (
        "🎁 *БЕСПЛАТНЫЙ СОВЕТ:*\n\n"
        f"⚠️ {advice}\n\n"
        "_Вредные советы могут быть опасны для вашего здоровья и благополучия!_"
    )
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def send_paid_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка платного (полезного) совета"""
    advice = random.choice(USEFUL_ADVICE)
    
    # Виртуальная "оплата"
    response = (
        "💎 *ПЛАТНЫЙ СОВЕТ:*\n\n"
        f"✅ {advice}\n\n"
        "💳 С вашего счета списано 100 монет\n"
        "_Спасибо за покупку! Возврат средств не предусмотрен._"
    )
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def about_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Информация о боте"""
    info_text = (
        "🤖 *О боте:*\n\n"
        "Этот бот выдает два типа советов:\n"
        "• 🎁 Бесплатные - вредные советы для развлечения\n"
        "• 💎 Платные - полезные советы для развития\n\n"
        "Все советы выбираются случайным образом из базы данных.\n"
        "Для начала просто выберите тип совета!"
    )
    
    await update.message.reply_text(info_text, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")
    if update and update.message:
        await update.message.reply_text(
            "Произошла ошибка. Попробуйте еще раз.",
            reply_markup=markup
        )

def main():
    """Основная функция"""
    # Создание приложения
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавление обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # Запуск бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()
