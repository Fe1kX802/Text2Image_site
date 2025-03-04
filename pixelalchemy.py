from PIL import Image
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QComboBox,
    QLineEdit,
    QProgressBar,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
from PyQt6.QtGui import QFont, QIcon, QTransform, QPixmap
from PyQt6.QtCore import Qt, QSettings
import sys
import time
import os
import tkinter as tk

class Txt2Img(QWidget):
    def __init__(self):
        super().__init__()
        # Устанавливаем название окна
        self.setWindowTitle("PixelAlchemy")
        # Задаем размер окна
        self.resize(230, 300)
        # Создаем основной вертикальный макет
        v_layout = QVBoxLayout(self)
        
        # Устанавливаем иконку окна
        self.setWindowIcon(QIcon(os.path.join('images', 'icon.png')))

        # Создаем заголовок
        title_label = QLabel("Текст в картинку", alignment=Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Dungeon", 20, QFont.Weight.Bold)
        title_label.setFont(title_font)
        v_layout.addWidget(title_label)

        # Создаем кнопку загрузки файла
        h_load_file_layout = QHBoxLayout()
        load_button = QPushButton("Загрузить")
        load_button.clicked.connect(self.load_text_file)
        h_load_file_layout.addStretch()
        h_load_file_layout.addWidget(load_button)
        h_load_file_layout.addStretch()
        v_layout.addLayout(h_load_file_layout)

        # Создаем поле ввода имени файла
        h_name_layout = QHBoxLayout()
        name_label = QLabel("Имя:")
        self.name_input = QLineEdit("output")
        h_name_layout.addWidget(name_label)
        h_name_layout.addWidget(self.name_input)
        v_layout.addLayout(h_name_layout)

        # Создаем выпадающий список для выбора расширения файла
        h_extension_layout = QHBoxLayout()
        extension_label = QLabel("Расширение:")
        self.extension_combo_box = QComboBox()
        self.extension_combo_box.addItems(["png", "jpg", "webp", "ico", "bmp"])
        self.extension_combo_box.setCurrentIndex(0)
        h_extension_layout.addWidget(extension_label)
        h_extension_layout.addWidget(self.extension_combo_box)
        v_layout.addLayout(h_extension_layout)

        """# Создаем выпадающий список для выбора типа изображения
        h_color_type_layout = QHBoxLayout()
        color_type_label = QLabel("Тип изображения:")
        self.color_type_combo_box = QComboBox()
        self.color_type_combo_box.addItems(["Цветная", "Черно-белая"])
        self.color_type_combo_box.setCurrentIndex(0)
        h_color_type_layout.addWidget(color_type_label)
        h_color_type_layout.addWidget(self.color_type_combo_box)
        v_layout.addLayout(h_color_type_layout)"""

        # Создаем выпадающий список для выбора цветового формата
        h_color_format_layout = QHBoxLayout()
        color_format_label = QLabel("Цветовой формат:")
        self.color_format_combo_box = QComboBox()
        self.color_format_combo_box.addItems(["RGB", "CMYK"])
        self.color_format_combo_box.setCurrentIndex(0)
        h_color_format_layout.addWidget(color_format_label)
        h_color_format_layout.addWidget(self.color_format_combo_box)
        v_layout.addLayout(h_color_format_layout)

        # Создаем прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        v_layout.addWidget(self.progress_bar)

        # Создаем кнопки Старт и Отмена
        h_buttons_layout = QHBoxLayout()
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.close)
        start_button = QPushButton("Старт")
        start_button.clicked.connect(self.start_conversion)
        h_buttons_layout.addWidget(start_button)
        h_buttons_layout.addWidget(cancel_button)
        v_layout.addLayout(h_buttons_layout)

        # Создаем кнопку переключения темы
        self.theme_button = QPushButton("🌙 Темная тема")
        self.theme_button.clicked.connect(self.toggle_theme)

        # Создаем кнопку для выбора папки сохранения
        import getpass
        username = getpass.getuser()
        print(username)
        self.output_folder = f'C://'
        self.choose_folder_button = QPushButton("Путь сохранения")
        self.choose_folder_button.clicked.connect(self.choose_output_folder)
        h_theme_folder_layout = QHBoxLayout()
        h_theme_folder_layout.addWidget(self.theme_button)
        h_theme_folder_layout.addWidget(self.choose_folder_button)
        v_layout.addLayout(h_theme_folder_layout)

        # Загружаем сохраненную тему
        self.settings = QSettings('YourCompany', 'PixelAlchemy')
        self.dark_theme = self.settings.value('dark_theme', False, type=bool)

        # Применяем тему
        self.apply_theme()

        # Устанавливаем центральный виджет
        self.setLayout(v_layout)

        # Инициализируем переменные для хранения данных
        self.input_string = ""
        self.color = "Черно-белая"
        self.color_format = "RGB"

    def toggle_theme(self):
        """Переключение между темной и светлой темами"""
        self.dark_theme = not self.dark_theme
        self.settings.setValue('dark_theme', self.dark_theme)
        self.apply_theme()

    def apply_theme(self):
        """Применение выбранной темы"""
        if self.dark_theme:
            self.theme_button.setText("☀️ Светлая тема")
            # Устанавливаем стили для темной темы
            self.setStyleSheet("""
                QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #404040;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                }
                QComboBox {
                    background-color: #404040;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 6px;
                }
                QLineEdit {
                    background-color: #404040;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 6px;
                }
                QProgressBar {
                    border: 1px solid #555555;
                    border-radius: 6px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #3daee9;
                }
            """)
        else:
            self.theme_button.setText("🌙 Темная тема")
            # Устанавливаем стили для светлой темы
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                    color: #000000;
                }
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
                QComboBox {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    border-radius: 6px;
                }
                QLineEdit {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    border-radius: 6px;
                }
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 6px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #0dd600;
                }
            """)

    def loading_done(self):
        """Метод, вызываемый по завершении загрузки"""
        pass

    def load_text_file(self):
        """Метод для открытия диалога выбора файла"""
        file_dialog = QFileDialog.getOpenFileName(
            self, "Открыть текстовый файл", "", "Текстовые файлы (*.txt *.md);;Все файлы (*)"
        )
        if file_dialog[0]:
            file_path = Path(file_dialog[0])
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.input_string = file.read()
                print(self.input_string)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при чтении файла: {e}")

    def start_conversion(self):
        """Метод для запуска процесса преобразования текста в изображение"""
        if not self.input_string:
            QMessageBox.warning(self, "Предупреждение", "Файл пуст или не был загружен.")
            return

        # Получаем значения из интерфейса
        name = self.name_input.text().strip()
        extension = self.extension_combo_box.currentText()
        #self.color = self.color_type_combo_box.currentText()
        self.color_format = self.color_format_combo_box.currentText()

        # Преобразуем строку в массив ASCII значений
        array = []
        try:
            for char in self.input_string:
                ascii_value = ord(char)
                array.append(ascii_value)
        except NameError as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при преобразовании строки: {e}")
            return

        # Проверяем длину массива и дополняем его до кратности трем
        if len(array) % 3 != 0:
            array += [0] * (3 - (len(array) % 3))

        # Обновляем прогрессбар
        for count in range(101):
            self.progress_bar.setValue(count)
            QApplication.processEvents()
            time.sleep(0.01)

        # Создаем изображение
        self.create_image_from_array(array, name, extension, self.color, self.color_format)

        # Показываем сообщение об успешном сохранении
        QMessageBox.information(self, "Успех", f"Изображение успешно создано и сохранено как {name}.{extension}.")

    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        event.accept()

    def choose_output_folder(self):
        """Метод для выбора папки сохранения"""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            self.output_folder = folder
            QMessageBox.information(self, "Папка выбрана", f"Изображения будут сохраняться в:\n{folder}")

    def create_image_from_array(self, data, name, extension, color, color_format):
        """
        Метод для создания изображения из массива данных
        data: Массив данных, представляющий пиксели изображения
        name: Имя файла для сохранения
        extension: Расширение файла
        color: Тип изображения ('Цветная' или 'Черно-белая')
        color_format: Цветовой формат ('RGB' или 'CMYK')
        """

        def find_max_factors(n):
            max_factor1 = 1
            max_factor2 = n
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    factor1 = i
                    factor2 = n // i
                    if factor1 > max_factor1:
                        max_factor1 = factor1
                        max_factor2 = factor2
            return max_factor1, max_factor2


        width, height = find_max_factors(len(data))
        print(len(data))
        print(width)
        print(height)
        print(width * height)
        pixels = []
        image = Image.new("RGB", (width, height))

        if color == 'Цветная':
            pixels.append(255)
            pixels.append(255)
            for i in range(height):
                for j in range(width - 2):
                    r = data[j * i]
                    g = data[(j + 1) * i]
                    b = data[(j + 2) * i]
                    pixels.append((r, g, b))
        elif color == 'Черно-белая':
            for i in range(height*width):
                #for j in range(width):
                    r = data[i]
                    g = data[i]
                    b = data[i]
                    pixels.append((r, g, b))

        image.putdata(pixels)
        if color_format == 'CMYK':
            image = image.convert('CMYK')
        
        if self.output_folder:
            save_path = os.path.join(self.output_folder, f"{name}.{extension}")
        else:
            save_path = f"{name}.{extension}"
        
        image.save(save_path)
        print(f"Изображение сохранено как {save_path}")





class Img2Txt(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = "C:/"
        self.setWindowTitle("PixelAlchemy")
        # Задаем размер окна
        self.resize(230, 300)
        # Создаем основной вертикальный макет
        v_layout = QVBoxLayout(self)
        
        # Устанавливаем иконку окна
        self.setWindowIcon(QIcon(os.path.join('images', 'icon.png')))

        # Создаем заголовок
        title_label = QLabel("Картинка в текст", alignment=Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Dungeon", 20, QFont.Weight.Bold)
        title_label.setFont(title_font)
        v_layout.addWidget(title_label)

        # Создаем кнопку загрузки файла
        h_load_file_layout = QHBoxLayout()
        load_button = QPushButton("Загрузить исходный файл")
        load_button.clicked.connect(self.load_text_file)
        h_load_file_layout.addStretch()
        h_load_file_layout.addWidget(load_button)
        h_load_file_layout.addStretch()
        v_layout.addLayout(h_load_file_layout)

        # Создаем поле ввода имени файла
        h_name_layout = QHBoxLayout()
        name_label = QLabel("Имя:")
        self.name_input = QLineEdit("output")
        h_name_layout.addWidget(name_label)
        h_name_layout.addWidget(self.name_input)
        v_layout.addLayout(h_name_layout)

        # Создаем выпадающий список для выбора расширения файла
        h_extension_layout = QHBoxLayout()
        extension_label = QLabel("Расширение:")
        self.extension_combo_box = QComboBox()
        self.extension_combo_box.addItems(["txt", "md"])
        self.extension_combo_box.setCurrentIndex(0)
        h_extension_layout.addWidget(extension_label)
        h_extension_layout.addWidget(self.extension_combo_box)
        v_layout.addLayout(h_extension_layout)

        # Создаем прогресс бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        v_layout.addWidget(self.progress_bar)

        # Создаем кнопки Старт и Отмена
        h_buttons_layout = QHBoxLayout()
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.close)
        start_button = QPushButton("Старт")
        start_button.clicked.connect(self.image_to_text)
        h_buttons_layout.addWidget(start_button)
        h_buttons_layout.addWidget(cancel_button)
        v_layout.addLayout(h_buttons_layout)

        # Создаем кнопку переключения темы
        self.theme_button = QPushButton("🌙 Темная тема")
        self.theme_button.clicked.connect(self.toggle_theme)

        # Создаем кнопку для выбора папки сохранения
        self.output_folder = f'C://outputs'
        self.choose_folder_button = QPushButton("Путь сохранения")
        self.choose_folder_button.clicked.connect(self.choose_output_folder)
        h_theme_folder_layout = QHBoxLayout()
        h_theme_folder_layout.addWidget(self.theme_button)
        h_theme_folder_layout.addWidget(self.choose_folder_button)
        v_layout.addLayout(h_theme_folder_layout)

        # Загружаем сохраненную тему
        self.settings = QSettings('PixelAlchemy')
        self.dark_theme = self.settings.value('dark_theme', False, type=bool)

        # Применяем тему
        self.apply_theme()

        # Устанавливаем центральный виджет
        self.setLayout(v_layout)

    def toggle_theme(self):
        """Переключение между темной и светлой темами"""
        self.dark_theme = not self.dark_theme
        self.settings.setValue('dark_theme', self.dark_theme)
        self.apply_theme()

    def apply_theme(self):
        """Применение выбранной темы"""
        if self.dark_theme:
            self.theme_button.setText("☀️ Светлая тема")
            # Устанавливаем стили для темной темы
            self.setStyleSheet("""
                QWidget {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #404040;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #4a4a4a;
                }
                QComboBox {
                    background-color: #404040;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 6px;
                }
                QLineEdit {
                    background-color: #404040;
                    border: 1px solid #555555;
                    padding: 5px;
                    border-radius: 6px;
                }
                QProgressBar {
                    border: 1px solid #555555;
                    border-radius: 6px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #3daee9;
                }
            """)
        else:
            self.theme_button.setText("🌙 Темная тема")
            # Устанавливаем стили для светлой темы
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                    color: #000000;
                }
                QPushButton {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
                QComboBox {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    border-radius: 6px;
                }
                QLineEdit {
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    padding: 5px;
                    border-radius: 6px;
                }
                QProgressBar {
                    border: 1px solid #cccccc;
                    border-radius: 6px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #0dd600;
                }
            """)

    def loading_done(self):
        """Метод, вызываемый по завершении загрузки"""
        pass

    
    def load_text_file(self):
        """Метод для открытия диалога выбора файла"""
        file_dialog = QFileDialog.getOpenFileName(
            self, "Открыть изображение", "", "Изображения (*.png)"
        )
        if file_dialog[0]:
            self.image_path = file_dialog[0]
            QMessageBox.information(self, "Файл выбран", f"Выбран файл: {self.image_path}")


    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        event.accept()

    def choose_output_folder(self):
        """Метод для выбора папки сохранения"""
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if folder:
            self.output_folder = folder
            QMessageBox.information(self, "Папка выбрана", f"Изображения будут сохраняться в:\n{folder}")


    def image_to_text(self):
        """Метод для конвертации изображения в текст"""
        # Получаем значения из интерфейса
        name = self.name_input.text()
        extension = self.extension_combo_box.currentText()

        try:
            # Открываем изображение
            img = Image.open(self.image_path)
            width, height = img.size
            img = img.convert('RGB')
            text = ""

            # Конвертируем изображение в текст
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    ascii_code = r
                    char = chr(ascii_code)
                    text += char

            # Обновляем прогресс-бар
            for count in range(101):
                self.progress_bar.setValue(count)
                QApplication.processEvents()
                time.sleep(0.01)

            # Сохраняем результат
            save_path = os.path.join(self.output_folder, f"{name}.{extension}")
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(text)

            QMessageBox.information(self, "Успех", f"Файл сохранен как {save_path}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    mode = None
    root = tk.Tk()
    root.title("PixelAlchemy")
    root.geometry('300x140')
    lbl = tk.Label(root, text="Выберете режим работы")
    lbl.pack(pady=10)
    btn_txt2img = tk.Button(root, text="Текст в картинку",
                            command=lambda: (exec("global mode; mode='txt2img'"), root.destroy()))
    btn_txt2img.pack(pady=5)
    btn_img2txt = tk.Button(root, text="Картинка в текст",
                            command=lambda: (exec("global mode; mode='img2txt'"), root.destroy()))
    btn_img2txt.pack(pady=5)
    root.mainloop()

    app = QApplication(sys.argv)
    if mode == 'txt2img':
        ex = Txt2Img()
    elif mode == 'img2txt':
        ex = Img2Txt()
    else:
        sys.exit()

    ex.setWindowIcon(QIcon('icon.png'))   
    ex.show()
    sys.exit(app.exec())