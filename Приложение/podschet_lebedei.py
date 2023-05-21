import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import ttk
from start_my_yolo import activate_yolo
import os
import csv


class SwansApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1366x768")
        self.root.title("Определение подвида лебедей")
        self.root["bg"] = "gray22"
        # self.info_table = info_table

        # Создание кнопки для загрузки изображений
        self.load_button_image = ImageTk.PhotoImage(file="img_2.png")
        self.load_button = tk.Button(self.root, image=self.load_button_image, compound="left", text="Загрузить "
                                                                                                    "изображения",
                                     font=("Roboto", 15), command=self.load_images)
        self.load_button.place(x=590, y=668, width=300, height=50)
        self.load_button.config(relief="flat")

        # Создание кнопки для сохранения отчета
        self.record_button_image = ImageTk.PhotoImage(file="img_1.png")
        self.record_button = tk.Button(self.root, image=self.record_button_image, compound="left", text="Сохранить "
                                                                                                        "отчет",
                                       font=("Roboto", 15), command=self.record_stats_files)
        self.record_button.place(x=751, y=573, width=220, height=50)
        self.record_button.config(relief="flat")

        # Создание кнопки для расчета численности видов лебедей на изображении
        self.calculation_button_image = ImageTk.PhotoImage(file="img_3.png")
        self.calculation_button = tk.Button(self.root, image=self.calculation_button_image, compound="left",
                                            text="Рассчитать",
                                            font=("Roboto", 15), command=self.recognize_image)
        self.calculation_button.place(x=503.5, y=573, width=220, height=50)
        self.calculation_button.config(relief="flat")

        # Создание поля для отображения изображений
        self.image_label = tk.Label(self.root, text="Нажмите на кнопку Загрузить изображения", font=("Roboto", 15))
        self.image_label.place(x=410, y=60, width=640, height=480)

        # Создание стрелок для просмотра изображений
        self.prev_button = tk.Button(self.root, text="<", font=("Roboto", 15), command=self.show_prev_image)
        self.next_button = tk.Button(self.root, text=">", font=("Roboto", 15), command=self.show_next_image)
        self.prev_button.place(x=372, y=262)
        self.next_button.place(x=1061.5, y=262)

        # Создание таблицы
        self.data = []
        columns = ("Имя изобр.", "Название вида", "Кол-во особей")
        self.info_table = ttk.Treeview(self.root, columns=columns, show="headings")
        self.info_table.place(x=40, y=60, width=310, height=650)
        style = ttk.Style()
        style.configure("Treeview", font=("Roboto", 8))
        self.info_table.tag_configure('ttk', font=("Roboto", 8))
        self.info_table.heading("Имя изобр.", text="Имя изобр.", anchor="w")
        self.info_table.heading("Название вида", text="Название вида", anchor="w")
        self.info_table.heading("Кол-во особей", text="Кол-во особей", anchor="w")

        # настраиваем столбцы
        self.info_table.column("#1", stretch=False, width=90)
        self.info_table.column("#2", stretch=False, width=130)
        self.info_table.column("#3", stretch=False, width=90)

        self.klikun_num = 0
        self.maliy_num = 0
        self.shipun_num = 0

        for col in columns:
            self.info_table.heading(col, text=col)

        for row in self.data:
            self.info_table.insert("", "end", values=row)

        # добавляем вертикальную прокрутку
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.info_table.yview)
        scrollbar.pack(side="right", fill="y")

        self.info_table["yscrollcommand"] = scrollbar.set

        # Создание таблицы со статистикой
        self.stats = []
        stats_columns = ("Вид", "Количество")
        self.stats_table = ttk.Treeview(self.root, columns=stats_columns, show="headings")
        self.stats_table.place(x=1110, y=60, width=195.5, height=650)
        style = ttk.Style()
        style.configure("Treeview", font=("Roboto", 8))
        self.stats_table.tag_configure('ttk', font=("Roboto", 8))
        self.stats_table.heading("Вид", text="Вид", anchor="w")
        self.stats_table.heading("Количество", text="Количество", anchor="w")

        # настраиваем столбцы
        self.stats_table.column("#1", stretch=False, width=98)
        self.stats_table.column("#2", stretch=False, width=98)

        for stats_col in stats_columns:
            self.stats_table.heading(stats_col, text=stats_col)

        for stats_row in self.stats:
            self.stats_table.insert("", "end", values=stats_row)

        self.stats_all = []

        self.bind_table()

        # Создание переменных для хранения списка загруженных изображений и текущего отображаемого изображения
        self.images = []
        self.current_image_index = 0

        # Пути хранения картинок
        self.image_path = []

        self.text_1 = tk.Label(self.root, text="Таблица с численностью каждого вида на изображении", font=("Roboto", 8))
        self.text_1.place(x=47, y=40)

        self.text_2 = tk.Label(self.root, text="Статистика по изображениям", font=("Roboto", 8))
        self.text_2.place(x=1130, y=40)

    def load_images(self):
        # Очистка списка загруженных изображений перед загрузкой новых
        self.images.clear()
        self.image_path.clear()

        # Вызов диалогового окна для выбора изображений
        filenames = filedialog.askopenfilenames(filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        print(len(filenames))
        
        # print(filenames)

        # Загрузка выбранных изображений и добавление их в список
        for filename in filenames:
            image = Image.open(filename)
            self.images.append(image)
            self.image_path.append(filename)

        # Отображание первого изображения из списка
        if self.images:
            self.show_image(0)

    def show_image(self, index):
        # Обновление текущий отображаемый индекс изображения
        self.current_image_index = index

        # Масштабирование изображения для подгонки размеров окна
        image = self.images[index].resize((640, 480))

        # Создание объекта ImageTk для отображения изображения на Label
        photo = ImageTk.PhotoImage(image)

        # Обновление Label для отображения нового изображения
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def show_prev_image(self):
        # Переключение на предыдущее изображение в списке
        if self.current_image_index > 0:
            self.show_image(self.current_image_index - 1)

    def show_next_image(self):
        # Переключение на следующее изображение в списке
        if self.current_image_index < len(self.images) - 1:
            self.show_image(self.current_image_index + 1)

    def recognize_image(self):
        for i in range(len(self.image_path)):
            print("Обработка изображения №", i)
            result = activate_yolo(model_path=R'best.pt', image_path=self.image_path[i])
            self.data.append((self.file_path(self.image_path[i]), result[1], result[0]))
            print((result[0], '-', result[1]))
            self.fill_table(i)
        self.fill_table_stat()

    def file_path(self, image_path):
        file_path = image_path
        file_name = os.path.basename(file_path)
        return file_name

    def fill_table(self, i):
        tens = self.data[i][1]
        for j in tens:
            tens_item = int(j.item()) # tens.item()
            if tens_item == 0:
                self.info_table.insert("", "end", values=(self.data[i][0], "кликун", self.data[i][2]))
                self.klikun_num += 1

            elif tens_item == 1:
                self.info_table.insert("", "end", values=(self.data[i][0], "малый", self.data[i][2]))
                self.maliy_num += 1

            elif tens_item == 2:
                self.info_table.insert("", "end", values=(self.data[i][0], "шипун", self.data[i][2]))
                self.shipun_num += 1

    def fill_table_stat(self):
        self.stats_table.insert("", "end", values=("Кликун", self.klikun_num))
        self.stats_table.insert("", "end", values=("Малый", self.maliy_num))
        self.stats_table.insert("", "end", values=("Шипун", self.shipun_num))

        self.stats_all = [("Кликун", self.klikun_num), ("Малый", self.maliy_num), ("Шипун", self.shipun_num)]

    def record_stats_files(self):
        with open("record_files.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.data)

        with open("record_stat_all.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.stats_all)

    def bind_table(self):
        self.info_table.bind("<ButtonRelease-1>", self.show_image_from_table)

    def show_image_from_table(self, event):
        item = self.info_table.selection()[0]
        index = int(item.split("I")[1]) - 1
        self.show_image(index)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SwansApp()
    app.run()
