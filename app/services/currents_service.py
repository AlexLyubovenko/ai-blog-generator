import logging
from typing import List, Optional, Dict, Any
import requests
from fastapi import HTTPException, status

from app.models.schemas import NewsArticle

logger = logging.getLogger(__name__)


class CurrentsAPI:
    """Класс для работы с Currents API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.currentsapi.services/v1"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "AI-Blog-Generator/1.0"})

    def get_latest_news(self,
                        keywords: str,
                        language: str = "en",
                        category: Optional[str] = None,
                        max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Получение последних новостей по ключевым словам

        Args:
            keywords: Ключевые слова для поиска
            language: Язык новостей
            category: Категория новостей
            max_results: Максимальное количество результатов

        Returns:
            List[Dict]: Список новостных статей
        """
        try:
            params = {
                "apiKey": self.api_key,
                "keywords": keywords,
                "language": language,
                "page_size": max_results
            }

            if category:
                params["category"] = category

            logger.info(f"Запрос новостей по ключевым словам: '{keywords}'")
            response = self.session.get(
                f"{self.base_url}/search",
                params=params,
                timeout=15
            )

            if response.status_code != 200:
                logger.error(f"Ошибка Currents API: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Ошибка при получении новостей: {response.status_code}"
                )

            data = response.json()
            news_data = data.get("news", [])

            if not news_data:
                logger.info(f"Новости по теме '{keywords}' не найдены")
                return []

            articles = []
            for article in news_data[:max_results]:
                article_data = {
                    "title": article.get("title", "Без заголовка"),
                    "description": article.get("description", "Без описания"),
                    "url": article.get("url", ""),
                    "published": article.get("published", ""),
                    "category": article.get("category", [])
                }
                articles.append(article_data)

            logger.info(f"Получено {len(articles)} новостных статей")
            return articles

        except requests.exceptions.Timeout:
            logger.error("Таймаут при запросе к Currents API")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Таймаут при получении новостей от Currents API"
            )
        except requests.exceptions.ConnectionError:
            logger.error("Ошибка подключения к Currents API")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Не удалось подключиться к Currents API"
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сети при запросе к Currents API: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Ошибка сети: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Неожиданная ошибка при получении новостей: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Внутренняя ошибка при получении новостей: {str(e)}"
            )

    def get_available_categories(self) -> List[str]:
        """Получение списка доступных категорий новостей"""
        return [
            "business", "entertainment", "health", "science", "sports",
            "technology", "politics", "world", "breaking-news"
        ]

    def test_connection(self) -> bool:
        """Тестирование подключения к Currents API"""
        try:
            response = self.session.get(
                f"{self.base_url}/search",
                params={
                    "apiKey": self.api_key,
                    "keywords": "test",
                    "page_size": 1
                },
                timeout=10
            )
            return response.status_code == 200
        except:
            return False