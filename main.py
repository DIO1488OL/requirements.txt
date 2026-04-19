import telebot
import requests
import phonenumbers
import random
import re
import os
from telebot import types
from phonenumbers import carrier, geocoder, timezone
from flask import Flask
from threading import Thread

# --- АНТИ-СОН (Чтобы хостинг не отключал бота) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- ТОКЕН (Вшит) ---
TOKEN = '8518391603:AAEVti-q22IU6MVXPASYGpJq1WcqwadXVL4'
bot = telebot.TeleBot(TOKEN)

# --- ГЛОБАЛЬНАЯ БАЗА МЕТОДОВ (V6.5 Hybrid) ---
DB = {
    "snos_vk": "Здравствуйте Агент! Прошу проверить профиль {t}. Нарушение пункта 5.2 правил: мультиаккаунты и спам через фермы ботов. IP-активность подозрительна.",
    "snos_tg_acc": "Уважаемая поддержка! Аккаунт {t} распространяет запрещенный контент (CSAM) и угрожает жизни. Просьба немедленно заблокировать до выяснения.",
    "snos_tg_ch": "Support, I report channel {t} for doxing and incitement to violence. This violates ToS. Block immediately.",
    "man_lvl3": "💀 **МЕТОД DELFIN (Lvl 3):** Используй RAT через 'чит для Minecraft'. Втирайся в доверие. Докс сливай на Doxbin только после полной деанонимизации.",
    "man_yandex": "📍 **МЕТОД SHTOSH:** Вытаскивай Public_ID через код страницы Яндекса. Ссылка: `reviews.yandex.ru/user/<id>`. Там палятся все заказы еды и адреса.",
    "swat_mail": "🧨 **МЕТОД 5YMAIL:** Анонимные угрозы через TOR. Используй шаблоны Melissa Killer для максимального давления на цель.",
    "crack_session": "⚙️ **LOGIC BY ALTERNATIVE:** Тикет 'Stolen Device' в поддержку ТГ с указанием 'старого' IP жертвы (бери из iplogger). Это выбьет все его сессии.",
    "dorks": "🔗 **GOOGLE DORKS:** `intext:\"{t}\" site:vk.com OR site:instagram.com OR site:ok.ru`"
}

def main_menu():
    m = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add("💀 СНОСЕР (ВАВИЛОН)", "🔍 ГЛУБОКИЙ OSINT")
    m.add("📂 ПРИВАТНЫЕ МАНУАЛЫ", "⚙️ ТЕРМИНАТОР СЕССИЙ")
    m.add("🧨 СВАТТИНГ / ДОСТАВКИ", "🛡 АНОНИМНОСТЬ")
    return m

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 **GALAXY ANNIHILATOR V6.5 HYBRID.**\n\nВсе системы (V5.0 + V6.0) объединены. Мануалы Melissa Killer активны.", reply_markup=main_menu(), parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def logic(message):
    cid = message.chat.id
    t = message.text

    if t == "🔍 ГЛУБОКИЙ OSINT":
        bot.send_message(cid, "🎯 **ВВЕДИ ЦЕЛЬ (Номер, Ник, Почта, IP):**")
        bot.register_next_step_handler(message, run_scan)

    elif t == "💀 СНОСЕР (ВАВИЛОН)":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Снести ВК (5.2)", callback_data="s_vk"))
        kb.add(types.InlineKeyboardButton("Снести ТГ КАНАЛ", callback_data="s_tg_ch"))
        kb.add(types.InlineKeyboardButton("Снести ТГ АККАУНТ 💀", callback_data="s_tg_acc"))
        bot.send_message(cid, "🧨 **ВЫБЕРИ ТИП АТАКИ:**", reply_markup=kb)

    elif t == "📂 ПРИВАТНЫЕ МАНУАЛЫ":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Dox Lvl 3 (Delfin)", callback_data="m_delfin"))
        kb.add(types.InlineKeyboardButton("Метод Shtosh (Яндекс)", callback_data="m_shtosh"))
        kb.add(types.InlineKeyboardButton("Google Dorks (Desu Lt)", callback_data="m_dorks_info"))
        bot.send_message(cid, "📚 **ВЫБЕРИ СЕКРЕТНЫЙ ФАЙЛ:**", reply_markup=kb)

    elif t == "🧨 СВАТТИНГ / ДОСТАВКИ":
        bot.send_message(cid, f"{DB['swat_mail']}", parse_mode='Markdown')

    elif t == "⚙️ ТЕРМИНАТОР СЕССИЙ":
        bot.send_message(cid, DB['crack_session'], parse_mode='Markdown')

    elif t == "🛡 АНОНИМНОСТЬ":
        bot.send_message(cid, "🛡 **ТВОЯ ЗАЩИТА:**\n1. VPN (не бесплатный!)\n2. Смена DNS\n3. Tor Browser для почты 5ymail.")

def run_scan(message):
    val = message.text
    dorks_res = DB['dorks'].format(t=val)
    if val.startswith('+'):
        try:
            p = phonenumbers.parse(val)
            res = f"📱 **ОПЕРАТОР:** {carrier.name_for_number(p, 'ru')}\n📍 **РЕГИОН:** {geocoder.description_for_number(p, 'ru')}"
            bot.send_message(message.chat.id, f"{res}\n\n{dorks_res}", parse_mode='Markdown')
        except:
            bot.send_message(message.chat.id, "❌ Ошибка формата!")
    else:
        bot.send_message(message.chat.id, f"👤 **НИК/ФИО СКАН:**\n\n{dorks_res}", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def calls(call):
    if call.data == "m_delfin": bot.send_message(call.message.chat.id, DB['man_lvl3'], parse_mode='Markdown')
    elif call.data == "m_shtosh": bot.send_message(call.message.chat.id, DB['man_yandex'], parse_mode='Markdown')
    elif call.data == "m_dorks_info": bot.send_message(call.message.chat.id, "Используй раздел OSINT и вводи данные — бот сам выдаст ссылки.")
    elif call.data == "s_vk": bot.send_message(call.message.chat.id, "Введи ссылку на ВК. Текст (5.2) готов.")
    elif call.data == "s_tg_ch": bot.send_message(call.message.chat.id, "Введи ссылку на КАНАЛ. Текст Abuse готов.")
    elif call.data == "s_tg_acc": bot.send_message(call.message.chat.id, "Введи @username или номер. Бот выдаст текст для техподдержки.")

# Запуск анти-сна и бота
if __name__ == '__main__':
    keep_alive()
    bot.polling(none_stop=True)
