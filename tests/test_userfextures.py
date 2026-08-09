import pytest

@pytest.fixture
def clear_books_database():
    print("[FIXTURE] Удаляем все данные из базы данных")


@pytest.fixture
def file_books_database():
    print("[FIXTURE] Создаем новые данные в базе данных")


@pytest.mark.usefixtures(file_books_database,clear_books_database)
class TestLibrary:
    def test_read_book_from_library(self):
        ...

    def test_delete_book_from_library(self):
        ...