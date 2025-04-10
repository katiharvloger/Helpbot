import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")
OWNER_ID = os.getenv("OWNER_ID")  # Seller/Owner Telegram user ID

bot = telebot.TeleBot(BOT_TOKEN)
users = set()
language_state = {}

# --- Command Handlers ---
@bot.message_handler(commands=['start'])
def start_handler(message):
    users.add(message.chat.id)
    lang = language_state.get(message.chat.id, 'en')
    welcome_text = get_welcome_text(lang)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Order Now", web_app=WebAppInfo(url=WEB_APP_URL)))
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['language'])
def toggle_language(message):
    current = language_state.get(message.chat.id, 'en')
    language_state[message.chat.id] = 'hi' if current == 'en' else 'en'
    bot.send_message(message.chat.id, "भाषा बदली गई है।" if language_state[message.chat.id] == 'hi' else "Language switched to English.")

@bot.message_handler(commands=['menu'])
def menu_handler(message):
    lang = language_state.get(message.chat.id, 'en')
    if lang == 'hi':
        text = "कैसे इस्तेमाल करें:
1. भोजन राशि दर्ज करें
2. टैक्स + प्लेटफार्म शुल्क
3. डिलीवरी दूरी दर्ज करें
फिर 'Calculate' दबाएं।"
    else:
        text = "How to order:
1. Enter food amount
2. Add tax + platform fee
3. Enter delivery distance
Then press 'Calculate'."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, "Contact the seller: @katiharvloger2
Or type your message and we'll forward it.")

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    users.add(message.chat.id)
    if str(message.chat.id) == OWNER_ID:
        if message.text.startswith("/broadcast "):
            text = message.text.replace("/broadcast ", "")
            for uid in users:
                if str(uid) != OWNER_ID:
                    bot.send_message(uid, f"📢 Broadcast:
{text}")
        elif message.reply_to_message:
            bot.send_message(message.reply_to_message.forward_from.id, f"💬 Seller: {message.text}")
    else:
        bot.send_message(int(OWNER_ID), f"📥 Message from @{message.from_user.username or message.from_user.first_name}:
{message.text}")
        bot.send_message(message.chat.id, "Your message has been forwarded to the seller.")

def get_welcome_text(lang):
    if lang == 'hi':
        return ("🍽️ *स्विगी ऑर्डर असिस्टेंट में आपका स्वागत है!*

"
                "अपना पसंदीदा खाना ऑर्डर करने के लिए तैयार हैं?

"
                "👉 नीचे दिए गए *Order Now* बटन पर टैप करें।

"
                "🔧 मदद चाहिए? /help टाइप करें
"
                "🌐 भाषा बदलें: /language
"
                "📋 निर्देश देखें: /menu
"
                "📦 ऑर्डर करें: /order

"
                "📞 संपर्क: [@katiharvloger2](https://t.me/katiharvloger2)")
    else:
        return ("🍽️ *Welcome to Swiggy Order Assistant!*

"
                "Ready to order your favorite food?

"
                "👉 Tap on the *Order Now* button below to get started.

"
                "🔧 Need help? Type /help
"
                "🌐 Switch language: /language
"
                "📋 View instructions: /menu
"
                "📦 Place order: /order

"
                "📞 For any query, contact: [@katiharvloger2](https://t.me/katiharvloger2)")

bot.infinity_polling()