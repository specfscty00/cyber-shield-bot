# -*- coding: utf-8 -*-
"""
Telegram-бот Cyber Shield
Автор: MrBulbaOO1, 12 лет, Беларусь
Конкурс #КиберПраво
"""
import os, json, random, logging, asyncio, re, sys
from urllib.parse import urlparse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "TOKEN"
if not TOKEN:
    print("Ошибка: задайте переменную окружения TOKEN")
    sys.exit(1)

LEARN_URL = "https://telegra.ph/Cyber-Shield-03-04"
DATA_FILE = "user_data.json"
PATTERNS_FILE = "scam_patterns.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# загрузка паттернов
with open(PATTERNS_FILE, "r", encoding="utf-8") as f:
    PATTERNS = json.load(f)

# ----- ВОПРОСЫ (40 доменов, 35 писем, 25 звонков) -----
DOMAIN_QUESTIONS = [
    {"text": "Ссылка: https://www.gosuslugi.ru\n\nЭто официальный сайт?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Настоящий портал Госуслуг."},
    {"text": "Ссылка: https://www.sberbank.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Официальный сайт Сбербанка."},
    {"text": "Ссылка: https://www.mos.ru\n\nЭто официальный сайт мэрии Москвы?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Официальный портал mos.ru."},
    {"text": "Ссылка: https://www.nalog.gov.ru\n\nЭто сайт ФНС?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Официальный сайт ФНС."},
    {"text": "Ссылка: https://www.google.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Google."},
    {"text": "Ссылка: https://www.youtube.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "YouTube."},
    {"text": "Ссылка: https://www.vtb.ru\n\nЭто официальный сайт ВТБ?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "ВТБ."},
    {"text": "Ссылка: https://www.tinkoff.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Тинькофф."},
    {"text": "Ссылка: https://www.ozon.ru\n\nЭто маркетплейс?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Озон."},
    {"text": "Ссылка: https://www.wildberries.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Wildberries."},
    {"text": "Ссылка: https://www.avito.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Авито."},
    {"text": "Ссылка: https://www.cian.ru\n\nЭто сайт недвижимости?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "ЦИАН."},
    {"text": "Ссылка: https://www.2gis.ru\n\nЭто карты?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "2ГИС."},
    {"text": "Ссылка: https://www.kaspersky.ru\n\nЭто антивирус?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Лаборатория Касперского."},
    {"text": "Ссылка: https://www.mail.ru\n\nЭто почта?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Mail.ru."},
    {"text": "Ссылка: https://www.yandex.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Яндекс."},
    {"text": "Ссылка: https://www.microsoft.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Microsoft."},
    {"text": "Ссылка: https://www.apple.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Apple."},
    {"text": "Ссылка: https://www.netflix.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Netflix."},
    {"text": "Ссылка: https://xn--80adtgbbrh1afh.xn--p1ai\n\nВы видите punycode. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Punycode — маскировка опасных сайтов."},
    {"text": "Ссылка: https://rostransnadzor.digital\n\nПисьмо от Ространснадзора. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг!"},
    {"text": "Ссылка: https://pcloud.online\n\nОблачное хранилище. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Подделка под pCloud."},
    {"text": "Ссылка: https://flowers-shop-msk.ru\n\nМагазин цветов со скидками. Надёжно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фейковый сайт."},
    {"text": "Ссылка: https://gift-card-2026.ru\n\nПодарочные сертификаты. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг."},
    {"text": "Ссылка: https://telegram-rose-fortune.ru\n\nРозыгрыш от Дурова. Правда?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Мошенники."},
    {"text": "Ссылка: https://zakon-o-podpiskah.ru\n\nСкрытые подписки. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг."},
    {"text": "Ссылка: https://фнс-проверка.рф\n\nПисьмо от ФНС. Официально?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Нет, налоговая не рассылает ссылки."},
    {"text": "Ссылка: https://gosuslugi-ident.ru\n\nПодтверждение личности. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Настоящий Госуслуги – gosuslugi.ru."},
    {"text": "Ссылка: https://photo-studio-msk.com\n\nБесплатная фотосессия. Нормально?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Мошенники просят перевод."},
    {"text": "Ссылка: https://zakaz-buketov.ru\n\nДоставка цветов с предоплатой. Надёжно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Сайт-однодневка."},
    {"text": "Ссылка: https://telegram-security.ru\n\nСлужба безопасности Telegram. Настоящий?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Нет! Настоящий – telegram.org."},
    {"text": "Ссылка: https://sberbank-online.info\n\nВход в личный кабинет. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен .info не относится к Сбербанку."},
    {"text": "Ссылка: https://vk.com.free-vote.ru\n\nГолосование. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг для кражи аккаунта."},
    {"text": "Ссылка: https://google.security-update.com\n\nОбновление безопасности. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг."},
    {"text": "Ссылка: http://apple.com.verify-account.net\n\nПодтверждение Apple ID. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг."},
    {"text": "Ссылка: https://www.paypal.com.signin.secure.tk\n\nВход в PayPal. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг, домен .tk."},
    {"text": "Ссылка: http://telegram.org-login.xyz\n\nВход в Telegram. Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг, домен .xyz."},
    {"text": "Ссылка: https://xn--e1awg7f.xn--p1ai\n\nPunycode для «кино.рф». Безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Официальный сайт."},
    {"text": "Ссылка: http://online.alfabank.by\n\nАльфа-Банк Беларусь?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Официальный сайт."},
]
# добиваем ровно до 40 (некоторые вопросы уже есть, но добавим пару тестовых для ровного счета)
while len(DOMAIN_QUESTIONS) < 40:
    DOMAIN_QUESTIONS.append({"text": "Ссылка: https://example.com\n\nТестовый сайт.", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Пример."})

MESSAGE_QUESTIONS = [
    {"text": "Письмо: «Обнаружено 7 скрытых подписок! Срочно отмените здесь: ссылка»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да, новая схема."},
    {"text": "Письмо: «Вы выиграли подписку Telegram Premium от Павла Дурова. Оплатите пошлину»\n\nЭто правда?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет, мошенники."},
    {"text": "Письмо: «Приглашение на фотосессию. Запись по ссылке»\n\nЧто делать?", "options": ["✅ Перейду", "🚫 Проверю"], "correct": 1, "explanation": "Проверьте! Фейк."},
    {"text": "Письмо: «Налоговая задолженность. Оплатите сейчас» со ссылкой\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет, налоговая не рассылает ссылки."},
    {"text": "Письмо: «Вы назначены на маникюр. Назовите последние цифры номера» (вы не записывались)\n\nЧто делать?", "options": ["✅ Назову", "🚫 Не буду"], "correct": 1, "explanation": "Не называйте! Схема 2026."},
    {"text": "Письмо с календарным приглашением без текста, только ссылка\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Календарный фишинг."},
    {"text": "Письмо: «Вам голосовое сообщение» с ссылкой\n\nЭто может быть опасно?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да, CAPTCHA-обход."},
    {"text": "Письмо от «службы безопасности» с вложением «Акт проверки.rtf»\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Вредоносный файл."},
    {"text": "СМС: «Курьер с цветами не может найти адрес, назовите последние цифры номера»\n\nВаши действия?", "options": ["✅ Назову", "🚫 Не назову"], "correct": 1, "explanation": "Не называйте!"},
    {"text": "Письмо: «Скрытые подписки обнаружены. Отмените здесь»\n\nЭто правда?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Фишинг."},
    {"text": "Письмо: «Ваш аккаунт взломан! Срочно перейдите по ссылке»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да, классика."},
    {"text": "Письмо: «Вы выиграли приз! Переведите 100 рублей за доставку»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да!"},
    {"text": "Письмо от «банка»: «Ваша карта заблокирована, подтвердите данные»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг!"},
    {"text": "Письмо: «Служба безопасности Telegram. Перейдите: t.me-login.ru»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Настоящий – t.me."},
    {"text": "Письмо: «Мама, положи 100 рублей на этот номер» (номер чужой)\n\nТвои действия?", "options": ["✅ Переведу", "🚫 Позвоню маме"], "correct": 1, "explanation": "Позвоните маме!"},
]
while len(MESSAGE_QUESTIONS) < 35:
    MESSAGE_QUESTIONS.append({"text": f"Тестовое письмо: срочное уведомление.\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Скорее всего, да."})

CALL_QUESTIONS = [
    {"text": "Звонок: «Вас беспокоит ФСБ. Переведите деньги на безопасный счёт»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Положу трубку"], "correct": 1, "explanation": "Клади трубку! ФСБ не звонит."},
    {"text": "Звонок: «Это из поликлиники. Назовите код из СМС»\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет!"},
    {"text": "Звонок: «Вам ошибочно перевели 5000 рублей. Верните на этот номер»\n\nЧто делать?", "options": ["✅ Верну", "🚫 Сообщу в банк"], "correct": 1, "explanation": "Не возвращайте!"},
    {"text": "Звонок: «Это курьер, у меня цветы для вас. Нужна предоплата 200 рублей»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Откажусь"], "correct": 1, "explanation": "Откажитесь!"},
    {"text": "Звонок: «Привет, я ваш новый сосед, заливаю этажом ниже. Скинь 500 рублей»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Позвоню в УК"], "correct": 1, "explanation": "Позвоните в УК."},
    {"text": "Звонок: «Вам одобрен кредит! Назовите паспортные данные»\n\nЧто делать?", "options": ["✅ Назову", "🚫 Положу трубку"], "correct": 1, "explanation": "Не называйте!"},
    {"text": "Звонок с неизвестного номера — сброс. Перезванивать?", "options": ["✅ Перезвоню", "🚫 Не буду"], "correct": 1, "explanation": "Не перезванивайте!"},
    {"text": "Звонок: «Служба безопасности Wildberries. Ваш заказ заморожен, назовите данные карты»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да!"},
    {"text": "Звонок: «Алло, это ваш директор! Срочно переведи 5000» (голос похож)\n\nЧто делать?", "options": ["✅ Переведу", "🚫 Позвоню директору"], "correct": 1, "explanation": "Позвоните директору! Дипфейк."},
    {"text": "Звонок: «Вас беспокоит Роскомнадзор. Ваши деньги пытаются украсть»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Позвоню в банк"], "correct": 1, "explanation": "Роскомнадзор не занимается деньгами."},
    {"text": "Звонок: «Это фотостудия. Назовите последние цифры номера для подтверждения» (вы не записывались)\n\nВаши действия?", "options": ["✅ Назову", "🚫 Не назову"], "correct": 1, "explanation": "Не называйте!"},
    {"text": "Звонок: «Мы тестируем новый сервис ЖКХ, скинем файлик, открой его»\n\nОткроете?", "options": ["✅ Открою", "🚫 Не открою"], "correct": 1, "explanation": "Не открывайте! Вирус."},
    {"text": "Звонок: «Ваш аккаунт в Telegram взламывают! Перейдите по ссылке из СМС»\n\nПерейдёте?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет!"},
    {"text": "Звонок: «Вы выиграли приз! Назовите данные карты»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да!"},
    {"text": "Звонок: «Служба безопасности банка. Назовите код из СМС»\n\nЧто сделает настоящий банк?", "options": ["✅ Попросит код", "🚫 Никогда не спросит"], "correct": 1, "explanation": "Верно!"},
    {"text": "Звонок с номера мамы: «Дочка, переведи деньги». Голос похож.\n\nТвои действия?", "options": ["✅ Переведу", "🚫 Перезвоню на старый номер"], "correct": 1, "explanation": "Перезвоните!"},
    {"text": "Звонок: «Служба безопасности Google. Продиктуйте пароль»\n\nВаши действия?", "options": ["✅ Продиктую", "🚫 Положу трубку"], "correct": 1, "explanation": "Google никогда не звонит."},
    {"text": "Звонок: «Это ваш участковый. Назовите паспортные данные»\n\nВаши действия?", "options": ["✅ Назову", "🚫 Позвоню в отделение"], "correct": 1, "explanation": "Полиция не запрашивает данные по телефону."},
    {"text": "Звонок: «Вы попали под следствие за терроризм, переведите деньги на спецсчёт»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Положу трубку и позвоню 102"], "correct": 1, "explanation": "Запугивание."},
    {"text": "Звонок от «соседа»: «У нас домофон ломают, скажи код из СМС»\n\nЭто норм?", "options": ["✅ Скажу", "🚫 Позвоню в управляйку"], "correct": 1, "explanation": "Развод!"},
    {"text": "Звонок: «Привет, я из фотостудии! Назови последние цифры»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг!"},
    {"text": "Звонок: «Тестируем сервис ЖКХ, скинем файлик, открой»\n\nОткроете?", "options": ["✅ Открою", "🚫 Не открою"], "correct": 1, "explanation": "Вирус!"},
    {"text": "Звонок: «Вам перевод от бабушки, нужна комиссия. Скажите код из СМС»\n\nЧто делать?", "options": ["✅ Скажу", "🚫 Положу трубку"], "correct": 1, "explanation": "Клади трубку!"},
    {"text": "Звонок: «Ваш аккаунт в Telegram взламывают! Перейдите по ссылке»\n\nПерейдёшь?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет!"},
    {"text": "Звонок: «Служба безопасности Wildberries. Ваш заказ заморожен»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да!"},
]
while len(CALL_QUESTIONS) < 25:
    CALL_QUESTIONS.append({"text": f"Тестовый звонок: неизвестный просит деньги.\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Проверю"], "correct": 1, "explanation": "Проверьте информацию."})

QUESTIONS = {"domains": DOMAIN_QUESTIONS, "messages": MESSAGE_QUESTIONS, "calls": CALL_QUESTIONS}
LEVELS_TOTAL = {k: len(v) for k, v in QUESTIONS.items()}

# ----- ПРОГРЕСС И ПЕРЕМЕШИВАНИЕ -----
def init_user_data():
    return {cat: {"order": random.sample(range(LEVELS_TOTAL[cat]), LEVELS_TOTAL[cat]), "pos": 0} for cat in QUESTIONS}

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_data(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = init_user_data()
        save_data(data)
    return data[uid]

def save_user_data(user_id, ud):
    data = load_data()
    data[str(user_id)] = ud
    save_data(data)

def answer_correct(user_id, cat):
    ud = get_user_data(user_id)
    ud[cat]["pos"] += 1
    save_user_data(user_id, ud)

def reset_progress(user_id):
    save_user_data(user_id, init_user_data())

def total_level(user_id):
    ud = get_user_data(user_id)
    return sum(ud[cat]["pos"] for cat in QUESTIONS)

# ----- КЛАВИАТУРЫ -----
def main_menu():
    kb = [
        [InlineKeyboardButton("🖥 Отличи домен", callback_data="cat_domains"),
         InlineKeyboardButton("📧 Отличи письмо", callback_data="cat_messages")],
        [InlineKeyboardButton("📞 Отличи звонок", callback_data="cat_calls"),
         InlineKeyboardButton("📚 Изучить материалы", callback_data="learn")],
        [InlineKeyboardButton("❓ Случайное задание", callback_data="random"),
         InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("ℹ️ О проекте", callback_data="about")]
    ]
    return InlineKeyboardMarkup(kb)

def answer_keyboard(cat, pos, opts):
    btns = [InlineKeyboardButton(opt, callback_data=f"ans_{cat}_{pos}_{i}") for i, opt in enumerate(opts)]
    return InlineKeyboardMarkup([btns, [InlineKeyboardButton("⬅️ В меню", callback_data="back_to_main")]])

# ----- СКАМ-ДЕТЕКТОР -----
def check_tld_risk(domain):
    d = domain.lower()
    for tld in PATTERNS["critical_tlds"]:
        if d.endswith(tld): return 5, f"Критическая зона {tld}"
    for tld in PATTERNS["high_risk_tlds"]:
        if d.endswith(tld): return 3, f"Опасная зона {tld}"
    for tld in PATTERNS["medium_risk_tlds"]:
        if d.endswith(tld): return 2, f"Подозрительная зона {tld}"
    return 0, None

def check_typo(domain):
    d = domain.lower()
    for pat, safe in PATTERNS["typosquatting_patterns"].items():
        if re.search(pat, d): return 4, f"Подмена: похоже на {safe}"
    return 0, None

def scam_detector(text):
    text_low = text.lower()
    score = 0
    reasons = []
    urls = re.findall(r'(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text_low)
    if urls:
        for url in urls:
            parsed = urlparse(url if '://' in url else 'http://'+url)
            domain = (parsed.netloc or parsed.path.split('/')[0]).split(':')[0]
            s, r = check_tld_risk(domain)
            if s: score += s; reasons.append(r)
            s, r = check_typo(domain)
            if s: score += s; reasons.append(r)
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
                score += 5; reasons.append("IP-адрес вместо домена")
            if any(short in domain for short in PATTERNS["shorteners"]):
                score += 4; reasons.append("Сокращённая ссылка")
    for ph in PATTERNS["phone_scam_phrases"]:
        if ph in text_low:
            score += 5; reasons.append(f"Телефон: «{ph}»"); break
    for ph in PATTERNS["message_scam_phrases"]:
        if ph in text_low:
            score += 3; reasons.append(f"Письмо: «{ph}»"); break
    for ph in PATTERNS["kids_scam_phrases"]:
        if ph in text_low:
            score += 4; reasons.append(f"Дети: «{ph}»"); break
    matched = [w for w in PATTERNS["general_scam_words"] if w in text_low]
    if matched:
        score += 2*min(3, len(matched)); reasons.append(f"Общие: {', '.join(matched[:3])}")
    for ph in PATTERNS["impersonal_phrases"]:
        if ph in text_low:
            score += 1; reasons.append(f"Безличное: «{ph}»"); break
    if urls and re.search(r'[а-яА-Я]', str(urls)):
        score += 3; reasons.append("Кириллица в ссылке")
    if score >= 8: v, adv = "🔴 КРИТИЧЕСКИ ОПАСНО", "НЕ ПЕРЕХОДИТЕ!"
    elif score >= 4: v, adv = "🟠 ПОДОЗРИТЕЛЬНО", "Будьте осторожны"
    elif score >= 1: v, adv = "🟡 ВНИМАНИЕ", "Проверьте информацию"
    else: v, adv = "🟢 БЕЗОПАСНО", "Признаков не найдено"
    res = f"{v}\n\n"
    if reasons:
        res += "🔍 Признаки:\n• " + "\n• ".join(reasons[:5])
        if len(reasons)>5: res += f"\n• и ещё {len(reasons)-5}"
        res += f"\n\n⚠️ Риск: {score} баллов\n\n"
    res += f"💡 {adv}"
    return res

# ----- ОБРАБОТЧИКИ -----
async def start(upd, ctx):
    await upd.message.reply_text("🛡️ Cyber Shield\n100 уровней, случайный порядок.\nВыбери действие:", reply_markup=main_menu(), disable_web_page_preview=True)

async def help_cmd(upd, ctx):
    await upd.message.reply_text("/start – запуск\n/reset – сброс прогресса\nОтправь мне подозрительное сообщение", disable_web_page_preview=True)

async def reset_cmd(upd, ctx):
    reset_progress(upd.effective_user.id)
    await upd.message.reply_text("✅ Прогресс сброшен.", disable_web_page_preview=True)

async def button(upd, ctx):
    q = upd.callback_query
    await q.answer()
    data = q.data
    uid = q.from_user.id
    if data == "back_to_main":
        await q.edit_message_text("Главное меню:", reply_markup=main_menu())
        return
    if data == "learn":
        await q.edit_message_text(f"📚 Обучающие материалы:\n{LEARN_URL}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ В меню", callback_data="back_to_main")]]))
        return
    if data == "stats":
        ud = get_user_data(uid)
        total = sum(ud[cat]["pos"] for cat in QUESTIONS)
        txt = f"📊 Статистика\nВсего пройдено: {total}\n" + "\n".join(f"{cat}: {ud[cat]['pos']}/{LEVELS_TOTAL[cat]}" for cat in QUESTIONS)
        await q.edit_message_text(txt, reply_markup=main_menu())
        return
    if data == "about":
        await q.edit_message_text("ℹ️ О проекте\nАвтор: MrBulbaOO1 (12 лет, Беларусь)\nКонкурс #КиберПраво\nКонтакты: Stepanchuk2024@gmail.com", reply_markup=main_menu())
        return
    if data.startswith("cat_"):
        cat = data[4:]
        ud = get_user_data(uid)
        pos = ud[cat]["pos"]
        if pos >= LEVELS_TOTAL[cat]:
            await q.edit_message_text("🎉 Вы прошли все задания в этой категории!", reply_markup=main_menu())
            return
        idx = ud[cat]["order"][pos]
        qst = QUESTIONS[cat][idx]
        await q.edit_message_text(f"🔍 Уровень {pos+1} ({cat}):\n{qst['text']}", reply_markup=answer_keyboard(cat, pos, qst['options']))
        return
    if data.startswith("ans_"):
        parts = data.split('_')
        cat, pos, ans_idx = parts[1], int(parts[2]), int(parts[3])
        ud = get_user_data(uid)
        if pos != ud[cat]["pos"]:
            await q.edit_message_text("⏳ Задание устарело", reply_markup=main_menu())
            return
        idx = ud[cat]["order"][pos]
        qst = QUESTIONS[cat][idx]
        if ans_idx == qst['correct']:
            answer_correct(uid, cat)
            new_pos = pos+1
            reply = f"✅ Правильно!\n{qst['explanation']}\nТеперь уровень {new_pos}"
        else:
            reply = f"❌ Неправильно.\n{qst['explanation']}"
        kb = [[InlineKeyboardButton("▶️ Следующее", callback_data=f"cat_{cat}")], [InlineKeyboardButton("⬅️ Меню", callback_data="back_to_main")]]
        await q.edit_message_text(reply, reply_markup=InlineKeyboardMarkup(kb))
        return
    if data == "random":
        cat = random.choice(list(QUESTIONS.keys()))
        idx = random.randint(0, LEVELS_TOTAL[cat]-1)
        qst = QUESTIONS[cat][idx]
        kb = [[InlineKeyboardButton(qst['options'][0], callback_data=f"rand_{cat}_{idx}_0"), InlineKeyboardButton(qst['options'][1], callback_data=f"rand_{cat}_{idx}_1")], [InlineKeyboardButton("⬅️ Меню", callback_data="back_to_main")]]
        await q.edit_message_text(f"🎲 Случайное задание:\n{qst['text']}", reply_markup=InlineKeyboardMarkup(kb))
        return
    if data.startswith("rand_"):
        parts = data.split('_')
        cat, idx, ans_idx = parts[1], int(parts[2]), int(parts[3])
        qst = QUESTIONS[cat][idx]
        if ans_idx == qst['correct']:
            reply = f"✅ Правильно!\n{qst['explanation']}"
        else:
            reply = f"❌ Неправильно.\n{qst['explanation']}"
        await q.edit_message_text(reply, reply_markup=main_menu())
        return

async def text_msg(upd, ctx):
    resp = scam_detector(upd.message.text)
    await upd.message.reply_text(resp, disable_web_page_preview=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("reset", reset_cmd))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_msg))
    print("Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()
