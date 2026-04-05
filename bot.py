# -*- coding: utf-8 -*-
"""
Telegram-бот Cyber Shield (v12.0)
Автор: MrBulbaOO1, 12 лет, Брест
Конкурс #КиберПраво
Данные обновлены по состоянию на апрель 2026 года
"""

import json
import random
import logging
import asyncio
import re
import sys
from urllib.parse import urlparse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# =============== ПРОВЕРКА УСТАНОВКИ ===============
try:
    from telegram import Update
except ImportError:
    print("\n" + "="*50)
    print("ОШИБКА: Библиотека python-telegram-bot не установлена!")
    print("Выполните: pip install python-telegram-bot")
    print("="*50 + "\n")
    sys.exit(1)

# =============== НАСТРОЙКИ ===============
TOKEN = "your_token"  # Вставьте свой токен
LEARN_URL = "https://telegra.ph/Cyber-Shield-03-04"
DATA_FILE = "user_data.json"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# =============== ВОПРОСЫ 2026 ГОДА ===============

# ----- 40 вопросов по доменам (актуальные фишинговые сайты 2026) -----
DOMAIN_QUESTIONS = [
    # Безопасные сайты (0)
    {"text": "Ссылка: https://www.gosuslugi.ru\n\nЭто официальный сайт Госуслуг?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, это официальный портал Госуслуг."},
    {"text": "Ссылка: https://www.sberbank.ru\n\nЭто официальный сайт Сбербанка?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Официальный сайт Сбербанка."},
    {"text": "Ссылка: https://www.mos.ru\n\nЭто официальный сайт мэрии Москвы?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный портал mos.ru."},
    {"text": "Ссылка: https://www.nalog.gov.ru\n\nЭто официальный сайт ФНС?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Официальный сайт Федеральной налоговой службы."},
    {"text": "Ссылка: https://www.google.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, это официальный сайт Google."},
    {"text": "Ссылка: https://www.youtube.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, это YouTube."},
    {"text": "Ссылка: https://www.vtb.ru\n\nЭто официальный сайт ВТБ?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный сайт ВТБ."},
    {"text": "Ссылка: https://www.tinkoff.ru\n\nЭто официальный сайт Тинькофф?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный сайт Тинькофф."},
    {"text": "Ссылка: https://www.ozon.ru\n\nЭто официальный маркетплейс?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, это Ozon."},
    {"text": "Ссылка: https://www.wildberries.ru\n\nЭто официальный сайт Wildberries?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный сайт Wildberries."},
    {"text": "Ссылка: https://www.avito.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, это Avito."},
    {"text": "Ссылка: https://www.cian.ru\n\nЭто официальный сайт ЦИАН?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный сайт ЦИАН."},
    {"text": "Ссылка: https://www.2gis.ru\n\nЭто официальный сайт 2ГИС?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный сайт 2ГИС."},
    {"text": "Ссылка: https://www.kaspersky.ru\n\nЭто официальный сайт Лаборатории Касперского?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный сайт."},
    {"text": "Ссылка: https://www.mail.ru\n\nЭто официальный почтовый сервис?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, это Mail.ru."},
    {"text": "Ссылка: https://www.rambler.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, это Rambler."},
    {"text": "Ссылка: https://www.yandex.ru\n\nЭто официальный сайт Яндекса?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный сайт Яндекса."},
    {"text": "Ссылка: https://www.microsoft.com\n\nЭто официальный сайт Microsoft?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный сайт Microsoft."},
    {"text": "Ссылка: https://www.apple.com\n\nЭто официальный сайт Apple?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный сайт Apple."},
    {"text": "Ссылка: https://www.netflix.com\n\nЭто официальный сайт Netflix?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, официальный сайт Netflix."},
    # Фишинговые сайты 2026 (1)
    {"text": "Ссылка: https://b2b-gospodderzka.ru\n\nСайт якобы от господдержки бизнеса. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Мошенники создают сайты с формулировками вроде b2b-gospodderzka для кражи данных компаний."},
    {"text": "Ссылка: https://trustconnectsoftware.com\n\nСайт якобы корпоративного инструмента удалённой поддержки. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен зарегистрирован в январе 2026 года, подделка под реальный бизнес."},
    {"text": "Ссылка: https://xn--80adtgbbrh1afh.xn--p1ai\n\nВы видите punycode. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Это punycode — мошенники маскируют опасные сайты под настоящие."},
    {"text": "Ссылка: https://rostransnadzor.digital\n\nПисьмо от «Ространснадзора» с этой ссылкой. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен .digital часто используется мошенниками."},
    {"text": "Ссылка: https://pcloud.online\n\nСайт якобы облачного хранилища. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Подделка под pCloud."},
    {"text": "Ссылка: https://jewelry-sale-msk.ru\n\nМагазин ювелирных украшений с огромными скидками к праздникам. Это надёжно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! В феврале 2026 года выявлено около 30 мошеннических ювелирных сайтов с однотипным оформлением."},
    {"text": "Ссылка: https://telegram-rose-fortune.ru\n\nСообщение от «Павла Дурова» о розыгрыше подписки. Это правда?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Мошенники выступают от имени Дурова."},
    {"text": "Ссылка: https://zakon-o-podpiskah.ru\n\nПисьмо о скрытых подписках. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Пугают подписками."},
    {"text": "Ссылка: https://фнс-проверка.рф\n\nПисьмо от ФНС о задолженности. Это официально?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Налоговая не рассылает ссылки через подозрительные домены."},
    {"text": "Ссылка: https://gosuslugi-ident.ru\n\nСсылка для подтверждения личности. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Настоящий Госуслуги — gosuslugi.ru."},
    {"text": "Ссылка: https://photo-studio-msk.com\n\nБесплатная фотосессия. Это нормально?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Мошенники просят перевод на карту."},
    {"text": "Ссылка: https://zakaz-buketov.ru\n\nДоставка цветов с предоплатой. Надёжно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "С осторожностью! Многие — однодневки."},
    {"text": "Ссылка: https://telegram-security.ru\n\nСлужба безопасности Telegram. Это настоящий сайт?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Нет! Настоящий Telegram — telegram.org."},
    {"text": "Ссылка: https://sberbank-online.info\n\nВход в личный кабинет. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен .info не относится к Сбербанку."},
    {"text": "Ссылка: https://vk.com.free-vote.ru\n\nСсылка для голосования. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Мошенники рассылают ссылки для голосования, чтобы украсть аккаунт."},
    {"text": "Ссылка: https://google.security-update.com\n\nОбновление безопасности. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен — security-update.com."},
    {"text": "Ссылка: http://apple.com.verify-account.net\n\nПодтверждение аккаунта Apple. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! verify-account.net не имеет отношения к Apple."},
    {"text": "Ссылка: https://www.paypal.com.signin.secure.tk\n\nВход в PayPal. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен .tk подозрительный."},
    {"text": "Ссылка: http://telegram.org-login.xyz\n\nВход в Telegram. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен .xyz."},
    {"text": "Ссылка: https://xn--e1awg7f.xn--p1ai\n\nPunycode для «кино.рф». Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Официальный сайт «кино.рф»."},
]

# ----- 35 вопросов по письмам (актуальные фишинговые сообщения 2026) -----
MESSAGE_QUESTIONS = [
    {"text": "Письмо: «Обнаружено 7 скрытых подписок! Срочно отмените здесь: ссылка»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! Новая схема 2026 года со скрытыми подписками."},
    {"text": "Письмо: «Вы выиграли подписку Telegram Premium от Павла Дурова. Оплатите пошлину»\n\nЭто правда?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Мошенники имитируют розыгрыши от имени Дурова."},
    {"text": "Письмо: «Приглашение на фотосессию. Запись по ссылке»\n\nЧто делать?", "options": ["✅ Перейду", "🚫 Проверю"], "correct": 1, "explanation": "Проверьте! Это может быть схема с фальшивыми фотографами."},
    {"text": "Письмо: «Налоговая задолженность. Оплатите сейчас» со ссылкой\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Налоговая не рассылает ссылки."},
    {"text": "Письмо: «Вы назначены на маникюр. Назовите последние цифры номера» (вы не записывались)\n\nЧто делать?", "options": ["✅ Назову", "🚫 Не буду"], "correct": 1, "explanation": "Не называйте! Новая схема 2026 года — по последним цифрам могут взломать аккаунт."},
    {"text": "Письмо с календарным приглашением без текста, только ссылка\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Календарный фишинг — новая тактика."},
    {"text": "Письмо: «Вам голосовое сообщение» с ссылкой\n\nЭто может быть опасно?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! Мошенники используют CAPTCHA для обхода защиты."},
    {"text": "Письмо от «службы безопасности» с вложением «Акт проверки.rtf»\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Вредоносный файл."},
    {"text": "СМС: «Курьер с цветами не может найти адрес, назовите последние цифры номера»\n\nВаши действия?", "options": ["✅ Назову", "🚫 Не назову"], "correct": 1, "explanation": "Не называйте! Это схема с последними цифрами."},
    {"text": "Письмо: «Скрытые подписки обнаружены. Отмените здесь»\n\nЭто правда?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Фишинг."},
    {"text": "Письмо: «Ваш аккаунт взломан! Срочно перейдите по ссылке»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! Классический фишинг."},
    {"text": "Письмо: «Вы выиграли приз! Переведите 100 рублей за доставку»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! Никогда не платите за выигрыш."},
    {"text": "Письмо от «банка»: «Ваша карта заблокирована, подтвердите данные»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Банк не просит данные по email."},
    {"text": "Письмо: «Служба безопасности Telegram. Перейдите: t.me-login.ru»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Настоящий Telegram — t.me."},
    {"text": "Письмо: «Мама, положи 100 рублей на этот номер» (номер чужой)\n\nТвои действия?", "options": ["✅ Переведу", "🚫 Позвоню маме"], "correct": 1, "explanation": "Позвоните маме! Мошенники."},
    {"text": "Письмо: «Срочный перевод от бабушки, нужна комиссия. Назовите код из СМС»\n\nВаши действия?", "options": ["✅ Назову", "🚫 Положу трубку"], "correct": 1, "explanation": "Никогда не называйте код из СМС."},
    {"text": "Письмо: «Ваш номер участвует в лотерее, отправьте СМС на короткий номер»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да, с короткого номера снимут деньги."},
    {"text": "Письмо от «оператора»: «У вас заканчивается контракт, скажите код из СМС»\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Операторы не просят коды по телефону."},
    {"text": "Письмо: «Ваш родственник в больнице, срочно нужны деньги на операцию»\n\nЧто делать?", "options": ["✅ Переведу", "🚫 Перезвоню родственнику"], "correct": 1, "explanation": "Перезвоните родственнику!"},
    {"text": "Письмо: «Вы записаны на маникюр, назовите последние цифры для подтверждения» (вы не записывались)\n\nВаши действия?", "options": ["✅ Назову", "🚫 Не назову"], "correct": 1, "explanation": "Не называйте!"},
    {"text": "Письмо: «Привет, это ваш новый сосед, заливаю этажом ниже. Скинь 500 рублей на стройматериалы»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Позвоню в УК"], "correct": 1, "explanation": "Позвоните в управляющую компанию."},
    {"text": "Письмо: «Вы выиграли приз, для получения оплатите доставку»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да!"},
    {"text": "Письмо: «Ваш аккаунт взломали, срочно смените пароль по ссылке»\n\nЧто делать?", "options": ["✅ Перейду", "🚫 Не буду"], "correct": 1, "explanation": "Не переходите, зайдите на сайт сами."},
    {"text": "Письмо: «Служба безопасности Госуслуг, ваш аккаунт заблокирован, перейдите по ссылке»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Госуслуги не рассылают такие письма."},
    {"text": "Письмо: «Вам назначена выплата, заполните форму»\n\nЧто делать?", "options": ["✅ Заполню", "🚫 Не буду"], "correct": 1, "explanation": "Не заполняйте, это сбор данных."},
]
while len(MESSAGE_QUESTIONS) < 35:
    MESSAGE_QUESTIONS.append({
        "text": f"Письмо {len(MESSAGE_QUESTIONS)+1}: срочное уведомление со ссылкой.\n\nЭто мошенники?",
        "options": ["✅ Да", "🚫 Нет"],
        "correct": 0,
        "explanation": "Скорее всего, да."
    })

# ----- 25 вопросов по звонкам (актуальные схемы 2026) -----
CALL_QUESTIONS = [
    {"text": "Звонок: «Вас беспокоит ФСБ. Помогите задержать мошенников, переведите деньги на безопасный счёт»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Положу трубку"], "correct": 1, "explanation": "Клади трубку! ФСБ не звонит."},
    {"text": "Звонок: «Это из поликлиники. Назовите код из СМС»\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Поликлиники не просят коды."},
    {"text": "Звонок: «Вам ошибочно перевели 5000 рублей. Верните на этот номер»\n\nЧто делать?", "options": ["✅ Верну", "🚫 Сообщу в банк"], "correct": 1, "explanation": "Не возвращайте! Ловушка."},
    {"text": "Звонок: «Это курьер, у меня цветы для вас. Нужна предоплата 200 рублей»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Откажусь"], "correct": 1, "explanation": "Откажитесь! Курьеры не просят предоплату."},
    {"text": "Звонок: «Привет, я ваш новый сосед, заливаю этажом ниже. Скинь 500 рублей на стройматериалы»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Позвоню в УК"], "correct": 1, "explanation": "Позвоните в УК. Мошенники."},
    {"text": "Звонок: «Вам одобрен кредит! Назовите паспортные данные»\n\nЧто делать?", "options": ["✅ Назову", "🚫 Положу трубку"], "correct": 1, "explanation": "Не называйте! Развод."},
    {"text": "Звонок с неизвестного номера — сброс. Перезванивать?", "options": ["✅ Перезвоню", "🚫 Не буду"], "correct": 1, "explanation": "Не перезванивайте! Платный номер."},
    {"text": "Звонок: «Служба безопасности Wildberries. Ваш заказ заморожен, назовите данные карты»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! Маркетплейсы не звонят."},
    {"text": "Звонок: «Алло, это ваш директор! Срочно переведи 5000 на этот номер» (голос похож)\n\nЧто делать?", "options": ["✅ Переведу", "🚫 Позвоню директору"], "correct": 1, "explanation": "Позвоните директору! Это дипфейк — подделка голоса с помощью ИИ."},
    {"text": "Звонок: «Вас беспокоит Роскомнадзор. Ваши деньги пытаются украсть»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Позвоню в банк"], "correct": 1, "explanation": "Роскомнадзор не занимается деньгами."},
    {"text": "Звонок: «Это фотостудия. Назовите последние цифры номера для подтверждения» (вы не записывались)\n\nВаши действия?", "options": ["✅ Назову", "🚫 Не назову"], "correct": 1, "explanation": "Не называйте! Новая схема — по последним цифрам взламывают аккаунты."},
    {"text": "Звонок: «Мы тестируем новый сервис ЖКХ, скинем файлик, открой его»\n\nОткроете?", "options": ["✅ Открою", "🚫 Не открою"], "correct": 1, "explanation": "Не открывайте! Вирус."},
    {"text": "Звонок: «Ваш аккаунт в Telegram взламывают! Перейдите по ссылке из СМС»\n\nПерейдёте?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Ссылка крадёт аккаунт."},
    {"text": "Звонок: «Вы выиграли приз! Назовите данные карты»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! По телефону не спрашивают данные карты."},
    {"text": "Звонок: «Служба безопасности банка. Назовите код из СМС»\n\nЧто сделает настоящий банк?", "options": ["✅ Попросит код", "🚫 Никогда не спросит"], "correct": 1, "explanation": "Верно! Банк никогда не спрашивает код."},
    {"text": "Звонок с номера мамы: «Дочка, переведи деньги». Голос похож.\n\nТвои действия?", "options": ["✅ Переведу", "🚫 Перезвоню на старый номер"], "correct": 1, "explanation": "Перезвоните! Нейросети подделывают голоса."},
    {"text": "Звонок: «Служба безопасности Google. Ваш аккаунт взломали, продиктуйте пароль»\n\nВаши действия?", "options": ["✅ Продиктую", "🚫 Положу трубку"], "correct": 1, "explanation": "Google никогда не звонит."},
    {"text": "Звонок: «Это ваш участковый. Назовите паспортные данные»\n\nВаши действия?", "options": ["✅ Назову", "🚫 Позвоню в отделение"], "correct": 1, "explanation": "Полиция не запрашивает данные по телефону."},
    {"text": "Звонок: «Вы попали под следствие за терроризм, переведите деньги на спецсчёт»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Положу трубку и позвоню 102"], "correct": 1, "explanation": "Запугивание, не ведитесь!"},
    {"text": "Звонок от «соседа»: «У нас домофон ломают, скажи код из СМС»\n\nЭто норм?", "options": ["✅ Скажу", "🚫 Позвоню в управляйку"], "correct": 1, "explanation": "Развод! Соседи не просят коды."},
    {"text": "Звонок: «Привет, я из фотостудии! Назови последние цифры»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! По цифрам взломают аккаунт."},
    {"text": "Звонок: «Тестируем сервис ЖКХ, скинем файлик, открой»\n\nОткроете?", "options": ["✅ Открою", "🚫 Не открою"], "correct": 1, "explanation": "Нет! Вирус."},
    {"text": "Звонок: «Вам перевод от бабушки, нужна комиссия. Скажите код из СМС»\n\nЧто делать?", "options": ["✅ Скажу", "🚫 Положу трубку"], "correct": 1, "explanation": "Клади трубку! Развод."},
    {"text": "Звонок: «Ваш аккаунт в Telegram взламывают! Перейдите по ссылке»\n\nПерейдёшь?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Ссылка украдёт аккаунт."},
    {"text": "Звонок: «Служба безопасности Wildberries. Ваш заказ заморожен»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! WB не звонит."},
]
while len(CALL_QUESTIONS) < 25:
    CALL_QUESTIONS.append({
        "text": f"Звонок {len(CALL_QUESTIONS)+1}: неизвестный представляется сотрудником банка.\n\nВаши действия?",
        "options": ["✅ Продолжу разговор", "🚫 Положу трубку"],
        "correct": 1,
        "explanation": "Положите трубку и перезвоните в банк."
    })

QUESTIONS = {
    "domains": DOMAIN_QUESTIONS,
    "messages": MESSAGE_QUESTIONS,
    "calls": CALL_QUESTIONS,
}

LEVELS_TOTAL = {
    "domains": len(DOMAIN_QUESTIONS),
    "messages": len(MESSAGE_QUESTIONS),
    "calls": len(CALL_QUESTIONS),
}

# =============== ПЕРЕМЕШИВАНИЕ ВОПРОСОВ ===============
def init_user_data():
    """Создаёт случайный порядок вопросов для каждого нового пользователя"""
    return {
        "domains": {
            "order": random.sample(range(LEVELS_TOTAL["domains"]), LEVELS_TOTAL["domains"]),
            "pos": 0
        },
        "messages": {
            "order": random.sample(range(LEVELS_TOTAL["messages"]), LEVELS_TOTAL["messages"]),
            "pos": 0
        },
        "calls": {
            "order": random.sample(range(LEVELS_TOTAL["calls"]), LEVELS_TOTAL["calls"]),
            "pos": 0
        }
    }

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_data(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = init_user_data()
        save_data(data)
    return data[uid]

def save_user_data(user_id, user_data):
    data = load_data()
    data[str(user_id)] = user_data
    save_data(data)

def answer_correct(user_id, category):
    user_data = get_user_data(user_id)
    user_data[category]["pos"] += 1
    save_user_data(user_id, user_data)

def reset_progress(user_id):
    user_data = init_user_data()
    save_user_data(user_id, user_data)

def total_level(user_id):
    user_data = get_user_data(user_id)
    return user_data["domains"]["pos"] + user_data["messages"]["pos"] + user_data["calls"]["pos"]

# =============== КЛАВИАТУРЫ ===============
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🖥 Отличи домен", callback_data="cat_domains"),
         InlineKeyboardButton("📧 Отличи письмо", callback_data="cat_messages")],
        [InlineKeyboardButton("📞 Отличи звонок", callback_data="cat_calls"),
         InlineKeyboardButton("📚 Изучить материалы", callback_data="learn")],
        [InlineKeyboardButton("❓ Случайное задание", callback_data="random"),
         InlineKeyboardButton("📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton("ℹ️ О проекте", callback_data="about")]
    ]
    return InlineKeyboardMarkup(keyboard)

def answer_keyboard(category, pos, options):
    buttons = [InlineKeyboardButton(opt, callback_data=f"ans_{category}_{pos}_{i}") for i, opt in enumerate(options)]
    keyboard = [buttons]
    keyboard.append([InlineKeyboardButton("⬅️ В меню", callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)

# =============== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===============
async def safe_answer(query, text=None, show_alert=False):
    try:
        await query.answer(text, show_alert=show_alert)
    except BadRequest as e:
        if "PEER_FLOOD" in str(e):
            await asyncio.sleep(5)
            await query.answer(text, show_alert=show_alert)
        else:
            logger.error(f"Answer error: {e}")

async def safe_edit(query, text, reply_markup=None):
    try:
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except BadRequest as e:
        if "PEER_FLOOD" in str(e):
            await asyncio.sleep(5)
            await query.edit_message_text(
                text,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
        elif "Message is not modified" in str(e):
            pass
        else:
            logger.error(f"Edit error: {e}")

# =============== УЛУЧШЕННЫЙ СКАМ-ДЕТЕКТОР (2026) ===============
# Опасные доменные зоны
CRITICAL_TLDS = ['.xin', '.bond', '.cfd', '.today', '.lol', '.zip', '.cam', '.help', '.win']
HIGH_RISK_TLDS = ['.top', '.xyz', '.shop', '.click', '.online', '.site', '.website', '.space', '.club', '.cc', '.pw', '.ml', '.tk', '.digital']
MEDIUM_RISK_TLDS = ['.app', '.arpa', '.io', '.me', '.info', '.buzz', '.live', '.rocks']

# Фразы для телефонных звонков (вес 5)
PHONE_SCAM_PHRASES = [
    "переключаю вас на сотрудника центробанка", "переключаю на сотрудника правоохранительных органов",
    "финансирование запрещенной организации", "безопасный счёт", "задекларировать денежные средства",
    "ваш аккаунт на госуслугах взломан", "зафиксирована подозрительная операция",
    "оформили кредит на ваше имя", "продлить действие сим-карты", "звоню по поводу удаленной работы",
    "отдел курьерской доставки", "ваш родственник попал в беду", "помогите задержать мошенников",
    "ваша карта взломана", "ошибочный перевод", "вы выиграли приз", "скинь паспорт для оформления",
    "участие в спецоперации", "токенизация карт"
]

# Фразы для писем (вес 3)
MESSAGE_SCAM_PHRASES = [
    "беспокоит директор департамента", "это ты на фото", "оплатите задолженность",
    "расчёт премий", "пароль к вашему аккаунту изменён", "нарушение корпоративной политики",
    "условия тарифа вашей карты обновлены", "внесено постановление о предоставлении компенсации",
    "вам одобрена высокооплачиваемая вакансия", "перезвоните по указанному номеру",
    "авторизация в аккаунте с помощью электронной подписи", "выгрузка документов",
    "вход с нового ip-адреса", "кто-то воспользовался вашими данными", "ваш код для подтверждения",
    "b2b-gospodderzka", "clients-gospodderzka", "gospodderzka"
]

# Фразы для детей (вес 4)
KIDS_SCAM_PHRASES = [
    "ты передал персональные данные мошенникам", "тебя заберут в приют", "спасти семью",
    "войди в мой apple id", "сдай аккаунт в аренду", "проголосуй за мою сестру",
    "внештатный спецагент", "забери деньги", "аккаунт будет удален"
]

# Общие слова-триггеры (вес 2)
GENERAL_SCAM_WORDS = [
    "срочно", "немедленно", "сегодня", "сейчас", "выигрыш", "приз", "розыгрыш", "миллион",
    "подарок", "скидка", "акция", "бесплатно", "заблокирована", "заблокирован", "удалят",
    "код из смс", "код подтверждения", "cvv", "номер карты", "последние цифры номера",
    "скрытые подписки", "предоплата", "оплатите доставку", "инвестиции", "криптовалюта"
]

# Безличные обращения (вес 1)
IMPERSONAL_PHRASES = ["уважаемый клиент", "уважаемый абонент", "дорогой пользователь"]

def check_tld_risk(domain):
    domain_lower = domain.lower()
    for tld in CRITICAL_TLDS:
        if domain_lower.endswith(tld):
            return 5, f"Критически опасная доменная зона {tld}"
    for tld in HIGH_RISK_TLDS:
        if domain_lower.endswith(tld):
            return 3, f"Опасная доменная зона {tld}"
    for tld in MEDIUM_RISK_TLDS:
        if domain_lower.endswith(tld):
            return 2, f"Подозрительная доменная зона {tld}"
    return 0, None

def check_typosquatting(domain):
    domain_lower = domain.lower()
    patterns = {
        r'g00gle': 'google', r'g0ogle': 'google', r'gооgle': 'google',
        r'аpple': 'apple', r'sberbаnk': 'sberbank', r'yandеx': 'yandex',
        r'tеlegram': 'telegram', r'whatsарр': 'whatsapp'
    }
    for pattern, safe in patterns.items():
        if re.search(pattern, domain_lower):
            return 4, f"Подмена символов: похоже на {safe}"
    return 0, None

def scam_detector(text):
    text_lower = text.lower()
    total_score = 0
    reasons = []

    # Поиск ссылок
    url_pattern = re.compile(r'(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)')
    urls = url_pattern.findall(text_lower)
    if urls:
        for url in urls:
            parsed = urlparse(url if '://' in url else 'http://' + url)
            domain = parsed.netloc or parsed.path.split('/')[0]
            domain = domain.split(':')[0]
            tld_score, tld_reason = check_tld_risk(domain)
            if tld_score:
                total_score += tld_score
                reasons.append(tld_reason)
            typo_score, typo_reason = check_typosquatting(domain)
            if typo_score:
                total_score += typo_score
                reasons.append(typo_reason)
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
                total_score += 5
                reasons.append("Сайт использует IP-адрес вместо домена")
            if any(short in domain for short in ['bit.ly', 'clck.ru', 'tinyurl', 'goo.gl', 't.co']):
                total_score += 4
                reasons.append("Сокращённая ссылка (скрывает настоящий адрес)")

    # Проверка фраз
    for phrase in PHONE_SCAM_PHRASES:
        if phrase in text_lower:
            total_score += 5
            reasons.append(f"Фраза телефонных мошенников: «{phrase}»")
            break
    for phrase in MESSAGE_SCAM_PHRASES:
        if phrase in text_lower:
            total_score += 3
            reasons.append(f"Фраза фишинговых писем: «{phrase}»")
            break
    for phrase in KIDS_SCAM_PHRASES:
        if phrase in text_lower:
            total_score += 4
            reasons.append(f"Схема для детей: «{phrase}»")
            break
    matched_general = [w for w in GENERAL_SCAM_WORDS if w in text_lower]
    if matched_general:
        total_score += 2 * min(len(matched_general), 3)
        reasons.append(f"Общие признаки: {', '.join(matched_general[:3])}")
    for phrase in IMPERSONAL_PHRASES:
        if phrase in text_lower:
            total_score += 1
            reasons.append(f"Безличное обращение: «{phrase}»")
            break

    # Кириллица в ссылке
    if urls and re.search(r'[а-яА-Я]', str(urls)):
        total_score += 3
        reasons.append("Ссылка содержит кириллицу (возможная подмена)")

    # Вердикт
    if total_score >= 8:
        verdict = "🔴 КРИТИЧЕСКИ ОПАСНО"
        advice = "НЕ ПЕРЕХОДИТЕ ПО ССЫЛКЕ и НЕ СООБЩАЙТЕ ДАННЫЕ! Это мошенники."
    elif total_score >= 4:
        verdict = "🟠 ПОДОЗРИТЕЛЬНО"
        advice = "Будьте осторожны. Вероятно, это попытка обмана."
    elif total_score >= 1:
        verdict = "🟡 ВНИМАНИЕ"
        advice = "Есть отдельные признаки мошенничества. Проверьте информацию."
    else:
        verdict = "🟢 ПРЕДВАРИТЕЛЬНО БЕЗОПАСНО"
        advice = "Явных признаков мошенничества не обнаружено."

    result = f"{verdict}\n\n"
    if reasons:
        result += "🔍 Найдены признаки:\n• " + "\n• ".join(reasons[:5])
        if len(reasons) > 5:
            result += f"\n• и ещё {len(reasons)-5} признаков"
        result += f"\n\n⚠️ Уровень риска: {total_score} баллов.\n\n"
    else:
        result += "⚠️ Явных признаков не найдено.\n\n"
    result += f"💡 {advice}"
    return result

# =============== ОБРАБОТЧИКИ ===============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🛡️ Добро пожаловать в Cyber Shield, {user.first_name}!\n\n"
        "Этот бот научит вас защищаться от кибермошенников.\n"
        "100 уровней: домены, письма, звонки.\n"
        "Вопросы перемешиваются для каждого пользователя.\n\n"
        "Выберите действие:",
        reply_markup=main_menu(),
        disable_web_page_preview=True
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Справка\n\n"
        "/start – запуск\n"
        "/help – эта справка\n"
        "/reset – сброс прогресса\n\n"
        "Отправьте мне подозрительное сообщение – я проанализирую.",
        disable_web_page_preview=True
    )

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    reset_progress(user_id)
    await update.message.reply_text("✅ Прогресс сброшен. Вопросы перемешаны заново.", disable_web_page_preview=True)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await safe_answer(query)
    data = query.data
    user_id = query.from_user.id

    if data == "back_to_main":
        await safe_edit(query, "Главное меню:", reply_markup=main_menu())
        return

    if data == "learn":
        text = f"📚 Обучающие материалы:\n{LEARN_URL}\n\nПереходите и изучайте!"
        keyboard = [[InlineKeyboardButton("⬅️ В меню", callback_data="back_to_main")]]
        await safe_edit(query, text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == "stats":
        user_data = get_user_data(user_id)
        dom_pos = user_data["domains"]["pos"]
        msg_pos = user_data["messages"]["pos"]
        call_pos = user_data["calls"]["pos"]
        total = dom_pos + msg_pos + call_pos
        text = (f"📊 Статистика\n\n"
                f"🛡️ Всего пройдено: {total}\n"
                f"🖥 Домены: {dom_pos}/{LEVELS_TOTAL['domains']}\n"
                f"📧 Письма: {msg_pos}/{LEVELS_TOTAL['messages']}\n"
                f"📞 Звонки: {call_pos}/{LEVELS_TOTAL['calls']}\n\n"
                f"Так держать!")
        await safe_edit(query, text, reply_markup=main_menu())
        return

    if data == "about":
        text = ("ℹ️ О проекте\n\n"
                "Автор: MrBulbaOO1 (12 лет, Брест)\n"
                "Конкурс #КиберПраво\n\n"
                "Контакты: a.carantine@gmail.com\n"
                "Бот: @MrBulbaOO1")
        await safe_edit(query, text, reply_markup=main_menu())
        return

    if data.startswith("cat_"):
        category = data.replace("cat_", "")
        user_data = get_user_data(user_id)
        pos = user_data[category]["pos"]
        if pos >= LEVELS_TOTAL[category]:
            await safe_edit(query, "🎉 Вы прошли все задания в этой категории!", reply_markup=main_menu())
            return
        q_index = user_data[category]["order"][pos]
        question = QUESTIONS[category][q_index]
        await safe_edit(query,
                        f"🔍 Уровень {pos+1} в категории «{category}»:\n\n{question['text']}",
                        reply_markup=answer_keyboard(category, pos, question['options']))
        return

    if data.startswith("ans_"):
        parts = data.split('_')
        if len(parts) < 4:
            return
        category = parts[1]
        pos = int(parts[2])
        answer_idx = int(parts[3])
        user_data = get_user_data(user_id)
        if pos != user_data[category]["pos"]:
            await safe_edit(query, "⏳ Задание устарело. Начните новое.", reply_markup=main_menu())
            return
        q_index = user_data[category]["order"][pos]
        question = QUESTIONS[category][q_index]
        correct = question['correct']
        if answer_idx == correct:
            answer_correct(user_id, category)
            new_pos = pos + 1
            reply = f"✅ Правильно!\n\n{question['explanation']}\n\nВаш уровень в категории «{category}» теперь {new_pos}."
        else:
            reply = f"❌ Неправильно.\n\n{question['explanation']}\n\nПопробуйте ещё раз."
        keyboard = [
            [InlineKeyboardButton("▶️ Следующее", callback_data=f"cat_{category}")],
            [InlineKeyboardButton("⬅️ Меню", callback_data="back_to_main")]
        ]
        await safe_edit(query, reply, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == "random":
        cat = random.choice(list(QUESTIONS.keys()))
        q_index = random.randint(0, LEVELS_TOTAL[cat] - 1)
        question = QUESTIONS[cat][q_index]
        keyboard = [
            [InlineKeyboardButton(question['options'][0], callback_data=f"rand_{cat}_{q_index}_0"),
             InlineKeyboardButton(question['options'][1], callback_data=f"rand_{cat}_{q_index}_1")],
            [InlineKeyboardButton("⬅️ Меню", callback_data="back_to_main")]
        ]
        await safe_edit(query, f"🎲 Случайное задание:\n\n{question['text']}", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data.startswith("rand_"):
        parts = data.split('_')
        if len(parts) < 4:
            return
        cat = parts[1]
        q_index = int(parts[2])
        answer_idx = int(parts[3])
        question = QUESTIONS[cat][q_index]
        correct = question['correct']
        if answer_idx == correct:
            reply = f"✅ Правильно!\n\n{question['explanation']}"
        else:
            reply = f"❌ Неправильно.\n\n{question['explanation']}"
        await safe_edit(query, reply, reply_markup=main_menu())
        return

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = scam_detector(text)
    await update.message.reply_text(response, disable_web_page_preview=True)

# =============== ЗАПУСК ===============
def main():
    print("\n" + "="*50)
    print("Cyber Shield Bot v12.0")
    print("Автор: MrBulbaOO1, 12 лет, Брест")
    print("Конкурс: #КиберПраво")
    print("Актуальные схемы мошенничества 2026 года")
    print("="*50 + "\n")
    try:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("reset", reset_command))
        app.add_handler(CallbackQueryHandler(button_click))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
        logger.info("Бот запущен!")
        print("✅ Бот работает! Нажмите Ctrl+C для остановки.\n")
        app.run_polling()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        print(f"\n❌ Ошибка: {e}\nПроверьте токен и интернет.")

if __name__ == "__main__":
    main()