import os
from dotenv import load_dotenv

# .env ፋይልን ያንብብ
load_dotenv()


class Settings:
    BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

    # የአድሚን አይዲዎችን ወደ List of Integers ይቀይራል
    ADMIN_IDS: list = [int(x.strip()) for x in os.getenv(
        "ADMIN_IDS", "").split(",") if x.strip()]

    DESIGNER_USERNAME: str = os.getenv("DESIGNER_USERNAME", "barrokcreative")
    DESIGNER_PHONE: str = os.getenv("DESIGNER_PHONE", "0960150960")


settings = Settings()
