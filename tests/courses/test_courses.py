from http import HTTPStatus

import allure
import pytest
from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import UpdateCourseRequestSchema, UpdateCourseResponseSchema, GetCoursesQuerySchema, \
    GetCoursesResponseSchema, CreateCourseRequestSchema, CreateCourseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.files import FileFixture
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeatures
from tools.allure.parent_suite import AllureParentSuite
from tools.allure.sub_suite import AllureSubSuite
from tools.allure.suite import AllureSuite
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.courses import assert_update_course_response, assert_get_courses_response, \
    assert_create_course_response
from tools.assertions.schema import validate_json_schema



@pytest.mark.courses
@pytest.mark.regression
@allure.tag(AllureTag.COURSES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeatures.COURSES)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.COURSES)
class TestCourses:
    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.UPDATE_ENTITY)
    @allure.title("Update course")
    def test_update_course(self, courses_client: CoursesClient, function_course: CourseFixture):
        # Формируем данные для обновления
        request = UpdateCourseRequestSchema()
        # Отправляем запрос на обновление курса
        response = courses_client.update_course_api(function_course.response.course.id, request.model_dump(by_alias=True, exclude_none=True))
        # Преобразуем JSON-ответ в объект схемы
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что данные в ответе соответствуют запросу
        assert_update_course_response(request, response_data)

        # Валидируем JSON-схему ответа
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.sub_suite(AllureSubSuite.GET_ENTITIES)
    @allure.title("Get courses")
    def test_get_courses(
            self,
            courses_client: CoursesClient,
            function_user: UserFixture,
            function_course: CourseFixture
    ):
        query = GetCoursesQuerySchema(user_id=function_user.response.user.id)

        response = courses_client.get_courses_api(query)
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)

        # Проверяем, что код ответа 200 OK
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Проверяем, что список курсов соответствует ранее созданным курсам
        assert_get_courses_response(response_data, [function_course.response])

        # Проверяем соответствие JSON-ответа схеме
        validate_json_schema(response.json(), response_data.model_json_schema())


    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Create course")
    def test_create_course(self,
                           courses_client: CoursesClient,
                           function_user: UserFixture,
                           function_file: FileFixture,

    ):
        request = CreateCourseRequestSchema(
            preview_file_id=function_file.response.file.id,
            created_by_user_id=function_user.response.user.id
        )
        response = courses_client.create_course_api(request)
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(response.json(), response_data.model_json_schema())

        assert_create_course_response(request, response_data)


