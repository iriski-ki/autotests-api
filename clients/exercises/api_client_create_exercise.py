from clients.course.courses_client import get_courses_client, CreateCourseRequestSchema
from clients.files.files_client import get_files_client
# Вместо CreateFileRequestDict импортируем CreateFileRequestSchema
from clients.files.file_shema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from Tools.Fakers import random_email
from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, GetExercisesQuerySchema, \
    GetExercisesResponseSchema, CreateExerciseResponseSchema, UpdateExerciseRequestSchema

public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email=random_email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string"
)
create_user_response = public_users_client.create_user(create_user_request)

authentication_user = AuthenticationUserSchema(
    email=create_user_request.email,
    password=create_user_request.password
)
files_client = get_files_client(authentication_user)
courses_client = get_courses_client(authentication_user)
exercises_client = get_exercises_client(authentication_user)

# Вместо CreateFileRequestDict используем CreateFileRequestSchema
create_file_request = CreateFileRequestSchema(
    filename="image.png",
    directory="courses",
    upload_file="./testdata/files/image.png"
)
create_file_response = files_client.create_file(create_file_request)
print('Create file data:', create_file_response)
# Вместо CreateCourseRequestDict используем CreateCourseRequestSchema
create_course_request = CreateCourseRequestSchema(
    title="Python",
    maxScore=100,
    minScore=10,
    description="Python API course",
    estimatedTime="2 weeks",
    previewFileId=create_file_response.file.id,  # Используем атрибуты место ключей
    createdByUserId=create_user_response.user.id  # Используем атрибуты место ключей
)
create_course_response = courses_client.create_course(create_course_request)
print('Create course data:', create_course_response)

# Создаем exercises
create_exercises_request = CreateExerciseRequestSchema(
    title=create_course_response.course.title,
    course_id=create_course_response.course.id,
    max_score=create_course_response.course.max_score,
    min_score=create_course_response.course.min_score,
    order_index=1,
    description = "Python API exercise",
    estimated_time = "2 weeks"
)
create_exercises_response = exercises_client.create_exercise(create_exercises_request)
print('Create exercises data:', create_exercises_response)

#Получаем exercises
get_exercises_request=GetExercisesQuerySchema(
    course_id=create_course_response.course.id
)
get_exercises_response=exercises_client.get_exercises(get_exercises_request)
print('Get exercises data:', get_exercises_response)

# Получаем задание по exercise_id
exercise_id = get_exercises_response.exercises[0].id

get_exercise_response = exercises_client.get_exercise(exercise_id)
print('Get exercise data:', get_exercise_response)

#Обновление задания по exercise_id
exercise_id = get_exercises_response.exercises[0].id

update_exercise_request = UpdateExerciseRequestSchema(
    title="Python updated",
    description="Updated description"
    # остальные поля можно не указывать — они останутся None и не попадут в запрос
)
update_exercise_response = exercises_client.update_exercise(exercise_id, update_exercise_request)
print('Update exercise data:', update_exercise_response)
