import unittest
from client_management import add_client, add_phone, update_client, delete_phone, delete_client, find_client, check_data
from create_db import create_db

class TestClientManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Создает структуру базы данных перед запуском тестов.
        """
        create_db()
        print("Создание структуры базы данных успешно.")

    def setUp(self):
        """
        Устанавливает необходимые данные перед каждым тестом.
        """
        self.client_id = add_client("Тест", "Клиент", "test@mail.ru")
        self.phone_number_1 = "1234567890"
        self.phone_number_2 = "0987654321"
        add_phone(self.client_id, self.phone_number_1)
        print("Начальные данные установлены успешно.")

    def tearDown(self):
        """
        Удаляет тестовые данные после каждого теста.
        """
        delete_phone(self.client_id, self.phone_number_1)
        delete_phone(self.client_id, self.phone_number_2)
        delete_client(self.client_id)
        print("Тестовые данные удалены успешно.")

    def test_add_client(self):
        """
        Тестирует добавление нового клиента.
        """
        new_client_id = add_client("Иван", "Иванов", "ivanov@mail.ru")
        self.assertIsNotNone(new_client_id)
        delete_client(new_client_id)
        print("Тест test_add_client успешно пройден.")

    def test_add_phone(self):
        """
        Тестирует добавление нового номера телефона для клиента.
        """
        add_phone(self.client_id, self.phone_number_2)
        result = find_client(phone_number=self.phone_number_2)
        self.assertTrue(any(phone_number == self.phone_number_2 for _, _, _, _, phone_number in result))
        print("Тест test_add_phone успешно пройден.")

    def test_update_client(self):
        """
        Тестирует обновление данных клиента.
        """
        new_email = "new_test@mail.ru"
        update_client(self.client_id, email=new_email)
        result = find_client(email=new_email)
        self.assertTrue(any(email == new_email for _, _, _, email, _ in result))
        print("Тест test_update_client успешно пройден.")

    def test_delete_phone(self):
        """
        Тестирует удаление номера телефона клиента.
        """
        add_phone(self.client_id, self.phone_number_2)
        delete_phone(self.client_id, self.phone_number_2)
        result = find_client(phone_number=self.phone_number_2)
        self.assertFalse(any(phone_number == self.phone_number_2 for _, _, _, _, phone_number in result))
        print("Тест test_delete_phone успешно пройден.")

    def test_delete_client(self):
        """
        Тестирует удаление клиента.
        """
        new_client_id = add_client("Иван", "Петров", "ivan.petrov@mail.ru")
        add_phone(new_client_id, "1111111111")
        delete_client(new_client_id)
        result = find_client(email="ivan.petrov@mail.ru")
        self.assertFalse(any(client_id == new_client_id for client_id, _, _, _, _ in result))
        print("Тест test_delete_client успешно пройден.")

    def test_find_client(self):
        """
        Тестирует поиск клиента по различным параметрам.
        """
        result = find_client(first_name="Тест")
        self.assertTrue(any(first_name == "Тест" for _, first_name, _, _, _ in result))
        result = find_client(last_name="Клиент")
        self.assertTrue(any(last_name == "Клиент" for _, _, last_name, _, _ in result))
        result = find_client(email="test@mail.ru")
        self.assertTrue(any(email == "test@mail.ru" for _, _, _, email, _ in result))
        result = find_client(phone_number=self.phone_number_1)
        self.assertTrue(any(phone_number == self.phone_number_1 for _, _, _, _, phone_number in result))
        print("Тест test_find_client успешно пройден.")

    @classmethod
    def tearDownClass(cls):
        """
        Выводит обобщающий отчет после завершения всех тестов.
        """
        print("Все тесты успешно пройдены.")

if __name__ == "__main__":
    unittest.main()
