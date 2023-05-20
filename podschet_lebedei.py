import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog


class SwansApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1366x768")
        self.root.title("Определение лебедей по виду")
        self.root["bg"] = "gray22"

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
                                       font=("Roboto", 15))
        self.record_button.place(x=751, y=573, width=220, height=50)
        self.record_button.config(relief="flat")

        # Создание кнопки для расчета численности видов лебедей на изображении
        self.calculation_button_image = ImageTk.PhotoImage(file="img_3.png")
        self.calculation_button = tk.Button(self.root, image=self.calculation_button_image, compound="left",
                                            text="Рассчитать",
                                            font=("Roboto", 15))
        self.calculation_button.place(x=503.5, y=573, width=220, height=50)
        self.calculation_button.config(relief="flat")

        # Создание поля для отображения изображений
        self.image_label = tk.Label(self.root)
        self.image_label.place(x=410, y=60, width=640, height=480)

        # Создание стрелок для просмотра изображений
        self.prev_button = tk.Button(self.root, text="<", font=("Roboto", 15), command=self.show_prev_image)
        self.next_button = tk.Button(self.root, text=">", font=("Roboto", 15), command=self.show_next_image)
        self.prev_button.place(x=372, y=262)
        self.next_button.place(x=1061.5, y=262)

        # Создание таблицы
        self.info_label_1 = tk.Label(self.root, text="", font=("Roboto", 15), bg="white", fg="white")
        self.info_label_1.place(x=60, y=60, width=270, height=650)

        # Создание текстового поля для отображения информации о лебедях
        self.info_label_2 = tk.Label(self.root, text="", font=("Roboto", 15), bg="white", fg="white")
        self.info_label_2.place(x=1130, y=60, width=175.5, height=650)

        # Создание переменных для хранения списка загруженных изображений и текущего отображаемого изображения
        self.images = []
        self.current_image_index = 0

    def load_images(self):
        # Очистка списка загруженных изображений перед загрузкой новых
        self.images.clear()

        # Вызов диалогового окна для выбора изображений
        filenames = filedialog.askopenfilenames(filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])

        # Загрузка выбранных изображений и добавление их в список
        for filename in filenames:
            image = Image.open(filename)
            self.images.append(image)

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

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SwansApp()
    app.run()
