import unittest
import os
import pandas as pd
import storage
from models import FinancialOperation

class TestFinanceIntegration(unittest.TestCase):

    def setUp(self):
        #Подготовка: создаем временный путь для тестовой БД
        self.original_path = storage.FILE_PATH
        storage.FILE_PATH = 'data/test_temp_2026.csv'
        storage.initialize_storage()

    def tearDown(self):
        #Очистка: удаляем временный файл и возвращаем путь назад
        if os.path.exists(storage.FILE_PATH):
            os.remove(storage.FILE_PATH)
        storage.FILE_PATH = self.original_path


    # 1) Тестирование работы классов (models.py)
    def test_class_to_list_conversion(self):
        #Проверка, что класс корректно готовит данные для сохранения
        op = FinancialOperation("5000", "Еда", "08.01.2026", "Обед", "Расход")
        expected_data = ["08.01.2026", "Расход", "Еда", 5000.0, "Обед"]
        self.assertEqual(op.to_list(), expected_data)

    # 2) Тестирование функций анализа и сохранения (реальная работа с файлом)
    def test_save_and_load_balance(self):
        #Реальный тест: запись в файл и расчет баланса из него
        # Создаем тестовый набор данных
        df = pd.DataFrame([
            ['01.01.2026', 'Доход', 'Зарплата', 1000.0, 'Бонус'],
            ['02.01.2026', 'Расход', 'Еда', 300.0, 'Магазин']
        ], columns=storage.HEADERS)
        #Сохраняем в файл
        storage.save_dataframe(df)
        # Загружаем заново и считаем баланс
        loaded_df = storage.load_all_data()
        balance = storage.calculate_balance(loaded_df)
        self.assertEqual(balance, 700.0)  # 1000 - 300
        self.assertEqual(len(loaded_df), 2)

    def test_filtering_logic_real(self):
        #Тест фильтрации данных, считанных с диска
        df = pd.DataFrame([
            ['01.01.2026', 'Расход', 'Транспорт', 100.0, 'Автобус'],
            ['01.01.2026', 'Расход', 'Еда', 200.0, 'Перекус']
        ], columns=storage.HEADERS)
        storage.save_dataframe(df)
        #Вызываем функцию фильтрации
        filtered = storage.load_filtered_data(category_filter='Транспорт')
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]['Категория'], 'Транспорт')
        self.assertEqual(filtered.iloc[0]['Сумма'], 100.0)

if __name__ == '__main__':
    unittest.main()

