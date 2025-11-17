import os
from typing import Optional
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()


class Settings:
    """Класс для управления конфигурацией приложения"""

    def __init__(self):
        # API Keys
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        self.currents_api_key: Optional[str] = os.getenv("CURRENTS_API_KEY")
        self.telegram_bot_token: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")

        # Server settings
        self.host: str = os.getenv("HOST", "0.0.0.0")
        self.port: int = int(os.getenv("PORT", "8000"))
        self.debug: bool = os.getenv("DEBUG", "False").lower() == "true"

        # API Settings
        self.default_openai_model: str = os.getenv("DEFAULT_OPENAI_MODEL", "gpt-4-1106-preview")
        self.max_news_articles: int = int(os.getenv("MAX_NEWS_ARTICLES", "5"))
        self.default_language: str = os.getenv("DEFAULT_LANGUAGE", "en")

        # Вывод отладочной информации
        print("🔧 Configuration loaded:")
        print(f"   - OpenAI API: {'✅' if self.openai_api_key else '❌'}")
        print(f"   - Currents API: {'✅' if self.currents_api_key else '❌'}")
        print(f"   - Telegram Bot: {'✅' if self.telegram_bot_token else '❌'}")

    def get_openai_api_key(self) -> str:
        """Получение OpenAI API ключа с валидацией"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY не установлен")
        return self.openai_api_key

    def get_currents_api_key(self) -> str:
        """Получение Currents API ключа с валидацией"""
        if not self.currents_api_key:
            raise ValueError("CURRENTS_API_KEY не установлен")
        return self.currents_api_key

    def get_telegram_config(self) -> tuple[Optional[str], Optional[str]]:
        """Получение конфигурации Telegram"""
        return self.telegram_bot_token, self.telegram_chat_id


# Глобальный экземпляр настроек
settings = Settings()