import pytest
from pydantic import BaseModel

from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from fixtures.users import UserFixture
from fixtures.courses import CourseFixture

class ExerciseFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture
def exercise_client(function_user: UserFixture) -> ExercisesClient:
    return get_exercises_client(function_user.authentication_user)


@pytest.fixture
def exercises_fixture(exercise_client:ExercisesClient ,function_course: CourseFixture) -> ExerciseFixture:
    request = CreateExerciseRequestSchema(
        courseId = function_course.response.course.id
    )
    response = exercise_client.create_exercise(request)
    return ExerciseFixture(request=request, response=response)
