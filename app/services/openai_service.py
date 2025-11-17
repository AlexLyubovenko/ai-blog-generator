import logging
from typing import List, Dict, Any
from datetime import datetime
import openai
from fastapi import HTTPException, status

from app.models.schemas import GeneratedPostResponse

logger = logging.getLogger(__name__)


class OpenAIContentGenerator:
    """Класс для генерации контента через OpenAI API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.available_models = ["gpt-4", "gpt-4-1106-preview", "gpt-3.5-turbo"]
        self.default_model = "gpt-4-1106-preview"

    def generate_blog_post(self,
                           topic: str,
                           news_articles: List[Dict[str, Any]],
                           writing_style: str = "professional") -> GeneratedPostResponse:
        """
        Генерация блог-поста на основе темы и новостей

        Args:
            topic: Тема поста
            news_articles: Список новостных статей для контекста
            writing_style: Стиль написания

        Returns:
            GeneratedPostResponse: Сгенерированный пост с метаданными
        """
        try:
            # Подготовка контекста из новостей
            news_context = self._prepare_news_context(news_articles)

            # Генерация заголовка
            title = self._generate_title(topic, news_context, writing_style)

            # Генерация мета-описания
            meta_description = self._generate_meta_description(title, writing_style)

            # Генерация основного контента
            content = self._generate_content(topic, title, news_context, writing_style)

            # Подготовка ответа
            return GeneratedPostResponse(
                topic=topic,
                title=title,
                content=content,
                meta_description=meta_description,
                news_used=[article["title"] for article in news_articles],
                generated_at=datetime.now(),
                tokens_used=1500,  # Можно получить из response.usage.total_tokens
                writing_style=writing_style
            )

        except openai.error.AuthenticationError:
            logger.error("Ошибка аутентификации OpenAI API")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный API ключ OpenAI"
            )
        except openai.error.RateLimitError:
            logger.error("Превышен лимит запросов к OpenAI API")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Превышен лимит запросов к OpenAI API. Попробуйте позже."
            )
        except openai.error.APIError as e:
            logger.error(f"Ошибка OpenAI API: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Ошибка OpenAI API: {str(e)}"
            )
        except openai.error.InvalidRequestError as e:
            logger.error(f"Неверный запрос к OpenAI API: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Неверный запрос: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Неожиданная ошибка при генерации контента: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка генерации контента: {str(e)}"
            )

    def _prepare_news_context(self, news_articles: List[Dict[str, Any]]) -> str:
        """Подготовка контекста из новостных статей"""
        if not news_articles:
            return "Актуальные новости по данной теме не найдены."

        context = "📰 Актуальные новости по теме:\n\n"
        for i, article in enumerate(news_articles, 1):
            context += f"• {article['title']}\n"
            if article['description'] and article['description'] != "Без описания":
                context += f"  {article['description']}\n"
            context += "\n"

        return context

    def _generate_title(self, topic: str, news_context: str, writing_style: str) -> str:
        """Генерация заголовка для поста"""

        style_prompts = {
            "professional": "создай профессиональный и информативный заголовок",
            "casual": "создай непринужденный и привлекательный заголовок",
            "creative": "создай креативный и запоминающийся заголовок",
            "technical": "создай технически точный и детализированный заголовок"
        }

        prompt = f"""
        {style_prompts.get(writing_style, 'создай заголовок')} для статьи на тему '{topic}'.

        {news_context}

        Требования к заголовку:
        - Длина: 5-10 слов
        - Привлекательный и цепляющий
        - Соответствует теме
        - Учитывает актуальные новости (если есть)
        - Без кавычек
        - На русском языке
        """

        response = openai.ChatCompletion.create(
            model=self.default_model,
            messages=[
                {
                    "role": "system",
                    "content": "Ты опытный копирайтер, специализирующийся на создании заголовков для блогов и новостных статей."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=60,
            temperature=0.7,
            stop=["\n"]
        )

        return response.choices[0].message.content.strip()

    def _generate_meta_description(self, title: str, writing_style: str) -> str:
        """Генерация мета-описания для поста"""

        prompt = f"""
        Напиши мета-описание для статьи с заголовком: '{title}'

        Требования:
        - Длина: 150-160 символов
        - Информативное и привлекательное
        - Содержит ключевые слова
        - Побуждает к прочтению
        - Стиль: {writing_style}
        - На русском языке
        """

        response = openai.ChatCompletion.create(
            model=self.default_model,
            messages=[
                {
                    "role": "system",
                    "content": "Ты специалист по SEO и мета-описаниям. Создаешь краткие, но информативные описания."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.5
        )

        return response.choices[0].message.content.strip()

    def _generate_content(self, topic: str, title: str, news_context: str, writing_style: str) -> str:
        """Генерация основного контента поста"""

        style_instructions = {
            "professional": "Профессиональный тон, структурированный подход, использование экспертных мнений",
            "casual": "Непринужденный тон, разговорный стиль, простота изложения",
            "creative": "Креативный подход, использование метафор, эмоциональная окраска",
            "technical": "Техническая точность, детализация, использование специфической терминологии"
        }

        prompt = f"""
        Напиши подробную статью на тему '{topic}' с заголовком '{title}'.

        {news_context}

        Стиль написания: {writing_style}
        {style_instructions.get(writing_style, '')}

        Требования к статье:
        1. Объем: 500-800 слов
        2. Структура: введение, основная часть, заключение
        3. Использование подзаголовков
        4. Абзацы по 3-5 предложений
        5. Фактическая точность
        6. Учет актуальных новостей (если есть)
        7. Практические примеры и insights
        8. Призыв к действию в заключении
        9. На русском языке

        Статья должна быть полезной, информативной и интересной для чтения.
        """

        response = openai.ChatCompletion.create(
            model=self.default_model,
            messages=[
                {
                    "role": "system",
                    "content": "Ты профессиональный блоггер и копирайтер с многолетним опытом. Создаешь качественный, структурированный контент."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
            presence_penalty=0.6,
            frequency_penalty=0.6
        )

        return response.choices[0].message.content.strip()

    def check_health(self) -> bool:
        """Проверка работоспособности OpenAI API"""
        try:
            openai.Model.list(limit=1)
            return True
        except:
            return False