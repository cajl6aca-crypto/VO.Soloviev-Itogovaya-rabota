import tkinter as tk
from tkinter import ttk, messagebox
import storage, utils, analysis
from datetime import datetime


class FinanceApp:
    #Класс графического интерфейса приложения Финансовый Менеджер 2026
    def __init__(self, root):
        self.root = root
        self.root.title("Финансовый Менеджер 2026")
        self.root.geometry("1050x800")
        self.selected_idx = None  # Хранит ID редактируемой строки
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        #Настройка элементов интерфейса с выравниванием по столбцам
        # 1) Поля ввода данных
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill="x", padx=10, pady=10)

        # Конфигурация колонок (уменьшено на ~10% от предыдущих значений)
        input_frame.grid_columnconfigure(0, minsize=50)  # ID (без изменений)
        input_frame.grid_columnconfigure(1, weight=1, minsize=100)  # Дата (без изменений)
        input_frame.grid_columnconfigure(2, weight=1, minsize=90)  # Тип (-10%)
        input_frame.grid_columnconfigure(3, weight=1, minsize=108)  # Категория (-10%)
        input_frame.grid_columnconfigure(4, weight=1, minsize=90)  # Сумма (-10%)
        input_frame.grid_columnconfigure(5, weight=2, minsize=225)  # Комментарий (-10%)

        #Метка над ID
        ttk.Label(input_frame, text="ID").grid(row=0, column=0, padx=5, sticky="w")

        #Список полей: (Текст метки, Имя переменной, Номер колонки)
        fields = [
            ("Дата", "ent_date", 1),
            ("Тип", "cb_type", 2),
            ("Категория", "ent_cat", 3),
            ("Сумма", "ent_sum", 4),
            ("Комментарий", "ent_comm", 5)
        ]

        for label_text, entry_name, col_idx in fields:
            ttk.Label(input_frame, text=label_text).grid(row=0, column=col_idx, padx=5, sticky="w")
            if entry_name == "cb_type":
                self.__dict__[entry_name] = ttk.Combobox(input_frame, values=["Доход", "Расход"], state="readonly")
                self.__dict__[entry_name].current(1)
            else:
                self.__dict__[entry_name] = ttk.Entry(input_frame)

            self.__dict__[entry_name].grid(row=1, column=col_idx, padx=5, pady=5, sticky="we")

        #Установка текущей даты
        self.ent_date.insert(0, datetime.now().strftime("%d.%m.%Y"))

        # 2) Кнопки действий
        btn_action_frame = ttk.Frame(self.root)
        btn_action_frame.pack(fill="x", padx=10, pady=5)

        self.btn_save = ttk.Button(btn_action_frame, text="Сохранить запись", command=self.handle_save)
        self.btn_save.pack(side="left", padx=5)

        ttk.Button(btn_action_frame, text="Очистить / Сброс", command=self.clear_fields).pack(side="left", padx=5)
        ttk.Button(btn_action_frame, text="Удалить запись", command=self.handle_delete).pack(side="right", padx=5)

        # 3) Таблица (Treeview)
        table_frame = ttk.LabelFrame(self.root, text="Список операций (Кликните на строку для редактирования)")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "D", "T", "C", "S", "Co"), show='headings')
        cols_map = {"ID": "ID", "D": "Дата", "T": "Тип", "C": "Категория", "S": "Сумма", "Co": "Комментарий"}

        for cid, head in cols_map.items():
            self.tree.heading(cid, text=head)

        #Настройка ширины колонок таблицы (синхронизировано с minsize выше)
        self.tree.column("ID", width=50, stretch=tk.NO)
        self.tree.column("D", width=100)
        self.tree.column("T", width=90)
        self.tree.column("C", width=108)
        self.tree.column("S", width=90)
        self.tree.column("Co", width=225)

        self.tree.pack(fill="both", expand=True, side="left")
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # 4) Аналитика
        graph_frame = ttk.Frame(self.root)
        graph_frame.pack(fill="x", padx=10, pady=10)
        ttk.Button(graph_frame, text="Динамика", command=analysis.plot_time_trend).pack(side="left", padx=10)
        ttk.Button(graph_frame, text="Категории", command=analysis.plot_category_pie).pack(side="left", padx=10)
        ttk.Button(graph_frame, text="ТОП трат", command=analysis.plot_top_expenses_bar).pack(side="left", padx=10)

        # 5) Фильтрация и Баланс
        filter_frame = ttk.LabelFrame(self.root, text="Итоги 2026")
        filter_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(filter_frame, text="Фильтр:").pack(side="left", padx=5)
        self.cb_filter_cat = ttk.Combobox(filter_frame, values=["Все категории"], state="readonly")
        self.cb_filter_cat.current(0)
        self.cb_filter_cat.pack(side="left", padx=5)
        self.cb_filter_cat.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        self.lbl_balance = ttk.Label(filter_frame, text="Баланс: 0.00", font=("Arial", 12, "bold"))
        self.lbl_balance.pack(side="right", padx=15)

    def refresh_table(self):
        #Загрузка данных в таблицу и расчет баланса
        for i in self.tree.get_children():
            self.tree.delete(i)

        cat_filter = self.cb_filter_cat.get()
        df = storage.load_all_data() if cat_filter == "Все категории" else storage.load_filtered_data(
            category_filter=cat_filter)

        for idx, r in df.iterrows():
            self.tree.insert("", "end",
                             values=(idx, r['Дата'].strftime("%d.%m.%Y"), r['Тип'], r['Категория'], r['Сумма'],
                                     r['Комментарий']))

        all_data = storage.load_all_data()
        self.cb_filter_cat['values'] = ["Все категории"] + sorted(all_data['Категория'].unique().tolist())

        balance = storage.calculate_balance(df)
        self.lbl_balance.config(text=f"Итог по выборке: {balance:,.2f}", foreground="green" if balance >= 0 else "red")

    def on_select(self, event):
        #Перенос данных из таблицы в поля ввода
        selected = self.tree.selection()
        if not selected: return
        vals = self.tree.item(selected)['values']
        if not vals: return

        self.selected_idx = vals[0]

        self.ent_date.delete(0, tk.END);
        self.ent_date.insert(0, vals[1])
        self.cb_type.set(vals[2])
        self.ent_cat.delete(0, tk.END);
        self.ent_cat.insert(0, vals[3])
        self.ent_sum.delete(0, tk.END);
        self.ent_sum.insert(0, vals[4])
        self.ent_comm.delete(0, tk.END);
        self.ent_comm.insert(0, vals[5])

        self.btn_save.config(text="Сохранить изменения")

    def handle_save(self):
        #Сохранение новой или обновленной записи
        d, t, c, s, comm = self.ent_date.get(), self.cb_type.get(), self.ent_cat.get(), self.ent_sum.get(), self.ent_comm.get()

        if not utils.validate_date_format(d): return messagebox.showerror("Ошибка", "Дата должна быть дд.мм.2026")
        if not utils.validate_amount(s): return messagebox.showerror("Ошибка", "Введите число (сумма)")
        if not all([utils.validate_not_empty(x) for x in [c, comm]]): return messagebox.showerror("Ошибка",
                                                                                                  "Заполните поля")

        df = storage.load_all_data()
        new_row = [d, t, c, float(s), comm]

        if self.selected_idx is not None:
            df.loc[int(self.selected_idx)] = new_row
            messagebox.showinfo("Успех", "Запись обновлена")
        else:
            df.loc[len(df)] = new_row
            messagebox.showinfo("Успех", "Запись добавлена")

        storage.save_dataframe(df)
        self.refresh_table()
        self.clear_fields()

    def handle_delete(self):
        #Удаление записи
        if self.selected_idx is None: return messagebox.showerror("Ошибка", "Выберите запись")
        if not messagebox.askyesno("Удаление", "Удалить выбранную операцию?"): return

        df = storage.load_all_data()
        df = df.drop(index=int(self.selected_idx))
        storage.save_dataframe(df)
        self.refresh_table()
        self.clear_fields()

    def clear_fields(self):
        #Сброс формы
        self.selected_idx = None
        self.ent_date.delete(0, tk.END);
        self.ent_date.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.ent_cat.delete(0, tk.END);
        self.ent_cat.insert(0, '')
        self.ent_sum.delete(0, tk.END);
        self.ent_sum.insert(0, '')
        self.ent_comm.delete(0, tk.END);
        self.ent_comm.insert(0, '')
        self.btn_save.config(text="Сохранить запись")
