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