import logging
from telegram import Bot
from telegram.error import TelegramError
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


class TelegramService:
    """Класс для работы с Telegram API"""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token) if bot_token else None

    async def send_message(self, message: str, title: str = None) -> dict:
        """
        Отправка сообщения в Telegram канал

        Args:
            message: Текст сообщения
            title: Заголовок (опционально)

        Returns:
            dict: Результат отправки
        """
        if not self.bot or not self.chat_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Telegram бот не настроен"
            )

        try:
            formatted_message = f"<b>{title}</b>\n\n{message}" if title else message

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=formatted_message,
                parse_mode="HTML"
            )

            logger.info(f"✅ Сообщение отправлено в Telegram канал: {title}")
            return {"status": "success", "message": "Сообщение отправлено в Telegram"}

        except TelegramError as e:
            logger.error(f"❌ Ошибка Telegram: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка отправки в Telegram: {str(e)}"
            )
        except Exception as e:
            logger.error(f"❌ Неожиданная ошибка: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка отправки: {str(e)}"
            )

    async def test_connection(self) -> bool:
        """Проверка подключения к Telegram"""
        try:
            if self.bot and self.chat_id:
                bot_info = await self.bot.get_me()
                chat = await self.bot.get_chat(self.chat_id)
                return True
            return False
        except:
            return False