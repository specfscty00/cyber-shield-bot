# -*- coding: utf-8 -*-
"""
Telegram-бот Cyber Shield
Автор: MrBulbaOO1, 12 лет, Брест
Конкурс #КиберПраво
Версия: 9.0 – для развёртывания на Render (токен из переменных окружения)
"""

import os
import json
import random
import logging
import asyncio
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# =============== ПРОВЕРКА УСТАНОВКИ ===============
try:
    from telegram import Update
except ImportError:
    print("\n" + "="*50)
    print("ОШИБКА: Библиотека python-telegram-bot не установлена!")
    print("Выполните в командной строке: pip install python-telegram-bot")
    print("="*50 + "\n")
    sys.exit(1)

# =============== НАСТРОЙКИ ===============
# Токен берётся из переменных окружения (настраивается на Render)
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    print("\n" + "="*50)
    print("ОШИБКА: Токен не найден!")
    print("Добавьте переменную окружения TOKEN на Render")
    print("="*50 + "\n")
    sys.exit(1)

LEARN_URL = "https://telegra.ph/Cyber-Shield-03-04"
DATA_FILE = "user_data.json"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# =============== ВОПРОСЫ (ПОЛНАЯ ВЕРСИЯ 100 ШТУК) ===============

# ----- 40 вопросов по доменам -----
DOMAIN_QUESTIONS = [
    # Безопасные (0)
    {"text": "Ссылка: https://www.gosuslugi.ru\n\nЭто официальный сайт?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Это настоящий портал Госуслуг."},
    {"text": "Ссылка: https://www.sberbank.ru\n\nЭто безопасный сайт?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Официальный сайт Сбербанка."},
    {"text": "Ссылка: https://www.mos.ru\n\nЭто официальный сайт мэрии Москвы?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, это официальный портал mos.ru."},
    {"text": "Ссылка: https://www.nalog.gov.ru\n\nЭто сайт ФНС?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Официальный сайт Федеральной налоговой службы."},
    {"text": "Ссылка: https://www.google.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Google, всё нормально."},
    {"text": "Ссылка: https://www.youtube.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "YouTube, можно смотреть."},
    {"text": "Ссылка: https://www.vtb.ru\n\nЭто официальный сайт ВТБ?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, это ВТБ."},
    {"text": "Ссылка: https://www.tinkoff.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Тинькофф, официально."},
    {"text": "Ссылка: https://www.ozon.ru\n\nЭто маркетплейс?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Озон, можно покупать."},
    {"text": "Ссылка: https://www.wildberries.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Wildberries, официальный сайт."},
    {"text": "Ссылка: https://www.avito.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Авито, популярная доска объявлений."},
    {"text": "Ссылка: https://www.cian.ru\n\nЭто сайт недвижимости?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "ЦИАН, официальный."},
    {"text": "Ссылка: https://www.2gis.ru\n\nЭто карты?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "2ГИС, можно доверять."},
    {"text": "Ссылка: https://www.kaspersky.ru\n\nЭто антивирус?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Лаборатория Касперского, официально."},
    {"text": "Ссылка: https://www.mail.ru\n\nЭто почта?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Mail.ru, всё ок."},
    {"text": "Ссылка: https://www.rambler.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Рамблер, старый портал."},
    {"text": "Ссылка: https://www.yandex.ru\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Яндекс, поисковик."},
    {"text": "Ссылка: https://www.microsoft.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Майкрософт, официально."},
    {"text": "Ссылка: https://www.apple.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Apple, официально."},
    {"text": "Ссылка: https://www.netflix.com\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Netflix, стриминг."},
    # Фишинговые (1)
    {"text": "Ссылка: https://xn--80adtgbbrh1afh.xn--p1ai\n\nВы видите punycode. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Это punycode — мошенники могут маскировать опасные сайты под настоящие."},
    {"text": "Ссылка: https://rostransnadzor.digital\n\nВам пришло письмо от «Ространснадзора» с этой ссылкой. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Это домен мошенников."},
    {"text": "Ссылка: https://pcloud.online\n\nСайт предлагает войти в облачное хранилище. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Это подделка под pCloud."},
    {"text": "Ссылка: https://flowers-shop-msk.ru\n\nМагазин цветов с огромными скидками к 8 Марта. Это надёжно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Мошенники создают фейковые сайты с предпраздничными распродажами."},
    {"text": "Ссылка: https://gift-card-2026.ru\n\nСайт предлагает подарочные сертификаты. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Под видом подарочных сертификатов распространяют вредоносные приложения."},
    {"text": "Ссылка: https://telegram-rose-fortune.ru\n\nПришло сообщение от «Павла Дурова» о розыгрыше подписки. Это правда?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Мошенники выступают от имени Дурова."},
    {"text": "Ссылка: https://zakon-o-podpiskah.ru\n\nПисьмо о новых скрытых подписках с просьбой срочно отменить. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Мошенники пугают скрытыми подписками."},
    {"text": "Ссылка: https://фнс-проверка.рф\n\nПисьмо от ФНС о задолженности. Это официально?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Налоговая не рассылает ссылки через подозрительные домены."},
    {"text": "Ссылка: https://gosuslugi-ident.ru\n\nСсылка для подтверждения личности. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Настоящий домен Госуслуг — только gosuslugi.ru."},
    {"text": "Ссылка: https://photo-studio-msk.com\n\nФотограф предлагает бесплатную фотосессию, нужно оплатить только материалы. Это нормально?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Мошенники прикрываются начинающими фотографами."},
    {"text": "Ссылка: https://zakaz-buketov.ru\n\nСайт по доставке цветов с предоплатой. Это надёжно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "С осторожностью! Многие такие сайты — однодневки."},
    {"text": "Ссылка: https://telegram-security.ru\n\nЯкобы служба безопасности Telegram. Это настоящий сайт?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Нет! Настоящий Telegram — только telegram.org."},
    {"text": "Ссылка: https://sberbank-online.info\n\nСайт предлагает войти в личный кабинет. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен .info не имеет отношения к Сбербанку."},
    {"text": "Ссылка: https://vk.com.free-vote.ru\n\nЭто ссылка для голосования. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен — free-vote.ru, vk только в поддомене."},
    {"text": "Ссылка: https://google.security-update.com\n\nСсылка на обновление безопасности. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен — security-update.com, Google не при делах."},
    {"text": "Ссылка: http://apple.com.verify-account.net\n\nПодтверждение аккаунта Apple. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! verify-account.net не имеет отношения к Apple."},
    {"text": "Ссылка: https://www.paypal.com.signin.secure.tk\n\nВход в PayPal. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен .tk, подозрительно."},
    {"text": "Ссылка: http://telegram.org-login.xyz\n\nВход в Telegram. Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Домен .xyz, login.xyz — ловушка."},
    {"text": "Ссылка: https://xn--e1awg7f.xn--p1ai\n\nЭто punycode для «кино.рф». Это безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Это punycode, но на самом деле это официальный сайт «кино.рф»."},
    {"text": "Ссылка: http://online.alfabank.by\n\nЭто официальный сайт Альфа-Банка в Беларуси?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 0, "explanation": "Да, это официальный сайт Альфа-Банка в Беларуси."},
]

# ----- 35 вопросов по письмам -----
MESSAGE_QUESTIONS = [
    {"text": "Письмо: «Обнаружено 7 скрытых подписок! Срочно отмените здесь: ссылка»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! Это новая схема со скрытыми подписками."},
    {"text": "Письмо: «Вы выиграли подписку Telegram Premium от Павла Дурова. Оплатите пошлину»\n\nЭто правда?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Мошенники имитируют розыгрыши от имени Дурова."},
    {"text": "Письмо: «Приглашение на фотосессию. Запись по ссылке»\n\nЧто делать?", "options": ["✅ Перейду", "🚫 Проверю"], "correct": 1, "explanation": "Проверьте! Это может быть схема с фальшивыми фотографами."},
    {"text": "Письмо: «Налоговая задолженность. Оплатите сейчас, иначе пени» со ссылкой\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Налоговая не рассылает ссылки в письмах."},
    {"text": "Письмо: «Вы назначены на маникюр 5 марта. Назовите последние цифры номера для подтверждения» (вы не записывались)\n\nЧто делать?", "options": ["✅ Назову", "🚫 Не буду"], "correct": 1, "explanation": "Не называйте! Это новая схема с последними цифрами номера."},
    {"text": "Письмо с календарным приглашением от «коллеги» без текста, только ссылка в описании\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Календарный фишинг — новая тактика."},
    {"text": "Письмо: «Вам голосовое сообщение» с ссылкой\n\nЭто может быть опасно?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! Мошенники используют CAPTCHA для обхода защиты."},
    {"text": "Письмо от «службы безопасности» с вложением «Акт проверки транспортного средства.rtf»\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Это вредоносный файл."},
    {"text": "СМС: «Курьер с цветами не может найти адрес, назовите последние цифры номера для подтверждения»\n\nВаши действия?", "options": ["✅ Назову", "🚫 Не назову"], "correct": 1, "explanation": "Не называйте! Это схема с последними цифрами."},
    {"text": "Письмо: «Скрытые подписки обнаружены. Отмените здесь, чтобы не списывали деньги»\n\nЭто правда?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Это фишинг."},
    {"text": "Письмо: «Ваш аккаунт взломан! Срочно перейдите по ссылке»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! Классический фишинг."},
    {"text": "Письмо: «Вы выиграли приз! Для получения переведите 100 рублей за доставку»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! Никогда не платите за выигрыш."},
    {"text": "Письмо от «банка»: «Ваша карта заблокирована, подтвердите данные»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Банк не просит данные по email."},
    {"text": "Письмо: «Служба безопасности Telegram. Кто-то пытается войти. Перейдите: t.me-login.ru»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Настоящий Telegram — t.me."},
    {"text": "Письмо: «Мама, положи 100 рублей на этот номер, я потом объясню» (номер чужой)\n\nТвои действия?", "options": ["✅ Переведу", "🚫 Позвоню маме"], "correct": 1, "explanation": "Позвоните маме! Это мошенники."},
    {"text": "Письмо: «Срочный перевод от бабушки, нужна комиссия, назовите код из СМС»\n\nВаши действия?", "options": ["✅ Назову", "🚫 Положу трубку"], "correct": 1, "explanation": "Никогда не называйте код из СМС."},
    {"text": "Письмо: «Ваш номер участвует в лотерее, отправьте СМС на короткий номер»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да, с короткого номера снимут деньги."},
    {"text": "Письмо от «оператора»: «У вас заканчивается контракт, скажите код из СМС»\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Операторы не просят коды по телефону."},
    {"text": "Письмо: «Ваш родственник в больнице, срочно нужны деньги на операцию»\n\nЧто делать?", "options": ["✅ Переведу", "🚫 Перезвоню родственнику"], "correct": 1, "explanation": "Перезвоните родственнику!"},
    {"text": "Письмо: «Вы записаны на маникюр, назовите последние цифры для подтверждения» (вы не записывались)\n\nВаши действия?", "options": ["✅ Назову", "🚫 Не назову"], "correct": 1, "explanation": "Не называйте!"},
    {"text": "Письмо: «Привет, это ваш новый сосед, заливаю этажом ниже. Скинь 500 рублей на стройматериалы»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Позвоню в УК"], "correct": 1, "explanation": "Позвоните в управляющую компанию."},
    {"text": "Письмо: «Вы выиграли приз, для получения оплатите доставку»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да!"},
    {"text": "Письмо: «Ваш аккаунт взломали, срочно смените пароль по ссылке»\n\nЧто делать?", "options": ["✅ Перейду", "🚫 Не буду"], "correct": 1, "explanation": "Не переходите, зайдите на сайт сами."},
    {"text": "Письмо: «Служба безопасности Госуслуг, ваш аккаунт заблокирован, перейдите по ссылке»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! Госуслуги не рассылают такие письма."},
    {"text": "Письмо: «Вам назначена выплата, заполните форму»\n\nЧто делать?", "options": ["✅ Заполню", "🚫 Не буду"], "correct": 1, "explanation": "Не заполняйте, это сбор данных."},
    {"text": "Письмо: «Ваша посылка задержана, подтвердите доставку по ссылке»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да, это типичный фишинг."},
    {"text": "Письмо: «Служба безопасности WhatsApp. Новое правило конфиденциальности, перейдите для подтверждения»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! WhatsApp не рассылает такие письма."},
    {"text": "Письмо: «Ваш аккаунт будет деактивирован, обновите данные» со ссылкой\n\nЧто делать?", "options": ["✅ Перейду", "🚫 Не буду"], "correct": 1, "explanation": "Не переходите, войдите на сайт вручную."},
    {"text": "Письмо от имени знакомого: «Привет, посмотри это видео» со ссылкой\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Скорее всего, аккаунт взломали."},
    {"text": "Письмо: «Срочная проверка безопасности вашего Apple ID» со ссылкой\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да, Apple не просит переходить по ссылкам в письмах."},
    {"text": "Письмо: «Вам пришло налоговое уведомление, скачайте квитанцию» с вложением\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет, налоговая присылает уведомления через Госуслуги."},
    {"text": "Письмо: «Подтвердите согласие на обработку персональных данных» со ссылкой\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг, не переходите."},
    {"text": "Письмо: «Розыгрыш от банка Тинькофф, заполните анкету» со ссылкой\n\nЭто правда?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет, это мошенники."},
    {"text": "Письмо: «Ваш пароль истек, смените его здесь» со ссылкой\n\nВаши действия?", "options": ["✅ Перейду", "🚫 Не буду"], "correct": 1, "explanation": "Не переходите, зайдите на официальный сайт."},
    {"text": "Письмо: «Служба безопасности VK. Подозрительная активность, подтвердите вход» со ссылкой\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! VK не рассылает такие письма."},
]

# ----- 25 вопросов по звонкам -----
CALL_QUESTIONS = [
    {"text": "Звонок: «Вас беспокоит ФСБ. Помогите задержать мошенников, переведите деньги на безопасный счёт»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Положу трубку"], "correct": 1, "explanation": "Клади трубку! ФСБ не работает через звонки."},
    {"text": "Звонок: «Это из поликлиники. Проверка записи к врачу. Назовите код из СМС»\n\nЭто нормально?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Поликлиники не просят коды."},
    {"text": "Звонок: «Вам ошибочно перевели 5000 рублей. Верните на этот номер карты»\n\nЧто делать?", "options": ["✅ Верну", "🚫 Сообщу в банк"], "correct": 1, "explanation": "Не возвращайте! Это ловушка."},
    {"text": "Звонок: «Это курьер, у меня цветы для вашей девушки. Нужна предоплата 200 рублей на карту» (вы не заказывали)\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Откажусь"], "correct": 1, "explanation": "Откажитесь! Курьеры не просят предоплату на карту."},
    {"text": "Звонок: «Привет, я ваш новый сосед, заливаю этажом ниже. Скинь 500 рублей на стройматериалы»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Позвоню в УК"], "correct": 1, "explanation": "Позвоните в Управляющую компанию."},
    {"text": "Звонок: «Вам одобрен кредит! Назовите паспортные данные для получения»\n\nЧто делать?", "options": ["✅ Назову", "🚫 Положу трубку"], "correct": 1, "explanation": "Не называйте! Это развод."},
    {"text": "Звонок с неизвестного номера — сброс. Перезванивать?", "options": ["✅ Перезвоню", "🚫 Не буду"], "correct": 1, "explanation": "Не перезванивайте! Это может быть платный номер."},
    {"text": "Звонок: «Служба безопасности Wildberries. Ваш заказ заморожен, назовите данные карты»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! Маркетплейсы не звонят."},
    {"text": "Звонок: «Алло, это ваш директор! Срочно переведи 5000 на этот номер» (голос похож)\n\nЧто делать?", "options": ["✅ Переведу", "🚫 Позвоню директору лично"], "correct": 1, "explanation": "Позвоните директору! Голос могут подделать."},
    {"text": "Звонок: «Вас беспокоит Роскомнадзор. Ваши деньги пытаются украсть, переведите на безопасный счёт»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Позвоню в банк"], "correct": 1, "explanation": "Роскомнадзор не занимается деньгами!"},
    {"text": "Звонок: «Это фотостудия. Я сейчас позвоню с номера, назови последние цифры, чтобы подтвердить запись» (вы не записывались)\n\nВаши действия?", "options": ["✅ Назову", "🚫 Не назову"], "correct": 1, "explanation": "Не называйте! Это новая схема."},
    {"text": "Звонок: «Мы тестируем новый сервис ЖКХ, сейчас скинем файлик, открой его»\n\nОткроете?", "options": ["✅ Открою", "🚫 Не открою"], "correct": 1, "explanation": "Не открывайте! Это может быть вирус."},
    {"text": "Звонок: «Ваш аккаунт в Telegram взламывают! Срочно перейдите по ссылке из СМС»\n\nПерейдёте?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Ссылка крадёт аккаунт."},
    {"text": "Звонок: «Вы выиграли приз! Для получения назовите данные карты»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! По телефону не спрашивают данные карты."},
    {"text": "Звонок: «Здравствуйте, это служба безопасности банка. Назовите код из СМС для отмены операции»\n\nЧто сделает настоящий банк?", "options": ["✅ Попросит код", "🚫 Никогда не спросит"], "correct": 1, "explanation": "Верно! Банк никогда не спрашивает код из СМС."},
    {"text": "Звонок с номера мамы: «Дочка, у меня проблемы, срочно переведи 500 рублей». Голос похож.\n\nТвои действия?", "options": ["✅ Переведу", "🚫 Перезвоню на старый номер"], "correct": 1, "explanation": "Перезвоните! Нейросети подделывают голоса."},
    {"text": "Звонок: «Служба безопасности Google. Ваш аккаунт взломали, продиктуйте пароль»\n\nВаши действия?", "options": ["✅ Продиктую", "🚫 Положу трубку"], "correct": 1, "explanation": "Google никогда не звонит."},
    {"text": "Звонок: «Это ваш участковый. Назовите паспортные данные для сверки»\n\nВаши действия?", "options": ["✅ Назову", "🚫 Позвоню в отделение"], "correct": 1, "explanation": "Полиция не запрашивает данные по телефону."},
    {"text": "Звонок: «Вы попали под следствие за терроризм, переведите деньги на спецсчёт»\n\nВаши действия?", "options": ["✅ Переведу", "🚫 Положу трубку и позвоню 102"], "correct": 1, "explanation": "Это запугивание, не ведитесь!"},
    {"text": "Звонок от «соседа»: «Здарова, я сосед снизу! У нас домофон ломают, скажи код из СМС для временного входа»\n\nЭто норм?", "options": ["✅ Скажу", "🚫 Позвоню в управляйку"], "correct": 1, "explanation": "Развод! Соседи не просят коды."},
    {"text": "Звонок: «Привет, я из фотостудии! Я сейчас позвоню с номера, назови последние цифры, чтобы подтвердить запись»\n\nЭто безопасно?", "options": ["✅ Безопасно", "🚫 Фишинг"], "correct": 1, "explanation": "Фишинг! По последним цифрам могут взломать аккаунт."},
    {"text": "Звонок: «Мы тестируем новый сервис ЖКХ, сейчас скинем файлик, открой его»\n\nОткроете файл?", "options": ["✅ Открою", "🚫 Не открою"], "correct": 1, "explanation": "Нет! Это вирус."},
    {"text": "Звонок: «Вам перевод от бабушки, но нужна комиссия. Скажите код из СМС»\n\nЧто делать?", "options": ["✅ Скажу", "🚫 Положу трубку"], "correct": 1, "explanation": "Клади трубку! Это развод."},
    {"text": "Звонок: «Ваш аккаунт в Telegram взламывают! Срочно перейдите по ссылке из СМС»\n\nПерейдёшь?", "options": ["✅ Да", "🚫 Нет"], "correct": 1, "explanation": "Нет! Ссылка может украсть аккаунт."},
    {"text": "Звонок: «Служба безопасности Wildberries. Ваш заказ заморожен, назовите данные карты»\n\nЭто мошенники?", "options": ["✅ Да", "🚫 Нет"], "correct": 0, "explanation": "Да! WB не звонит."},
]

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

# =============== РАБОТА С ДАННЫМИ (С ПЕРЕМЕШИВАНИЕМ) ===============
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
    user_data = init_user_data()  # при сбросе — новый случайный порядок
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

# =============== СКАМ-ДЕТЕКТОР ===============
def scam_detector(text):
    text_lower = text.lower()
    scam_words = ["код из смс", "заблокирована", "выигрыш", "срочно", "переведите", "данные карты", "cvv"]
    found = [w for w in scam_words if w in text_lower]
    has_link = "http" in text_lower or "bit.ly" in text_lower or "clck.ru" in text_lower
    
    if found or has_link:
        return ("⚠️ ПОДОЗРИТЕЛЬНО\n\n"
                "Найдены признаки мошенничества.\n"
                "Не переходите по ссылкам и не сообщайте личные данные!")
    else:
        return ("✅ ПРЕДВАРИТЕЛЬНО БЕЗОПАСНО\n\n"
                "Явных признаков мошенничества не обнаружено.\n"
                "Но всегда будьте внимательны!")

# =============== ОБРАБОТЧИКИ ===============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🛡️ Добро пожаловать в Cyber Shield, {user.first_name}!\n\n"
        "Этот бот научит вас защищаться от кибермошенников.\n"
        "100 уровней: домены, письма, звонки.\n"
        "Вопросы для каждого пользователя перемешиваются случайным образом!\n"
        "Выберите действие в меню ниже:",
        reply_markup=main_menu(),
        disable_web_page_preview=True
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Справка по командам\n\n"
        "/start — запустить бота\n"
        "/help — показать эту справку\n"
        "/reset — сбросить прогресс и перемешать вопросы заново\n\n"
        "Отправьте мне подозрительное сообщение или ссылку — я проанализирую.",
        disable_web_page_preview=True
    )

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    reset_progress(user_id)
    await update.message.reply_text(
        "✅ Прогресс сброшен. Вопросы перемешаны заново!",
        disable_web_page_preview=True
    )

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
        text = (
            f"📊 Ваша статистика:\n\n"
            f"🛡️ Всего пройдено: {total} уровней\n"
            f"   🖥 Домены: {dom_pos} / {LEVELS_TOTAL['domains']}\n"
            f"   📧 Письма: {msg_pos} / {LEVELS_TOTAL['messages']}\n"
            f"   📞 Звонки: {call_pos} / {LEVELS_TOTAL['calls']}\n\n"
            f"Так держать!"
        )
        await safe_edit(query, text, reply_markup=main_menu())
        return

    if data == "about":
        text = (
            "ℹ️ О проекте\n\n"
            "Автор: MrBulbaOO1 (12 лет, Брест)\n"
            "Бот создан для конкурса «#КиберПраво: твой щит в сети».\n\n"
            "Контакты: a.carantine@gmail.com\n"
            "Ссылка на бота: @MrBulbaOO1"
        )
        await safe_edit(query, text, reply_markup=main_menu())
        return

    if data.startswith("cat_"):
        category = data.replace("cat_", "")
        user_data = get_user_data(user_id)
        pos = user_data[category]["pos"]
        if pos >= LEVELS_TOTAL[category]:
            await safe_edit(query, "🎉 Вы уже прошли все задания в этой категории!", reply_markup=main_menu())
            return
        q_index = user_data[category]["order"][pos]
        question = QUESTIONS[category][q_index]
        await safe_edit(
            query,
            f"🔍 Уровень {pos+1} в категории «{category}»:\n\n{question['text']}",
            reply_markup=answer_keyboard(category, pos, question['options'])
        )
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
            await safe_edit(query, "⏳ Это задание уже неактуально. Начните новое!", reply_markup=main_menu())
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
            [InlineKeyboardButton("▶️ Следующее задание", callback_data=f"cat_{category}")],
            [InlineKeyboardButton("⬅️ В меню", callback_data="back_to_main")]
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
            [InlineKeyboardButton("⬅️ В меню", callback_data="back_to_main")]
        ]
        await safe_edit(
            query,
            f"🎲 Случайное задание:\n\n{question['text']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
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
    print("Cyber Shield Bot v9.0")
    print("Автор: MrBulbaOO1, 12 лет, Брест")
    print("Конкурс: #КиберПраво")
    print("="*50 + "\n")
    
    try:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("reset", reset_command))
        app.add_handler(CallbackQueryHandler(button_click))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
        
        logger.info("Бот успешно запущен!")
        print("✅ Бот работает! Нажмите Ctrl+C для остановки.\n")
        
        app.run_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}")
        print(f"\n❌ Ошибка: {e}\n")
        print("Проверьте:")
        print("1. Правильно ли настроен токен в переменных окружения?")
        print("2. Есть ли интернет?")
        print("3. Установлена ли библиотека? pip install python-telegram-bot")

if __name__ == "__main__":
    main()