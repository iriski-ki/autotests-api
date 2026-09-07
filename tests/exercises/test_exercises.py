from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from fixtures.courses import CourseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercises_response
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