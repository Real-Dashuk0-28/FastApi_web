import unittest
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def total(a: int, b: int) -> int:
    """Простая функция для демонстрации тестирования"""
    return a + b


class TotalTestCase(unittest.TestCase):
    """Тесты для функции total"""

    def test_total_positive_numbers(self):
        """Проверка сложения положительных чисел"""
        a = 5
        b = 3
        expected = 8

        result = total(a, b)

        self.assertEqual(expected, result, f"Ошибка: {a} + {b} должно быть {expected}")

    def test_total_negative_numbers(self):
        """Проверка сложения отрицательных чисел"""
        a = -5
        b = -3
        expected = -8

        result = total(a, b)

        self.assertEqual(expected, result)

    def test_total_mixed_numbers(self):
        """Проверка сложения положительного и отрицательного"""
        test_cases = [
            (5, -3, 2),
            (-5, 3, -2),
            (0, 0, 0),
            (10, -10, 0),
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b):
                result = total(a, b)
                self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()