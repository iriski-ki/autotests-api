from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from tools.assertions.base import assert_equal


def assert_create_exercises_response(request: CreateExerciseRequestSchema,response: CreateExerciseResponseSchema):
    """
    Проверяет, что поля созданного задания соответствуют данным из запроса на создание.

    :param request: Данные запроса на создание задания.
    :param response: Ответ API с созданным задания.
    :raises AssertionError: Если поля задания не совпадают.
    """

    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")