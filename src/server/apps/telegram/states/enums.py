import enum


class StateType(enum.Enum):
    """Перечисление типов состояний."""

    USER_INFO = 'USER_INFO'
    CONF_QUESTIONS = 'CONF_QUESTIONS'
    COURSE_QUESTIONS = 'COURSE_QUESTIONS'
    FEEDBACK = 'FEEDBACK'
    PROMO = 'PROMO'


class StageType(enum.Enum):
    """Перечисление сценариев."""

    START = 'START'
    CONF_QUESTIONS = 'CONF_QUESTIONS'
    COURSE_QUESTIONS = 'COURSE_QUESTIONS'
    BREAKFAST = 'BREAKFAST'
    GAME = 'GAME'
    PERSONAL_WORK = 'PERSONAL_WORK'


class MessageContentTypeEnum(enum.Enum):
    """Перечисление типов сообщений."""

    TEXT = 'text'
    CONTACT = 'contact'
