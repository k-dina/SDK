import unittest
from SDK.models.auth import Token  # замените 'your_module' на имя вашего модуля, где находится класс Token


class TestToken(unittest.TestCase):

    def test_token_attributes(self):
        # Создаем тестовые данные
        res = {
            "access_token": {
                "access_token": "test_access_token",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }

        # Создаем экземпляр объекта Token
        token = Token(res)

        # Проверяем, что атрибуты установлены правильно
        self.assertEqual(token.access_token, 'test_access_token')
        self.assertEqual(token.type, 'bearer')
        self.assertEqual(token.expires_in, 3600)

    def test_my(self):
        res = None
        with self.assertRaises(ValueError):
            Token(res)


if __name__ == '__main__':
    unittest.main()
