import unittest
from SDK.models import Token  # замените 'your_module' на имя вашего модуля, где находится класс Token
from pydantic import ValidationError


class TestToken(unittest.TestCase):

    def test_token_attributes(self):
        # Создаем тестовые данные
        res = {
            "access_token": "test_access_token",
            "token_type": "bearer",
            "expires_in": 3600
        }

        # Создаем экземпляр объекта Token
        token = Token.model_validate(res)

        print(token)
        # Проверяем, что атрибуты установлены правильно
        self.assertEqual(token.access_token, 'test_access_token')
        self.assertEqual(token.token_type, 'bearer')
        self.assertEqual(token.expires_in, 3600)

    def test_error(self):
        # Создаем тестовые данные
        res = {
            "access_token": "test_access_token",
        }

        with self.assertRaises(ValidationError):
            token = Token.model_validate(res)




if __name__ == '__main__':
    unittest.main()
