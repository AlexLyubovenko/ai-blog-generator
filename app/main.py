from fastapi import FastAPI
import uvicorn
from app.config import settings
from app.services.telegram_service import TelegramService

app = FastAPI()

# Инициализация Telegram сервиса
telegram_service = TelegramService(settings.telegram_bot_token, settings.telegram_chat_id)

@app.get("/")
def root():
    return {"message": "With TelegramService - WORKS"}

@app.get("/telegram-test")
async def telegram_test():
    try:
        # Тест подключения к Telegram
        connected = await telegram_service.test_connection()
        return {
            "status": "telegram_test_works",
            "telegram_connected": connected,
            "bot_token_set": bool(settings.telegram_bot_token)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/send-test-message")
async def send_test_message():
    """Отправка тестового сообщения в Telegram"""
    try:
        result = await telegram_service.send_message(
            message="🤖 Тестовое сообщение от бота!\n\nБот успешно настроен и готов к работе! 🚀",
            title="Тест бота"
        )
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}