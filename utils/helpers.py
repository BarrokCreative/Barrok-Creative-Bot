import re
from datetime import datetime, timedelta, timezone


def validate_ethiopian_phone(phone: str) -> bool:
    """የኢትዮጵያ ስልክ ቁጥር ፎርማትን ያረጋግጣል (+251..., 09..., 07...)"""
    # 09, 07, ወይም +251 9, +251 7 ብሎ የጀመረ እና በትክክል የቁጥር ብዛቱ የሞላ
    pattern = r"^(\+251|0)(9|7)\d{8}$"
    return bool(re.match(pattern, phone.strip()))


def get_ethiopian_time() -> datetime:
    """የአሁኑን የUTC ሰዓት ወደ ኢትዮጵያ ሰዓት አቆጣጠር (GMT+3) ይቀይራል"""
    utc_now = datetime.now(timezone.utc)
    eat_tz = timezone(timedelta(hours=3))  # East Africa Time (EAT)
    return utc_now.astimezone(eat_tz)
