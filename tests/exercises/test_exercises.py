from http import HTTPStatus

import allure
import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesQuerySchema
from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import GetExercisesResponseSchema
from fixtures.courses import CourseFixture, function_course
from fixtures.exercises import ExerciseFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeatures
from tools.allure.parent_suite import AllureParentSuite
from tools.allure.sub_suite import AllureSubSuite
from tools.allure.suite import AllureSuite
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercises_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.exercises
@pytest.mark.regression
@allure.tag(AllureTag.EXERCISES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeatures.EXERCISES)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.EXERCISES)
class TestExercises:
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Create exercise")
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

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @allure.title("Get exercise")
    def test_get_exercise(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture):

        response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)

        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_get_exercise_response(response_data, function_exercise.response)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.UPDATE_ENTITY)
    @allure.title("Update exercise")
    def test_update_exercise(self,exercises_client: ExercisesClient, function_exercise: ExerciseFixture):
        request_exercise = UpdateExerciseRequestSchema()
        response = exercises_client.update_exercise_api(function_exercise.response.exercise.id,request_exercise)

        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_update_exercise_response(request_exercise, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.sub_suite(AllureSubSuite.DELETE_ENTITY)
    @allure.title("Delete exercise")
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

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.sub_suite(AllureSubSuite.GET_ENTITIES)
    @allure.title("Get exercises")
    def test_get_exercises(self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture, function_course: CourseFixture):
            query = GetExercisesQuerySchema(courseId=function_course.response.course.id)

            response = exercises_client.get_exercises_api(query)
            response_data = GetExercisesResponseSchema.model_validate_json(response.text)

            # Проверяем, что код ответа 200 OK
            assert_status_code(response.status_code, HTTPStatus.OK)
            # Проверяем, что список задания соответствует ранее созданным заданием
            assert_get_exercises_response(response_data, [function_exercise.response])

