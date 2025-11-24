from sqlalchemy import create_engine
from app.core.config import settings

def test_connection():
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            print("🔥 Connected to PostgreSQL successfully!")
    except Exception as e:
        print("❌ Connection error:", e)

if __name__ == "__main__":
    test_connection()
