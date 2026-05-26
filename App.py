import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QCheckBox, QComboBox, QLineEdit, QSpinBox, 
    QDoubleSpinBox, QSlider, QListWidget, QDial, QGroupBox
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        # Настройка главного окна
        self.setWindowTitle("Демонстрация виджетов")
        self.setFixedSize(QSize(900, 600))
        
        # Создаём виджет с вкладками для удобной группировки всех элементов
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Создаём каждую вкладку с разными виджетами
        self.tabs.addTab(self.create_dial_tab(), "Циферблат (Dial)")
        self.tabs.addTab(self.create_slider_tab(), "Ползунок (Slider)")
        self.tabs.addTab(self.create_spinbox_tab(), "Счётчик (SpinBox)")
        self.tabs.addTab(self.create_lineedit_tab(), "Текстовое поле (LineEdit)")
        self.tabs.addTab(self.create_listwidget_tab(), "Список (ListWidget)")
        self.tabs.addTab(self.create_label_tab(), "Метка (Label)")
        self.tabs.addTab(self.create_button_tab(), "Кнопка (Button)")
        self.tabs.addTab(self.create_checkbox_tab(), "Флажок (CheckBox)")
        self.tabs.addTab(self.create_combobox_tab(), "Выпадающий список (ComboBox)")
        
        # Общий лог для вывода информации со всех виджетов
        self.log_label = QLabel("Лог событий будет отображаться здесь...")
        self.log_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;")
        self.log_label.setWordWrap(True)
        self.log_label.setMinimumHeight(100)
        
        # Добавляем область лога внизу главного окна
        main_container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.log_label)
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)
    
    # Вспомогательный метод для записи сообщений в лог
    def log_message(self, message):
        """Добавляет сообщение в лог и выводит в консоль"""
        current_text = self.log_label.text()
        if current_text == "Лог событий будет отображаться здесь...":
            current_text = ""
        self.log_label.setText(f"{message}\n{current_text}"[:500])  # Ограничиваем длину лога
        print(message)  # Также выводим в консоль для отладки
    
    # ВКЛАДКА 1: QDial - круговой циферблат
    def create_dial_tab(self):
        """Создаёт вкладку с виджетом Dial (круговой регулятор)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Создаём круговой циферблат
        dial = QDial()
        dial.setRange(0, 100)           # Устанавливаем диапазон
        dial.setSingleStep(1)             # Шаг изменения (целое число, т.к. QDial работает с int)
        dial.setNotchesVisible(True)      # Показывать засечки
        dial.setFixedSize(200, 200)       # Фиксированный размер
        
        # Подключаем сигналы
        dial.valueChanged.connect(lambda v: self.log_message(f"Dial: значение изменилось на {v}"))
        dial.sliderMoved.connect(lambda p: self.log_message(f"Dial: ползунок перемещён в позицию {p}"))
        dial.sliderPressed.connect(lambda: self.log_message("Dial: ползунок нажат"))
        dial.sliderReleased.connect(lambda: self.log_message("Dial: ползунок отпущен"))
        
        # Метка для отображения текущего значения
        value_label = QLabel("Значение: 0")
        dial.valueChanged.connect(lambda v: value_label.setText(f"Значение: {v}"))
        
        layout.addWidget(dial, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("QDial - круговой регулятор. Используйте мышь или колёсико для изменения."))
        
        widget.setLayout(layout)
        return widget
    
    # ВКЛАДКА 2: QSlider - линейный ползунок
    def create_slider_tab(self):
        """Создаёт вкладку с виджетом Slider (линейный ползунок)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Создаём горизонтальный ползунок
        slider = QSlider(Qt.Orientation.Horizontal)  # Горизонтальная ориентация
        slider.setRange(0, 10)                     # Диапазон
        slider.setSingleStep(1)                       # Шаг при нажатии стрелок
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)  # Положение засечек
        slider.setTickInterval(1)                    # Интервал между засечками
        
        # Подключаем сигналы
        slider.valueChanged.connect(lambda v: self.log_message(f"Slider: значение изменилось на {v}"))
        slider.sliderMoved.connect(lambda p: self.log_message(f"Slider: ползунок перемещён в позицию {p}"))
        slider.sliderPressed.connect(lambda: self.log_message("Slider: ползунок нажат"))
        slider.sliderReleased.connect(lambda: self.log_message("Slider: ползунок отпущен"))
        
        # Метка для отображения текущего значения
        value_label = QLabel("Значение: 0")
        slider.valueChanged.connect(lambda v: value_label.setText(f"Значение: {v}"))
        
        layout.addWidget(slider)
        layout.addWidget(value_label)
        layout.addWidget(QLabel("QSlider - линейный ползунок. Можно перетаскивать или использовать стрелки."))
        
        widget.setLayout(layout)
        return widget
    
    # ВКЛАДКА 3: QSpinBox и QDoubleSpinBox - числовые счётчики
    def create_spinbox_tab(self):
        """Создаёт вкладку с виджетами SpinBox (целые числа) и DoubleSpinBox (дробные)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Группа для целых чисел (SpinBox)
        group_int = QGroupBox("Целые числа (QSpinBox)")
        int_layout = QVBoxLayout()
        
        spinbox = QSpinBox()
        spinbox.setRange(-10, 100)          # Диапазон значений
        spinbox.setPrefix("$")              # Префикс перед числом
        spinbox.setSuffix(" руб")           # Суффикс после числа
        spinbox.setSingleStep(3)            # Шаг изменения
        
        # Сигналы: valueChanged передаёт число, textChanged передаёт строку
        spinbox.valueChanged.connect(lambda v: self.log_message(f"SpinBox (целое): значение = {v}"))
        spinbox.textChanged.connect(lambda s: self.log_message(f"SpinBox (целое): текст = '{s}'"))
        
        int_layout.addWidget(spinbox)
        group_int.setLayout(int_layout)
        
        # Группа для дробных чисел (DoubleSpinBox)
        group_double = QGroupBox("Дробные числа (QDoubleSpinBox)")
        double_layout = QVBoxLayout()
        
        doublespinbox = QDoubleSpinBox()
        doublespinbox.setRange(-10.5, 100.5)   # Диапазон значений
        doublespinbox.setPrefix("≈")           
        doublespinbox.setSuffix(" мм")         
        doublespinbox.setSingleStep(0.5)       # Шаг изменения (дробный)
        doublespinbox.setDecimals(2)           # Количество знаков после запятой
        
        doublespinbox.valueChanged.connect(lambda v: self.log_message(f"DoubleSpinBox (дробное): значение = {v}"))
        
        double_layout.addWidget(doublespinbox)
        group_double.setLayout(double_layout)
        
        layout.addWidget(group_int)
        layout.addWidget(group_double)
        layout.addWidget(QLabel("QSpinBox - для целых чисел, QDoubleSpinBox - для дробных."))
        
        widget.setLayout(layout)
        return widget
    
    # ВКЛАДКА 4: QLineEdit - однострочное текстовое поле
    def create_lineedit_tab(self):
        """Создаёт вкладку с виджетом LineEdit (текстовое поле)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        lineedit = QLineEdit()
        lineedit.setMaxLength(20)                     # Максимальная длина текста
        lineedit.setPlaceholderText("Введите текст здесь...")  # Подсказка
        lineedit.setClearButtonEnabled(True)          # Кнопка очистки
        
        # Подключаем сигналы
        lineedit.returnPressed.connect(lambda: self.log_message("LineEdit: нажат Enter"))
        lineedit.selectionChanged.connect(lambda: self.log_message(f"LineEdit: выделен текст '{lineedit.selectedText()}'"))
        lineedit.textChanged.connect(lambda s: self.log_message(f"LineEdit: текст изменён на '{s}'"))
        lineedit.textEdited.connect(lambda s: self.log_message(f"LineEdit: текст отредактирован пользователем '{s}'"))
        
        # Кнопка для демонстрации установки текста программно
        button = QPushButton("Установить текст 'BOOM!'")
        button.clicked.connect(lambda: lineedit.setText("BOOM!"))
        
        # Чекбокс для переключения режима только для чтения
        readonly_check = QCheckBox("Только для чтения (ReadOnly)")
        readonly_check.toggled.connect(lineedit.setReadOnly)
        
        layout.addWidget(lineedit)
        layout.addWidget(button)
        layout.addWidget(readonly_check)
        layout.addWidget(QLabel("QLineEdit - однострочное текстовое поле. Поддерживает сигналы изменения текста и выделения."))
        
        widget.setLayout(layout)
        return widget
    
    # ВКЛАДКА 5: QListWidget - список элементов
    def create_listwidget_tab(self):
        """Создаёт вкладку с виджетом ListWidget (список)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        listwidget = QListWidget()
        # Добавляем элементы в список
        listwidget.addItems(["Яблоко", "Банан", "Апельсин", "Виноград", "Арбуз"])
        listwidget.addItem("Дополнительный элемент")
        
        # Сигналы: currentItemChanged передаёт текущий элемент QListWidgetItem
        #          currentTextChanged передаёт текст текущего элемента
        listwidget.currentItemChanged.connect(
            lambda current, previous: self.log_message(f"ListWidget: выбран элемент '{current.text() if current else None}'")
        )
        listwidget.currentTextChanged.connect(
            lambda s: self.log_message(f"ListWidget: текущий текст изменён на '{s}'")
        )
        
        # Кнопка для добавления нового элемента
        input_field = QLineEdit()
        input_field.setPlaceholderText("Новый элемент")
        add_button = QPushButton("Добавить в список")
        add_button.clicked.connect(lambda: listwidget.addItem(input_field.text()) if input_field.text() else None)
        
        # Кнопка для удаления выбранного элемента
        remove_button = QPushButton("Удалить выбранный")
        remove_button.clicked.connect(lambda: listwidget.takeItem(listwidget.currentRow()))
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(input_field)
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        
        layout.addWidget(listwidget)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("QListWidget - список элементов. Можно добавлять, удалять и выбирать элементы."))
        
        widget.setLayout(layout)
        return widget
    
    # ВКЛАДКА 6: QLabel - текстовая метка
    def create_label_tab(self):
        """Создаёт вкладку с виджетом Label (текстовая метка)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Создаём метку с текстом
        label = QLabel("Привет, мир!")
        
        # Настраиваем шрифт
        font = label.font()
        font.setPointSize(30)      # Размер шрифта 30
        font.setBold(True)         # Жирный
        label.setFont(font)
        
        # Выравнивание: по центру по горизонтали и вертикали
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Стилизация с помощью CSS
        label.setStyleSheet("background-color: lightblue; border: 2px solid navy; border-radius: 10px; padding: 20px;")
        
        # Кнопки для изменения текста
        button1 = QPushButton("Изменить текст на 'Python'")
        button1.clicked.connect(lambda: label.setText("Python"))
        
        button2 = QPushButton("Сбросить текст")
        button2.clicked.connect(lambda: label.setText("Привет, мир!"))
        
        layout.addWidget(label)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(QLabel("QLabel - используется для отображения текста, изображений или HTML."))
        
        widget.setLayout(layout)
        return widget
    
    # ВКЛАДКА 7: QPushButton - кнопка
    def create_button_tab(self):
        """Создаёт вкладку с виджетом Button (кнопка)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.button_is_checked = False  # Храним состояние кнопки
        
        button = QPushButton("Нажми меня!")
        button.setCheckable(True)       # Кнопка может быть "зажатой" (переключатель)
        
        # Подключаем сигналы
        button.clicked.connect(lambda: self.log_message("Кнопка: нажата (сигнал clicked)"))
        button.clicked.connect(self.on_button_toggled)  # Для обработки состояния
        button.pressed.connect(lambda: self.log_message("Кнопка: нажата (сигнал pressed)"))
        button.released.connect(lambda: self.log_message("Кнопка: отпущена (сигнал released)"))
        
        # Метка для отображения состояния кнопки
        state_label = QLabel("Состояние: отжата")
        button.clicked.connect(lambda checked: state_label.setText(f"Состояние: {'зажата' if checked else 'отжата'}"))
        
        # Кнопка для программного изменения состояния
        toggle_button = QPushButton("Программно переключить состояние")
        toggle_button.clicked.connect(lambda: button.setChecked(not button.isChecked()))
        
        layout.addWidget(button)
        layout.addWidget(state_label)
        layout.addWidget(toggle_button)
        layout.addWidget(QLabel("QPushButton - кнопка. При установке setCheckable(True) работает как переключатель."))
        
        widget.setLayout(layout)
        return widget
    
    def on_button_toggled(self, checked):
        """Обработчик изменения состояния кнопки"""
        self.button_is_checked = checked
        self.log_message(f"Кнопка: состояние изменилось на {'зажата' if checked else 'отжата'}")
    
    # ВКЛАДКА 8: QCheckBox - флажок (чекбокс)
    def create_checkbox_tab(self):
        """Создаёт вкладку с виджетом CheckBox (флажок)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Обычный чекбокс (два состояния)
        checkbox1 = QCheckBox("Обычный чекбокс (2 состояния)")
        checkbox1.setCheckState(Qt.CheckState.Checked)  # Устанавливаем в отмеченное состояние
        
        # Трёхсостояний чекбокс
        checkbox2 = QCheckBox("Трёхсостояний чекбокс")
        checkbox2.setTristate(True)                     # Включаем три состояния
        checkbox2.setCheckState(Qt.CheckState.PartiallyChecked)  # Частично отмечен
        
        # Сигнал stateChanged передаёт состояние (int: 0, 1, 2)
        checkbox1.stateChanged.connect(lambda s: self.log_message(f"Чекбокс1: состояние = {s} ({self.get_check_state_name(s)})"))
        checkbox2.stateChanged.connect(lambda s: self.log_message(f"Чекбокс2: состояние = {s} ({self.get_check_state_name(s)})"))
        
        layout.addWidget(checkbox1)
        layout.addWidget(checkbox2)
        layout.addWidget(QLabel("QCheckBox - флажок. setTristate(True) включает третье состояние 'частично'."))
        
        widget.setLayout(layout)
        return widget
    
    def get_check_state_name(self, state):
        """Возвращает строковое название состояния чекбокса"""
        if state == Qt.CheckState.Checked.value:
            return "Отмечено"
        elif state == Qt.CheckState.PartiallyChecked.value:
            return "Частично отмечено"
        else:
            return "Не отмечено"
    
    # ВКЛАДКА 9: QComboBox - выпадающий список
    def create_combobox_tab(self):
        """Создаёт вкладку с виджетом ComboBox (выпадающий список)"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        combobox = QComboBox()
        combobox.addItems(["Красный", "Зелёный", "Синий", "Жёлтый", "Чёрный"])
        combobox.addItem("Белый")  # Альтернативный способ добавления
        
        # Сигналы: currentIndexChanged передаёт индекс (int)
        #          currentTextChanged передаёт текст (str)
        combobox.currentIndexChanged.connect(
            lambda index: self.log_message(f"ComboBox: выбран индекс {index}, значение '{combobox.currentText()}'")
        )
        combobox.currentTextChanged.connect(
            lambda text: self.log_message(f"ComboBox: изменён текущий текст на '{text}'")
        )
        
        # Поле для добавления нового элемента
        input_field = QLineEdit()
        input_field.setPlaceholderText("Новый элемент для списка")
        add_button = QPushButton("Добавить в выпадающий список")
        add_button.clicked.connect(lambda: combobox.addItem(input_field.text()) if input_field.text() else None)
        
        layout.addWidget(combobox)
        layout.addWidget(input_field)
        layout.addWidget(add_button)
        layout.addWidget(QLabel("QComboBox - выпадающий список. Можно добавлять элементы динамически."))
        
        widget.setLayout(layout)
        return widget


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())  # Запуск цикла событий