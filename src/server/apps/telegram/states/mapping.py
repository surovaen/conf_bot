from server.apps.telegram.states.enums import StateType
from server.apps.telegram.states.strategies import (
    ConferenceQuestionsStrategy,
    CourseQuestionsStrategy,
    UserInfoStrategy,
)


STATE_TYPE_MAPPING = {
    StateType.USER_INFO.value: UserInfoStrategy,
    StateType.CONF_QUESTIONS.value: ConferenceQuestionsStrategy,
    StateType.COURSE_QUESTIONS.value: CourseQuestionsStrategy,
}
