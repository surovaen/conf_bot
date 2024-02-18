from server.apps.telegram.states.enums import StateType
from server.apps.telegram.states.strategies import (
    CourseQuestionsStrategy,
    UserInfoStrategy,
)


STATE_TYPE_MAPPING = {
    StateType.USER_INFO.value: UserInfoStrategy,
    StateType.COURSE_QUESTIONS.value: CourseQuestionsStrategy,
}
