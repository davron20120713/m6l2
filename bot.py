import telebot
import time
import os
from logic import FusionBrainAPI
from confic import TOKEN, API_KEY, SECRET_KEY

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# ---------------- Задание 1 ----------------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! 👋 Я бот, который генерирует картинки по твоему описанию.\n\n"
        "Просто напиши мне, что ты хочешь увидеть 🖼️\n"
        "Команды:\n"
        "• /start или /help — показать помощь\n"
    )

# ---------------- Задание 2, 3, 4 ----------------
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text

    # эффект "печатает..."
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)

    # временное сообщение "Генерирую картинку.."
    msg = bot.send_message(message.chat.id, "⏳ Генерирую картинку..")

    try:
        # Генерация картинки через API
        api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
        pipeline_id = api.get_pipeline()
        uuid = api.generate(prompt, pipeline_id)
        files = api.check_generation(uuid)[0]

        # сохраняем на диск
        file_path = "generated_image.jpg"
        api.save_image(files, file_path)

        # отправляем пользователю
        with open(file_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

        # удаляем картинку после отправки (экономия места)
        if os.path.exists(file_path):
            os.remove(file_path)

    finally:
        # удаляем сообщение "Генерирую картинку.."
        try:
            bot.delete_message(message.chat.id, msg.message_id)
        except:
            pass

# ---------------- Запуск ----------------
print("Бот запущен...")
bot.polling(none_stop=True)
