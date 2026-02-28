# my-ai-telegram-palych-bot

AI Telegram bot на Python с использованием OpenAI (Chat Completions) + Redis для хранения сессий (контекста).

Коротко: простой бот, который принимает текстовые сообщения в Telegram и пересылает контекст в OpenAI, а ответы кеширует в Redis.

---

## Что в репозитории
- `bot.py` — основной бот (polling)
- `utils/ai_client.py` — вызовы OpenAI-совместимого API
- `utils/sessions.py` — хранение истории в Redis
- `Dockerfile`, `Procfile`
- `.github/workflows/ci-deploy.yml` — CI и шаблоны деплоя
- `requirements.txt`, `tests/`

---

## Переменные окружения (обязательно)
Убедитесь, что в окружении заданы следующие переменные (имена точные):

- `BOT_TOKEN` — токен Telegram Bot (BotFather)
- `OPENAI_API_KEY` — API ключ OpenAI
- `OPENAI_API_URL` — (опционально) URL API, по умолчанию `https://api.openai.com/v1/chat/completions`
- `REDIS_URL` — URL Redis, например `redis://localhost:6379/0` или `rediss://:password@host:port/0`
- `MODEL` — (опционально) модель, по умолчанию `gpt-3.5-turbo`
- `MAX_TOKENS` — (опционально) max tokens для ответа (по умолчанию `500`)
- `SESSION_TTL` — (опционально) время жизни сессии в секундах (по умолчанию `3600`)
- `SESSION_MAX_MESSAGES` — (опционально) сколько последних сообщений хранить (по умолчанию `6`)

Пример файла `.env` (НЕ коммитьте в репозиторий):
