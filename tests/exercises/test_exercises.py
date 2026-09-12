from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesQuerySchema
from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import GetExercisesResponseSchema
from fixtures.courses import CourseFixture, function_course
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercises_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(self,
                             exercises_client: ExercisesClient,
                             function_course: CourseFixture
                             ):
        request_exercise = CreateExerciseRequestSchema(
            courseId=function_course.response.course.id
        )
        response_exercise = exercises_client.create_exercise_api(request_exercise)

        response_data = CreateExerciseResponseSchema.model_validate_json(response_exercise.text)

        assert_status_code(response_exercise.status_code, HTTPStatus.OK)

        assert_create_exercises_response(request_exercise, response_data)

        validate_json_schema(response_exercise.json(), response_data.model_json_schema())


    def test_get_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):

        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)

        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_get_exercise_response(response_data, function_exercise.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_update_exercise(self,exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        request_exercise = UpdateExerciseRequestSchema()
        response = exercises_client.update_exercise_api(function_exercise.response.exercise.id,request_exercise)

        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_update_exercise_response(request_exercise, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        response=exercises_client.delete_exercise_api(function_exercise.response.exercise.id)
        assert_status_code(response.status_code, HTTPStatus.OK)
        response_get_exercise = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(response_get_exercise .text)
        # 4. Проверяем, что сервер вернул 404 Not Found
        assert_status_code(response_get_exercise.status_code, HTTPStatus.NOT_FOUND)
        # 5. Проверяем, что в ответе содержится ошибка "File not found"
        assert_exercise_not_found_response(get_response_data)

        # 6. Проверяем, что ответ соответствует схеме
        validate_json_schema(response_get_exercise.json(), get_response_data.model_json_schema())


    def test_get_exercises(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture, function_course: CourseFixture):
            query = GetExercisesQuerySchema(courseId=function_course.response.course.id)

            response = exercises_client.get_exercises_api(query)
            response_data = GetExercisesResponseSchema.model_validate_json(response.text)

            # Проверяем, что код ответа 200 OK
            assert_status_code(response.status_code, HTTPStatus.OK)
            # Проверяем, что список задания соответствует ранее созданным заданием
            assert_get_exercises_response(response_data, [function_exercise.response])

