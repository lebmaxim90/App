import sys
import os
from pathlib import Path

from PyQt6.QtCore import Qt, QDir, QTimer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QFileDialog, QProgressBar, QMessageBox, QSplitter, QTextEdit
)
from PyQt6.QtGui import QIcon, QFont


class FileSearchApp(QMainWindow):
    """
    Приложение для поиска файлов и работы с ними
    """
    def __init__(self):
        super().__init__()
        self.search_results = []  # Храним результаты поиска
        self.current_directory = str(Path.home())  # Стартовая директория
        
        self.setup_ui()  # Настраиваем интерфейс
        self.load_directory_contents()  # Загружаем содержимое текущей папки
    
    def setup_ui(self):
        """Создаёт и настраивает все виджеты интерфейса"""
        self.setWindowTitle("Файловый менеджер с поиском")
        self.setGeometry(100, 100, 1200, 700)  # x, y, width, height
        
        # Центральный виджет и главный layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # ========== ВЕРХНЯЯ ПАНЕЛЬ (навигация и поиск) ==========
        top_panel = QWidget()
        top_layout = QHBoxLayout(top_panel)
        
        # Кнопка "Назад"
        self.back_button = QPushButton("◀ Назад")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setEnabled(False)  # Изначально неактивна
        
        # Поле с текущим путём
        self.path_edit = QLineEdit(self.current_directory)
        self.path_edit.returnPressed.connect(self.navigate_to_path)  # Enter для перехода
        
        # Кнопка "Выбрать папку"
        self.browse_button = QPushButton("📁 Обзор")
        self.browse_button.clicked.connect(self.browse_directory)
        
        top_layout.addWidget(self.back_button)
        top_layout.addWidget(self.path_edit, 1)  # stretch=1 - растягивается
        top_layout.addWidget(self.browse_button)
        
        # ========== ПАНЕЛЬ ПОИСКА ==========
        search_panel = QWidget()
        search_layout = QHBoxLayout(search_panel)
        
        # Поле для поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Введите текст для поиска в файлах...")
        self.search_input.returnPressed.connect(self.search_in_files)  # Поиск по Enter
        
        # Кнопка поиска
        self.search_button = QPushButton("Найти")
        self.search_button.clicked.connect(self.search_in_files)
        
        # Кнопка поиска по имени файла
        self.search_name_button = QPushButton("Поиск по имени")
        self.search_name_button.clicked.connect(self.search_by_name)
        
        # Прогресс-бар для длительных операций
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        search_layout.addWidget(self.search_input, 2)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.search_name_button)
        search_layout.addWidget(self.progress_bar, 1)
        
        # ========== ОСНОВНАЯ ОБЛАСТ (сплиттер) ==========
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Левая панель: список файлов в текущей папке
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        left_label = QLabel("📂 Содержимое текущей папки")
        left_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.open_file_or_folder)  # Двойной клик
        
        left_layout.addWidget(left_label)
        left_layout.addWidget(self.file_list)
        
        # Правая панель: результаты поиска и просмотр содержимого файлов
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Результаты поиска
        search_label = QLabel("🔎 Результаты поиска")
        search_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.open_result_file)  # Двойной клик для открытия
        
        # Просмотр содержимого файла
        preview_label = QLabel("📄 Просмотр содержимого файла:")
        preview_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)  # Только для чтения
        
        right_layout.addWidget(search_label)
        right_layout.addWidget(self.results_list, 1)
        right_layout.addWidget(preview_label)
        right_layout.addWidget(self.preview_text, 1)
        
        # Добавляем виджеты в сплиттер
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 800])  # Начальная ширина панелей
        
        # Собираем главное окно
        main_layout.addWidget(top_panel)
        main_layout.addWidget(search_panel)
        main_layout.addWidget(splitter)
        
        # ========== СТАТУСНАЯ СТРОКА ==========
        self.status_label = QLabel("Готов к работе")
        self.statusBar().addWidget(self.status_label)
    
    def load_directory_contents(self):
        """Загружает содержимое текущей директории в левый список"""
        self.file_list.clear()
        
        try:
            path = Path(self.current_directory)
            
            # Сначала отображаем папки
            folders = [item for item in path.iterdir() if item.is_dir()]
            # Затем файлы
            files = [item for item in path.iterdir() if item.is_file()]
            
            # Сортируем по имени
            folders.sort(key=lambda x: x.name.lower())
            files.sort(key=lambda x: x.name.lower())
            
            # Добавляем папки
            for folder in folders:
                item = QListWidgetItem(f"📁 {folder.name}")
                item.setData(Qt.ItemDataRole.UserRole, str(folder))  # Сохраняем полный путь
                self.file_list.addItem(item)
            
            # Добавляем файлы
            for file in files:
                size = file.stat().st_size
                size_str = self.format_file_size(size)
                item = QListWidgetItem(f"📄 {file.name} ({size_str})")
                item.setData(Qt.ItemDataRole.UserRole, str(file))
                self.file_list.addItem(item)
            
            # Обновляем статус
            self.status_label.setText(f"Загружено: {len(folders)} папок, {len(files)} файлов")
            
        except PermissionError:
            self.status_label.setText("Нет доступа к этой папке")
        except Exception as e:
            self.status_label.setText(f"Ошибка: {str(e)}")
    
    def open_file_or_folder(self, item):
        """Открывает файл или переходит в папку по двойному клику"""
        path_str = item.data(Qt.ItemDataRole.UserRole)
        path = Path(path_str)
        
        if path.is_dir():
            # Переходим в папку
            self.current_directory = str(path)
            self.path_edit.setText(self.current_directory)
            self.load_directory_contents()
            
            # Активируем кнопку "Назад"
            self.back_button.setEnabled(True)
        else:
            # Открываем файл (в системной программе по умолчанию)
            self.preview_file_content(path_str)
    
    def preview_file_content(self, filepath):
        """Показывает содержимое текстового файла в области предпросмотра"""
        path = Path(filepath)
        
        # Проверяем расширение для текстовых файлов
        text_extensions = {'.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.md', '.csv'}
        
        if path.suffix.lower() in text_extensions:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Ограничиваем длину для производительности
                    if len(content) > 10000:
                        content = content[:10000] + "\n\n... (файл обрезан, слишком большой)"
                    self.preview_text.setText(content)
                    self.status_label.setText(f"Просмотр: {path.name}")
            except Exception as e:
                self.preview_text.setText(f"Не удалось прочитать файл: {str(e)}")
        else:
            self.preview_text.setText(f"[Бинарный файл] {path.name}\n\nНевозможно отобразить содержимое.")
    
    def search_in_files(self):
        """Ищет текст во всех файлах текущей папки (рекурсивно)"""
        search_text = self.search_input.text().strip()
        
        if not search_text:
            QMessageBox.warning(self, "Внимание", "Введите текст для поиска")
            return
        
        # Очищаем предыдущие результаты
        self.results_list.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.status_label.setText("Поиск...")
        
        # Запускаем поиск в отдельном потоке (здесь упрощённо, без QThread)
        # В реальном приложении для больших папок нужно использовать QThread
        root_path = Path(self.current_directory)
        results = []
        
        # Рекурсивный поиск
        file_count = 0
        for file_path in root_path.rglob("*"):
            if file_path.is_file():
                file_count += 1
                # Обновляем прогресс каждые 100 файлов
                if file_count % 100 == 0:
                    self.progress_bar.setValue(min(file_count, 100))
                    QApplication.processEvents()  # Позволяет GUI отвечать
                
                # Проверяем текстовые файлы
                text_extensions = {'.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.md', '.csv', '.log'}
                if file_path.suffix.lower() in text_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if search_text.lower() in content.lower():
                                # Находим строки с совпадением
                                lines = []
                                for i, line in enumerate(content.split('\n'), 1):
                                    if search_text.lower() in line.lower():
                                        lines.append(f"Строка {i}: {line[:100]}")
                                
                                results.append((file_path, lines[:3]))  # Берём первые 3 совпадения
                    except:
                        pass  # Пропускаем файлы, которые не удалось прочитать
        
        # Отображаем результаты
        for file_path, matches in results:
            item_text = f"📄 {file_path.name} ({len(matches)} совпадений)\n   {file_path.parent}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, str(file_path))
            item.setData(Qt.ItemDataRole.UserRole + 1, matches)  # Сохраняем совпадения
            self.results_list.addItem(item)
        
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Поиск завершён. Найдено {len(results)} файлов (проверено {file_count} файлов)")
        
        if not results:
            QMessageBox.information(self, "Результаты поиска", f"Текст '{search_text}' не найден")
    
    def search_by_name(self):
        """Ищет файлы по имени"""
        search_name = self.search_input.text().strip()
        
        if not search_name:
            QMessageBox.warning(self, "Внимание", "Введите имя файла для поиска")
            return
        
        self.results_list.clear()
        root_path = Path(self.current_directory)
        results = []
        
        # Используем glob для поиска по шаблону
        pattern = f"*{search_name}*"
        
        for file_path in root_path.rglob(pattern):
            if file_path.is_file():
                results.append(file_path)
        
        # Отображаем результаты
        for file_path in results:
            item = QListWidgetItem(f"📄 {file_path.name}\n   {file_path.parent}")
            item.setData(Qt.ItemDataRole.UserRole, str(file_path))
            self.results_list.addItem(item)
        
        self.status_label.setText(f"Найдено {len(results)} файлов по имени '{search_name}'")
    
    def open_result_file(self, item):
        """Открывает файл из результатов поиска"""
        filepath = item.data(Qt.ItemDataRole.UserRole)
        self.preview_file_content(filepath)
        
        # Также показываем совпадения, если они есть
        matches = item.data(Qt.ItemDataRole.UserRole + 1)
        if matches:
            self.preview_text.append("\n\n=== НАЙДЕННЫЕ СОВПАДЕНИЯ ===\n" + "\n".join(matches))
    
    def browse_directory(self):
        """Открывает диалог выбора папки"""
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Выберите папку", 
            self.current_directory
        )
        
        if directory:
            self.current_directory = directory
            self.path_edit.setText(directory)
            self.load_directory_contents()
            self.back_button.setEnabled(True)
    
    def navigate_to_path(self):
        """Переходит по пути, введённому в строку адреса"""
        new_path = self.path_edit.text().strip()
        path = Path(new_path)
        
        if path.exists() and path.is_dir():
            self.current_directory = str(path)
            self.load_directory_contents()
            self.back_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Ошибка", f"Папка '{new_path}' не существует")
            self.path_edit.setText(self.current_directory)
    
    def go_back(self):
        """Возвращается на предыдущий уровень вверх"""
        parent_path = Path(self.current_directory).parent
        if parent_path != Path(self.current_directory):
            self.current_directory = str(parent_path)
            self.path_edit.setText(self.current_directory)
            self.load_directory_contents()
    
    @staticmethod
    def format_file_size(size_bytes):
        """Форматирует размер файла в человекочитаемый вид"""
        for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} ТБ"


def main():
    app = QApplication(sys.argv)
    window = FileSearchApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()