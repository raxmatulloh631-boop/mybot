import os
import types

import dp
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import ContextTypes
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from downloader import download_media
from utils import clean_caption


# Holatlarni belgilaymiz
class CaptionState(StatesGroup):
    waiting_for_link = State()


# /caption komandasi
@dp.message(Command("caption"))
async def caption_request(message: types.Message, state: ContextTypes):
    builder = InlineKeyboardBuilder()
    builder.button(text="🔗 Link yuborish", callback_data="send_link_now")

    await message.answer(
        "Instagram yoki TikTok videosining matnini (caption) olish uchun pastdagi tugmani bosing:",
        reply_markup=builder.as_markup()
    )


# Tugma bosilganda linkni kutish holatiga o'tamiz
@dp.callback_query(F.data == "send_link_now")
async def ask_for_link(call: types.CallbackQuery, state: ContextTypes):
    await state.set_state(CaptionState.waiting_for_link)
    await call.message.edit_text("Marhamat, videoning linkini yuboring:")
    await call.answer()


# Faqat caption kutayotgan holatimizda link kelsa
@dp.message(CaptionState.waiting_for_link)
async def process_caption_link(message: types.Message, state: ContextTypes):
    url = message.text.strip()

    if not any(x in url for x in ["instagram.com", "tiktok.com", "youtube.com"]):
        await message.answer("❌ Bu yaroqli link emas. Iltimos, video linkini yuboring.")
        return

    msg = await message.answer("🔍 Matn tayyorlanmoqda...")

    try:
        # downloader.py dagi funksiyani faqat ma'lumot olish uchun chaqiramiz
        # video yuklamaslik uchun download_media funksiyasini biroz moslash kerak yoki info_only qilish kerak
        file_path, raw_caption = await download_media(url, mode="video")

        formatted_caption = clean_caption(raw_caption)

        await message.answer(
            f"✅ *Video matni:* \n\n`{formatted_caption}`",
            parse_mode="Markdown"
        )

        # Keraksiz videoni o'chirib yuboramiz (agar download_media yuklab qo'ysa)
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")

    await msg.delete()
    await state.clear()  # Holatni yakunlaymiz