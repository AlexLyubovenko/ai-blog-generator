from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TopicRequest(BaseModel):
    """Модель запроса для генерации поста по теме"""
    topic: str = Field(
        ...,
        description="Основная тема для генерации поста",
        min_length=2,
        max_length=100,
        example="искусственный интеллект"
    )
    language: str = Field(
        "en",
        description="Язык для поиска новостей (en, ru, etc.)",
        example="en"
    )
    include_news: bool = Field(
        True,
        description="Включать ли актуальные новости в контекст"
    )
    max_news_articles: int = Field(
        5,
        description="Максимальное количество новостей для использования",
        ge=1,
        le=10,
        example=5
    )
    writing_style: str = Field(
        "professional",
        description="Стиль написания (professional, casual, creative, technical)",
        example="professional"
    )

class NewsSearchRequest(BaseModel):
    """Модель запроса для поиска новостей"""
    keywords: str = Field(
        ...,
        description="Ключевые слова для поиска новостей",
        example="технологии"
    )
    language: str = Field(
        "en",
        description="Язык новостей",
        example="en"
    )
    category: Optional[str] = Field(
        None,
        description="Категория новостей",
        example="technology"
    )
    max_results: int = Field(
        5,
        description="Максимальное количество результатов",
        ge=1,
        le=20,
        example=5
    )

class NewsArticle(BaseModel):
    """Модель новостной статьи"""
    title: str = Field(..., description="Заголовок статьи")
    description: str = Field(..., description="Описание статьи")
    url: str = Field(..., description="URL статьи")
    published: str = Field(..., description="Дата публикации")
    category: List[str] = Field(..., description="Категории статьи")

class GeneratedPostResponse(BaseModel):
    """Модель ответа с сгенерированным постом"""
    topic: str = Field(..., description="Исходная тема")
    title: str = Field(..., description="Сгенерированный заголовок")
    content: str = Field(..., description="Сгенерированный контент")
    meta_description: str = Field(..., description="Мета-описание")
    news_used: List[str] = Field(..., description="Использованные новости")
    generated_at: datetime = Field(..., description="Время генерации")
    tokens_used: int = Field(..., description="Использованные токены")
    writing_style: str = Field(..., description="Стиль написания")

class HealthCheckResponse(BaseModel):
    """Модель ответа для проверки здоровья сервиса"""
    status: str = Field(..., description="Общий статус сервиса")
    timestamp: datetime = Field(..., description="Время проверки")
    services: Dict[str, str] = Field(..., description="Статусы отдельных сервисов")

class ErrorResponse(BaseModel):
    """Модель ответа для ошибок"""
    detail: str = Field(..., description="Описание ошибки")
    error_type: str = Field(..., description="Тип ошибки")
    timestamp: datetime = Field(..., description="Время ошибки")