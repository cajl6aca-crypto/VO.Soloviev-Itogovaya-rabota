import unittest
import pandas as pd
from models import FinancialOperation
import storage
import analysis


class TestFinanceManager(unittest.TestCase):

    # --- ТЕСТЫ КЛАССОВ (models.py) ---
    def test_operation_creation(self):
        """Проверка корректности создания объекта операции."""
        op = FinancialOperation(
            amount="1500.50",
            category="Еда",
            date_str="07.01.2026",
            comment="Ужин",
            op_type="Расход"
        )
        self.assertEqual(op.amount, 1500.50)
        self.assertEqual(op.category, "Еда")
        self.assertEqual(op.to_list(), ["07.01.2026", "Расход", "Еда", 1500.50, "Ужин"])

    def test_invalid_date_format(self):
        """Проверка, что класс выдает ошибку при неверном формате даты."""
        with self.assertRaises(ValueError):
            FinancialOperation("100", "Тест", "2026-01-07", "Ошибка", "Доход")

    # --- ТЕСТЫ АНАЛИЗА ДАННЫХ (storage.py / analysis.py) ---
    def test_balance_calculation(self):
        """Проверка логики расчета баланса."""
        # Создаем тестовый DataFrame
        data = {
            'Дата': pd.to_datetime(['01.01.2026', '02.01.2026']),
            'Тип': ['Доход', 'Расход'],
            'Категория': ['Зарплата', 'Еда'],
            'Сумма': [50000.0, 10000.0],
            'Комментарий': ['Бонус', 'Магазин']
        }
        df = pd.DataFrame(data)

        balance = storage.calculate_balance(df)
        self.assertEqual(balance, 40000.0)

    def test_filter_logic(self):
        """Проверка, что фильтрация возвращает только нужные категории."""
        data = {
            'Дата': pd.to_datetime(['01.01.2026', '02.01.2026']),
            'Тип': ['Расход', 'Расход'],
            'Категория': ['Еда', 'Транспорт'],
            'Сумма': [500, 200],
            'Комментарий': ['-', '-']
        }
        df = pd.DataFrame(data)

        # Имитируем фильтрацию (логика из load_filtered_data)
        filtered_df = df[df['Категория'] == 'Еда']
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df.iloc[0]['Категория'], 'Еда')


if __name__ == '__main__':
    unittest.main()
