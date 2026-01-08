import tkinter as tk
import storage
import gui
import unittest

def run_tests():
    print("Запуск тестов...")
    loader = unittest.TestLoader()
    # discover ищет файлы, начинающиеся на test_*.py в текущей директории и поддиректориях
    suite = loader.discover(start_dir='.', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=1).run(suite)

if __name__ == "__main__":
    #Запуск тестов
    run_tests()

    # 1) Подготовка папок и файлов
    storage.initialize_storage()

    # 2) Запуск GUI
    root = tk.Tk()
    app = gui.FinanceApp(root)
    root.mainloop()