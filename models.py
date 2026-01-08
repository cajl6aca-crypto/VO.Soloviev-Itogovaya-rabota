from datetime import datetime

class FinancialOperation:
    #Класс, описывающий одну финансовую операцию
    def __init__(self, amount, category, date_str, comment, op_type):
        self.amount = float(amount)
        self.category = category
        # Валидация даты при создании объекта
        self.date = datetime.strptime(date_str, "%d.%m.%Y")
        self.comment = comment
        self.op_type = op_type # 'Доход' или 'Расход'

    def to_list(self):
        #Преобразование объекта в список для записи в CSV
        return [self.date.strftime("%d.%m.%Y"), self.op_type, self.category, self.amount, self.comment]
