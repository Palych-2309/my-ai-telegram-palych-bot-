import os
from dotenv import load_dotenv
from telegram import Update, ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from utils.ai_client import call_ai_api
from utils.sessions import append_user_message, append_assistant_message, get_session_messages, clear_session

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment")

SYSTEM_PROMPT = "Ты — полезный и краткий помощник. Отвечай на вопросы дружелюбно."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я AI‑бот. Отправь мне сообщение — и я отвечу. /reset — сбросить контекст.")

async def reset_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_session(update.effective_user.id)
    await update.message.reply_text("Контекст очищен.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Просто отправь сообщение. Используй /reset чтобы очистить историю.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text or ""
    if not text.strip():
        await update.message.reply_text("Пожалуйста, пришлите текст.")
        return

    if len(text) > 4000:
        await update.message.reply_text("Сообщение слишком длинное — сократите до 4000 символов.")
        return

    # Добавляем пользовательское сообщение в сессию
    append_user_message(user_id, text)

    # Получаем сообщения для отправки в OpenAI
    messages = get_session_messages(user_id, system_prompt=SYSTEM_PROMPT)

    # Показываем индикатор
    await update.message.chat.send_action(ChatAction.TYPING)

    try:
        reply = call_ai_api(messages)
    except Exception as e:
        await update.message.reply_text("Ошибка при обращении к AI: " + str(e))
        return

    # Сохраняем ответ ассистента и отправляем пользователю
    append_assistant_message(user_id, reply)
