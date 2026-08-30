import random

import pytest

PLATFORM = "Linux"


@pytest.mark.flaky(reruns=3, reruns_delay=2)  # Перезапуски реализуются на уровне маркировки flaky
def test_reruns():
    assert random.choice([True, False])  # Случайный выбор для демонстрации нестабильного теста


@pytest.mark.flaky(reruns=3, reruns_delay=2)
class TestCreateUser:
    def test_test(self):
        assert random.choice([True, False])

    def test_tewst(self):
        assert random.choice([True, False])


# При условии отправляется
@pytest.mark.flaky(reruns=3, reruns_delay=2, condition=PLATFORM == "WINDOWS")
def test_rerunsw():
    assert random.choice([True, False])


#@pytest.mark.flaky(reruns = 5, reruns_delay = 3)
