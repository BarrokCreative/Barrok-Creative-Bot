from supabase import create_client, Client
from config.settings import settings

# ከSupabase ጋር ግንኙነት መፍጠር
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def get_db():
    """የዳታቤዝ ክላይንቱን ለመጥራት የሚያገለግል ረዳት ተግባር"""
    return supabase
