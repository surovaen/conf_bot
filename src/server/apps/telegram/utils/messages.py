from telebot import formatting


START_TEXT = """Привет! На связи помощник Анастасии Гелеверовой

Здесь вы можете первыми узнать:
• о всех предстоящих мероприятиях
• записаться на коуч-завтраки
• посмотреть анонсы игр
• узнать о ближайших курсах
• попасть в листы предзаписи.

Давайте познакомимся!"""

WELCOME_TEXT = '{name}, Бот-Богач к Вашим услугам!'
MENU_TEXT = f"""Что хотите посмотреть сначала?\n
{formatting.hitalic('В любой момент Вы можете вернуться сюда, нажав на кнопку МЕНЮ')}"""
START_MENU_TEXT = ("""{name}, Бот-Богач к Вашим услугам!\n
Что хотите посмотреть сначала?\n\n""" +
                   f"""{formatting.hitalic('В любой момент Вы можете вернуться сюда, нажав на кнопку МЕНЮ')}""")

FIRST_NAME = 'Напишите свое имя:'
LAST_NAME = 'Напишите свою фамилию:'
PHONE_NUMBER = 'Укажите свой номер телефона:'
ERROR_PHONE = 'Неверно указан номер телефона. Попробуйте еще раз:'
INSTAGRAM = 'Укажите свой инстаграм через @'

USER_INFO_PRERECORDING_TEXT = 'Для предзаписи необходимо указать Ваши данные: имя, фамилию и номер телефона.'
USER_INFO_PAYMENT_TEXT = 'Для оплаты необходимо указать Ваши данные: имя, фамилию и номер телефона.'
USER_INFO_PERSONAL_WORK_TEXT = 'Для запроса необходимо указать Ваши данные: имя, фамилию и номер телефона.'

PERSONAL_WORK_TEXT = 'Отправить запрос "Хочу в личную работу"?'
CONTINUE_PRERECORD = 'Продолжить предзапись?'
RECORDING_TEXT = 'Спасибо, всё записали!'
PRERECORDING_TEXT = 'Пожалуйста, ответьте на несколько вопросов для листа предзаписи:'
AFTER_COURSE_RECORDING_TEXT = 'Спасибо, всё записали! С Вами свяжется ассистент Анастасии'
COURSE_RECORDING_TEXT = 'Мы приняли Вашу заявку на курс. С Вами свяжется ассистент Анастасии'
NOT_INFO_TEXT = 'Информации по данному разделу пока нет'
CONFERENCE_PAID_TEXT = 'Для участия в конференции необходимо внести оплату'
PROMO_TEXT = 'Введите промокод:'
PROMO_ERROR_TEXT = 'Промокод "{promo}" не найден'
PROMO_SUCCESS_TEXT = 'Промокод "{promo}" применен'
PAYMENT_URL_TEXT = 'Для оплаты пройдите по ссылке:'
EXCEED_LIMIT_TEXT = 'К сожалению, все места уже заняты'
FEEDBACK_TEXT = 'Благодарим за обратную связь!'
NOT_PRERECORDING_TEXT = 'Извините, предзапись пока не открыта'
NOT_GIFTS = 'Подарков пока нет, приходите позже'
BREAKFAST_CONFIRMATION_TEXT = 'Отличный выбор! Ждем Вас завтра по адресу: {place}. До встречи!'
ERROR_BOT_TEXT = 'К сожалению, возникла ошибка обработки Вашего запроса. Попробуйте позже'
TICKET_CATEGORY_TEXT = 'Выберите категорию билета:'
NOT_TICKET = 'К сожалению, билеты категории {type} раскуплены'

USER_INFO_MSG_MAP = {
    0: FIRST_NAME,
    1: LAST_NAME,
    2: INSTAGRAM,
    3: PHONE_NUMBER,
    4: ERROR_PHONE,
}
