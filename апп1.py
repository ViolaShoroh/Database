import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import Button, Label, Menu, messagebox, ttk
from tkinter.messagebox import showerror, showinfo, askyesno

db_file_name = 'my_database2.db'

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('База данных')
        self.geometry('830x350')
        self.resizable(False, False)
        self.ui_init()
        self.check()
        self.mainloop()

    def ui_init(self):
        self.create_menu()
        self.create_table()

    def create_menu(self): #создаем главное меню
        menu = Menu(self)
        self.config(menu=menu)

        mode_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label='Режим', menu=mode_menu)
        mode_menu.add_command(label='Просмотр', command=self.view_mode)
        mode_menu.add_command(label='Добавление', command=self.add_mode)
        mode_menu.add_command(label='Изменение', command=self.edit_mode)
        mode_menu.add_command(label='Удаление', command=self.delete_mode)

        req_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label='Запросы', menu=req_menu)
        req_menu.add_command(label='Найти по продолжительности жизни', command=self.parametr)
        req_menu.add_command(label='Имена от А до Я', command=self.grup)
        req_menu.add_command(label='Сложный запрос', command=self.hard)

    def parametr(self):
        def get_data():
            try:
                value = int(entry.get())
                if value <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(title='Ошибка', message='Введите целое положительное число')
            else:
                query = f'''select * from species where life = {value}'''
                self.render_data(query)
                top.destroy()
        top = tk.Toplevel(self)
        top.title('Параметризованный запрос')
        label = Label(top, text='Введите продолжительность жизни:')
        label.pack()
        entry = tk.Entry(top)
        entry.pack()
        button = Button(top, text='Выполнить', command=get_data)
        button.pack()

    def grup(self): #сортировка по алфавиту
        query = '''select * from species order by name asc'''
        self.render_data(query)
        
    def hard(self): #сложный запрос по двум таблицам
        query = '''select species.id,
species.name as "Название рыбы",
species.life as "Продолжительность жизни",
species.date as "Дата записи",
orders.name as "Из какой реки" from orders inner join species on orders.id = species.order_id'''
        self.render_data(query)

    def create_table(self): #создание интерфейса
        table_root = tk.Frame(self)
        self.table = ttk.Treeview(table_root, show='headings',
                                  selectmode='browse') #виджет с иерархической структурой
        self.table.pack(fill='y', side='left')
        yscroll = tk.Scrollbar(table_root, orient=tk.VERTICAL)   
        self.table.configure(yscroll=yscroll.set)#настройка изменений
        yscroll.pack(side='left', fill='y')
        table_root.pack(side='left', fill='both')

    def check(self): #проверка является ли файл пустым и сущесвтвует ли он
        conn = sqlite3.connect(db_file_name) #соединение с базой данных
        cursor = conn.cursor()#возвращает объект курсора
        #проверка наличия таблицы, если ее нет - создаем, также и у 2-й таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='species'")
        res = cursor.fetchone() #получение всех строк по одной

        if res is None:
            cursor.execute("""CREATE TABLE IF NOT EXISTS species (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL UNIQUE,
life INTEGER NOT NULL CHECK(life >0),
date TEXT NOT NULL,
order_id INTEGER NOT NULL);
""")
            records_table1 = [
    (1, "Щука", 10, "15.07.2015", 2),
    (2, "Судак", 15, "14.07.2015", 2),
    (3, "Берш", 12, "15.08.2015", 2),
    (4, "Окунь", 8, "15.07.2013", 2),
    (5, "Омуль", 12, "15.07.2011", 2),
    (6, "Лещ", 15, "11.03.2015", 2),
    (7, "Голавль", 10, "12.04.2015", 4),
    (8, "Сазан", 5, "15.07.2021", 2),
    (9, "Красноперка", 20, "09.07.2015", 4),
    (10, "Кефаль", 15, "06.07.2015", 4),
    (11, "Язь", 15, "15.02.2015", 2),
    (12, "Плотва", 20, "11.07.2015", 2),
    (13, "Пираруку", 3, "25.07.2015", 1),
    (14, "Тамбак", 10, "19.07.2015", 1),
    (15, "Паку", 8, "15.07.2011", 1),
    (16, "Пирании", 5, "15.02.2013", 1),
    (17, "Желтый сом", 15, "25.07.2015", 1),
    (18, "Тиляпия", 5, "15.03.2015", 3),
    (19, "Нильский окунь", 15, "09.07.2015", 3),
    (20, "Африканский сом", 8, "15.09.2015", 3),
    (21, "Барбус", 5, "15.07.2019", 3)]
            cursor.executemany("INSERT INTO species VALUES (?, ?, ?, ?, ?)", records_table1)
            conn.commit() #запись изменений на диск

        else:
            #проверка наличия данных в таблице, также и у 2-й таблицы
            cursor.execute("SELECT COUNT(*) FROM species")
            res = cursor.fetchone()
            if res[0] == 0:
                records_table1 = [
    (1, "Щука", 10, "15.07.2015", 2),
    (2, "Судак", 15, "14.07.2015", 2),
    (3, "Берш", 12, "15.08.2015", 2),
    (4, "Окунь", 8, "15.07.2013", 2),
    (5, "Омуль", 12, "15.07.2011", 2),
    (6, "Лещ", 15, "11.03.2015", 2),
    (7, "Голавль", 10, "12.04.2015", 4),
    (8, "Сазан", 5, "15.07.2021", 2),
    (9, "Красноперка", 20, "09.07.2015", 4),
    (10, "Кефаль", 15, "06.07.2015", 4),
    (11, "Язь", 15, "15.02.2015", 2),
    (12, "Плотва", 20, "11.07.2015", 2),
    (13, "Пираруку", 3, "25.07.2015", 1),
    (14, "Тамбак", 10, "19.07.2015", 1),
    (15, "Паку", 8, "15.07.2011", 1),
    (16, "Пирании", 5, "15.02.2013", 1),
    (17, "Желтый сом", 15, "25.07.2015", 1),
    (18, "Тиляпия", 5, "15.03.2015", 3),
    (19, "Нильский окунь", 15, "09.07.2015", 3),
    (20, "Африканский сом", 8, "15.09.2015", 3),
    (21, "Барбус", 5, "15.07.2019", 3)]
                cursor.executemany("INSERT INTO species VALUES (?, ?, ?, ?, ?)", records_table1)
                conn.commit()


        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL UNIQUE,
name_country TEXT NOT NULL UNIQUE,
temp INTEGER);
""")
            records_table2 = [
    (1, "Амазонка", "Южная Америка", 28),
    (2, "Волга", "Россия", 25),
    (3, "Нил", "Африка", 35),
    (4, "Янцзы", "Китай", 21)]
            cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", records_table2)
            conn.commit()

        else:
            cursor.execute("SELECT COUNT(*) FROM orders")
            result = cursor.fetchone()
            if result[0] == 0:
                records_table2 = [
    (1, "Амазонка", "Южная Америка", 28),
    (2, "Волга", "Россия", 25),
    (3, "Нил", "Африка", 35),
    (4, "Янцзы", "Китай", 21)]
                cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", records_table2)
                conn.commit()

    def view_mode(self): #передаем данные из таблицы на интерфейс
        query = '''select * from species'''
        self.render_data(query)

    def add_mode(self): #для всплывающего окна
        EditWindow(master=self, mode='add')

    def edit_mode(self): #для всплывающего окна
        selection = self.table.selection()
        if len(selection) == 0:
            messagebox.showerror(title='Ошибка', message='Выберите запись')
        else:
            EditWindow(master=self, mode='edit')

    def edit_row(self,data): #изменение данных через сравнение старой и новой информации
        id = self.table.selection()[0]
        query = f'''select species.name, species.life, species.date, species.order_id from species where species.id = {id}'''
        connection = sqlite3.connect(database=db_file_name)
        cursor = connection.cursor().execute(query)
        oldData = cursor.fetchone()
        result = []
        for column_index in range(len(oldData)):
            if data[column_index] != '' and data[column_index] != oldData[column_index]: 
                result.append(data[column_index])
                continue
            result.append(oldData[column_index])
        query = f'''update species set name = "{result[0]}", life = {result[1]}, 
                    date = "{result[2]}", order_id = {result[3]} 
                    where id = {id}'''
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        query = 'select * from species'
        self.render_data(query)
   
    def add_row(self, data): #добавление новой строки
        connection = sqlite3.connect(database=db_file_name)
        cursor = connection.cursor()
        query = f'''insert into species(name, life, date, order_id) values(?, ?, ?, ?)'''
        cursor.execute(query, tuple(data))
        connection.commit()
        cursor.close()
        connection.close()
   
    def delete_mode(self): #удаление выбранной пользователем строки
        selection = self.table.selection()
        if len(selection) == 0:
            messagebox.showerror(title='Ошибка', message='Выберите запись')
        else:
            result = messagebox.askyesno(title='Удаление', message='Вы точно хотите удалить запись из базы данных?')
            if result:
                self.delete_row()

    def render_data(self, query): #взаимодействие БД и интерфейса
        connection = sqlite3.connect(database=db_file_name)
        cursor = connection.cursor().execute(query)
        data = cursor.fetchall()
        columns = list(map(lambda i: i[0], cursor.description))
        column_keys = [i for i in range(1, len(columns))]
        self.table.config(columns=column_keys)
        self.table.delete(*self.table.get_children())
        for col_key in column_keys:
            self.table.heading(column=col_key, text=columns[col_key]) #определение заголовка
        for row in data:
            row_id = row[0]
            row_data = [row[index] for index in column_keys]
            self.table.insert(index=tk.END, iid=row_id, values=row_data, parent='')
        cursor.close()
        connection.close()

    def delete_row(self): #удаление строки по id
        selection = self.table.selection()[0]
        query = f"DELETE FROM species WHERE id={selection}"
        connection = sqlite3.connect(database=db_file_name)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        self.view_mode()

 
class EditWindow(tk.Toplevel):
    def __init__(self, master, mode): #mode - режим работы
        super().__init__(master)
        self.master = master
        self.mode = mode
        self.title(mode.capitalize())
        self.geometry('350x350')
        self.resizable(False, False)
        #создадим Entry и Combobox для ввода данных пользователем.
        self.name = tk.Entry(self)
        self.date = tk.Entry(self)
        self.life = tk.Entry(self)
        query = '''select orders.id, orders.name from orders'''
        connection = sqlite3.connect(database=db_file_name)
        cursor = connection.cursor().execute(query)
        self.select_data = cursor.fetchall()
        self.order_id = ttk.Combobox(self, values=list(map(lambda x: x[1], 
                                                           self.select_data)))
        self.order_id.current(0)
        Label(self, text='Название рыбы:').pack(side='top', fill='x')
        self.name.pack(side='top', fill='x', padx=10, pady=10)
        Label(self, text='Продолжительность жизни:').pack(side='top', fill='x')
        self.life.pack(side='top', fill='x', padx=10, pady=10)
        Label(self, text='Дата записи:').pack(side='top', fill='x')
        self.date.pack(side='top', fill='x', padx=10, pady=10)
        Label(self, text='Из какой реки:').pack(side='top', fill='x')
        self.order_id.pack(side='top', fill='x', padx=10, pady=10)
        tk.Button(self,text='Отправить', command=self.handle_submit).pack(side='top', fill='x', padx=10, pady=10)
        tk.Button(self,text='Отмена',command=lambda *args: self.destroy()).pack(side='top', fill='x', padx=10, pady=10)
        if mode == 'edit' :
            cur_id = self.master.table.focus()
            cur_item = self.master.table.item(cur_id)
            order_ids = list(map(lambda x: x[0], self.select_data))
            self.name.insert(0, cur_item['values'][0])
            self.life.insert(0, cur_item['values'][1])
            self.date.insert(0, cur_item['values'][2])
            self.order_id.current(order_ids.index(int(cur_item['values'][3])))
        cursor.close()
        connection.close()

    def handle_submit(self, *args): #handle_submit для обработки нажатия кнопки "Отправить"
        name = self.name.get()
        life = self.life.get()
        date = self.date.get()
        order_id = self.select_data[self.order_id.current()][0]
        if name == '':
            showerror('Ошибка!','Введите имя рыбы!')
            return
        if not life.isdigit():
            showerror('Ошибка!','Введите среднюю продолжительность жизни!\n(целое число)')
            return
        try:
            format = "%d.%m.%Y"
            datetime.strptime(date, format)#метод для преобразования строки
        except:
            showerror('Ошибка!','Введите дату наблюдения!\n(дд.мм.гггг)')
            return
        data=[name, life, date, order_id]
        if self.mode == 'add': #вызывает метод родительского окна
            self.master.add_row(data)
        if self.mode == 'edit': #вызывает метод родительского окна
            self.master.edit_row(data)
        self.destroy() #удаление дочернего окна

if __name__ == '__main__':
    app = App()
