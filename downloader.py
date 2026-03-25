import yt_dlp
import asyncio
import os
import uuid
from config import DOWNLOAD_PATH


async def download_media(url, mode="video"):
    """
    mode="video" bo'lsa eng yaxshi sifatli video,
    mode="audio" bo'lsa mp3 yuklaydi.
    """
    loop = asyncio.get_event_loop()
    unique_id = str(uuid.uuid4())[:8]

    ydl_opts = {
        "quiet": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "outtmpl": f"{DOWNLOAD_PATH}/{unique_id}_%(title)s.%(ext)s",
    }

    if mode == "audio":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        # Video uchun format (mp4 bo'lishi tavsiya etiladi)
        ydl_opts.update({"format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"})

    def run():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            if mode == "audio":
                file_path = os.path.splitext(file_path)[0] + ".mp3"

            # Instagram caption yoki video title
            caption = info.get("description") or info.get("title") or "Video yuklandi"
            return file_path, caption

    return await loop.run_in_executor(None, run)