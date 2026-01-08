import matplotlib.pyplot as plt
import seaborn as sns
from storage import load_all_data

def plot_time_trend():
    # Загружаем все данные из нашего CSV-файла
    df = load_all_data()
    # Если данных еще нет, ничего не рисуем и выходим
    if df.empty: return
    # Складываем суммы, группируя их по датам и типу (доход/расход), и рисуем график с точками
    df.groupby(['Дата', 'Тип'])['Сумма'].sum().unstack().fillna(0).plot(marker='o')
    # Добавляем заголовок графика
    plt.title("Динамика финансов 2026")
    # Включаем сетку для удобства чтения
    plt.grid(True)
    # Показываем готовое окно с графиком
    plt.show()

def plot_category_pie():
    # Загружаем данные из файла
    df = load_all_data()
    # Оставляем только те строки, где тип операции — 'Расход'
    expenses = df[df['Тип'] == 'Расход']
    # Если расходов нет, выходим
    if expenses.empty: return
    # Считаем сумму для каждой категории и рисуем круговую диаграмму с процентами
    expenses.groupby('Категория')['Сумма'].sum().plot(kind='pie', autopct='%1.1f%%')
    # Добавляем заголовок
    plt.title("Расходы по категориям 2026")
    # Убираем лишнюю подпись сбоку
    plt.ylabel("")
    # Показываем график
    plt.show()

def plot_top_expenses_bar():
    # Загружаем данные
    df = load_all_data()
    # Берем только расходы
    expenses = df[df['Тип'] == 'Расход']
    # Если записей нет, выходим
    if expenses.empty: return
    # Группируем по категориям, считаем суммы, сортируем от больших к меньшим и берем первые 10
    top = expenses.groupby('Категория')['Сумма'].sum().sort_values(ascending=False).head(10)
    # Создаем область для графика определенного размера
    plt.figure(figsize=(10, 6))
    # Рисуем горизонтальные цветные полоски (чем длиннее полоска, тем больше трата)
    sns.barplot(x=top.values, y=top.index, hue=top.index, palette="viridis", legend=False)
    # Добавляем заголовок
    plt.title("ТОП-10 расходов 2026")
    # Показываем результат
    plt.show()
