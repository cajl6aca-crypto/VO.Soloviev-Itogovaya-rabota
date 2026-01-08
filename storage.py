import os
import csv
import pandas as pd

#Путь к файлу базы данных на 2026 год
FILE_PATH = 'data/finance_data_2026.csv'
#Названия столбцов в таблице
HEADERS = ['Дата', 'Тип', 'Категория', 'Сумма', 'Комментарий']

def initialize_storage():
    #Создает директорию и файл, если их нет
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(HEADERS)
    print(f" База данных: {os.path.abspath(FILE_PATH)}")

def load_all_data():
    #Загружает данные в DataFrame
    try:
        df = pd.read_csv(FILE_PATH, sep=';', encoding='utf-8-sig')
        df['Дата'] = pd.to_datetime(df['Дата'], format="%d.%m.%Y", errors='coerce')
        return df.dropna(subset=['Дата'])
    except:
        return pd.DataFrame(columns=HEADERS)

def save_dataframe(df):
    #Сохраняет DataFrame обратно в CSV
    df_copy = df.copy()
    #Здесь мы адаптируем столбец дат в формат pandas и проверяем на невозможные даты
    df_copy['Дата'] = pd.to_datetime(df_copy['Дата'], format="%d.%m.%Y", errors='coerce')
    #Здесь формат меняется снова на строчки и производится подготовка к записи в формате д.м.г
    df_copy['Дата'] = df_copy['Дата'].dt.strftime("%d.%m.%Y")
    #Собственно сама запись в файл
    df_copy.to_csv(FILE_PATH, sep=';', index=False, encoding='utf-8-sig')

def load_filtered_data(category_filter=None, start_date=None, end_date=None):
    #Загружаем данные и отбираем строки по категории или периоду дат
    df = load_all_data()
    if category_filter and category_filter != 'Все категории':
        df = df[df['Категория'] == category_filter]
    #Фильтруем данные, если указана дата начала или конца периода
    if start_date:
        df = df[df['Дата'] >= pd.to_datetime(start_date, format="%d.%m.%Y")]
    if end_date:
        df = df[df['Дата'] <= pd.to_datetime(end_date, format="%d.%m.%Y")]
    return df

def calculate_balance(df=None):
    # Считаем разницу между всеми доходами и расходами
    if df is None:
        df = load_all_data()
    #Убеждаемся, что 'Сумма' имеет числовой тип
    df['Сумма'] = pd.to_numeric(df['Сумма'], errors='coerce').fillna(0)
    total_income = df[df['Тип'] == 'Доход']['Сумма'].sum()
    total_expense = df[df['Тип'] == 'Расход']['Сумма'].sum()
    balance = total_income - total_expense
    return balance