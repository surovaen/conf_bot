import enum


class Callback(enum.Enum):
    """Перечисление колбеков."""

    NONE = 'NONE'
    CONFERENCE = 'conference'
    CONFERENCE_PRERECORD = 'conference_prerecord'
    CONFERENCE_TICKET = 'conference_ticket'
    CONFERENCE_TICKET_UUID = 'conference_ticket_{uuid}_{type}'
    CONFERENCE_PAYMENT = 'conference_payment'
    CONFERENCE_PAYMENT_UUID = 'conference_payment_{uuid}'
    COURSE = 'course'
    COURSE_PRERECORD = 'course_prerecord'
    BREAKFAST = 'breakfast'
    BREAKFAST_DETAILS = 'breakfast_details'
    BREAKFAST_DETAILS_UUID = 'breakfast_details_{uuid}'
    BREAKFAST_PAYMENT = 'breakfast_payment'
    BREAKFAST_PAYMENT_UUID = 'breakfast_payment_{uuid}'
    GAME = 'game'
    GAME_PAYMENT = 'game_payment'
    GAME_PAYMENT_UUID = 'game_payment_{uuid}'
    PERSONAL_WORK = 'personal_work'
    PODCAST = 'podcast'
    GIFT = 'gift'
    MENU_BREAKFAST = 'menu_{uuid}_{pk}'
    MENU = 'menu'
    FEEDBACK = 'feedback'
    FEEDBACK_UUID = 'feedback_{uuid}'
    PROMO = 'promo'
