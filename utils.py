import re


def format_duration(seconds):
    """Saniyalarni 00:00 formatiga o'tkazadi"""
    if not seconds:
        return "Noma'lum"
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"


def clean_caption(caption, limit=900):
    """
    Instagram yoki YT captionlarini tozalaydi va
    Telegram limiti (1024) dan oshib ketmasligini ta'minlaydi.
    """
    if not caption:
        return "Video tavsifi mavjud emas."

    # Ortiqcha bo'shliqlarni olib tashlash
    caption = caption.strip()

    # Telegram limiti uchun qisqartirish
    if len(caption) > limit:
        return caption[:limit] + "..."
    return caption


def extract_hashtags(text):
    """Matn ichidan barcha heshteglarni ajratib oladi"""
    if not text:
        return ""
    hashtags = re.findall(r"#\w+", text)
    return " ".join(hashtags) if hashtags else "Heshteglar topilmadi."


def generate_media_caption(title, duration=None, source="Ijtimoiy tarmoq"):
    """Video yoki Audio uchun tayyor chiroyli matn yasaydi"""
    time_str = format_duration(duration) if duration else "Noma'lum"

    return (
        f"🎵 *Nomi:* {title}\n"
        f"⏱ *Davomiyligi:* {time_str}\n"
        f"🌐 *Manba:* {source}\n\n"
        f"🤖 @Qoshiq_Yuklovchi_orgBot orqali yuklandi"
    )