try:
    from app.config import settings
    print("✅ config.py imports OK")
except Exception as e:
    print(f"❌ config.py error: {e}")

try:
    from app.models import schemas
    print("✅ schemas.py imports OK")
except Exception as e:
    print(f"❌ schemas.py error: {e}")

try:
    from app.services import openai_service
    print("✅ openai_service.py imports OK")
except Exception as e:
    print(f"❌ openai_service.py error: {e}")

try:
    from app.services import currents_service
    print("✅ currents_service.py imports OK")
except Exception as e:
    print(f"❌ currents_service.py error: {e}")