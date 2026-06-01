import flet as ft
from pathlib import Path


class FileSearchApp:
    def __init__(self):
        self.current_directory = str(Path.home())
        self.search_results = []
    
    def main(self, page: ft.Page):
        """Главная функция приложения"""
        page.title = "Файловый менеджер с поиском"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1200
        page.window_height = 700
        
        # Панель навигации
        self.path_field = ft.TextField(
            value=self.current_directory,
            expand=True,
            hint_text="Введите путь к папке и нажмите Enter"
        )
        self.path_field.on_submit = self.navigate_to_path
        
        # Кнопка "Назад"
        back_button = ft.ElevatedButton(
            "◀ Назад",
            on_click=self.go_back
        )
        
        # Кнопка обновления
        refresh_button = ft.ElevatedButton(
            "🔄 Обновить",
            on_click=lambda e: self.load_directory_contents(e.page)
        )
        
        # Поле для ручного ввода пути
        go_button = ft.ElevatedButton(
            "📁 Перейти",
            on_click=self.navigate_to_path
        )
        
        # Верхняя панель
        top_row = ft.Row(
            [back_button, refresh_button, self.path_field, go_button],
            alignment=ft.MainAxisAlignment.START,
            spacing=10
        )
        
        self.search_field = ft.TextField(
            hint_text="🔍 Введите текст для поиска в файлах...",
            expand=True,
        )
        
        search_button = ft.ElevatedButton(
            "🔍 Поиск в файлах",
            on_click=self.search_in_files
        )
        
        search_name_button = ft.ElevatedButton(
            "📄 Поиск по имени",
            on_click=self.search_by_name
        )
        
        clear_button = ft.ElevatedButton(
            "🗑 Очистить результаты",
            on_click=self.clear_results
        )
        
        search_row = ft.Row(
            [self.search_field, search_button, search_name_button, clear_button],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Список файлов (левая панель)
        self.file_list = ft.ListView(expand=1, spacing=5)
        
        # Результаты поиска (правая панель)
        self.results_list = ft.ListView(expand=1, spacing=5)
        
        # Область предпросмотра
        self.preview_text = ft.TextField(
            multiline=True,
            read_only=True,
            expand=True,
            hint_text="Содержимое файла появится здесь после двойного клика...",
            text_size=12
        )
        
        # Правая колонка
        right_column = ft.Column([
            ft.Text("🔎 Результаты поиска", weight=ft.FontWeight.BOLD),
            ft.Container(height=5),
            self.results_list,
            ft.Divider(),
            ft.Text("📄 Предпросмотр файла", weight=ft.FontWeight.BOLD),
            ft.Container(height=5),
            self.preview_text
        ], expand=True, spacing=5)
        
        # Основная область с двумя колонками
        content_row = ft.Row([
            ft.Column([
                ft.Text("📂 Содержимое папки", weight=ft.FontWeight.BOLD),
                ft.Container(height=5),
                self.file_list
            ], expand=1),
            ft.VerticalDivider(width=1),
            right_column
        ], expand=True, spacing=10)
        
        # Статусная строка
        self.status_text = ft.Text("Готов к работе. Используйте поиск по тексту или имени файла.", italic=True)
        
        # Собираем всё на страницу
        page.add(
            ft.Container(height=10),
            top_row,
            ft.Divider(height=5),
            search_row,
            ft.Divider(height=5),
            content_row,
            ft.Divider(height=5),
            ft.Row([self.status_text])
        )
        
        # Загружаем содержимое текущей папки
        self.load_directory_contents(page)
    
    def navigate_to_path(self, e):
        """Переход по указанному пути"""
        new_path = self.path_field.value.strip()
        if new_path:
            path = Path(new_path)
            if path.exists() and path.is_dir():
                self.current_directory = str(path)
                self.load_directory_contents(e.page)
            else:
                self.status_text.value = f"Ошибка: папка '{new_path}' не существует"
                e.page.update()
    
    def clear_results(self, e):
        """Очищает результаты поиска"""
        self.results_list.controls.clear()
        self.preview_text.value = ""
        self.status_text.value = "Результаты поиска очищены"
        e.page.update()
    
    def load_directory_contents(self, page):
        """Загружает содержимое текущей папки"""
        self.file_list.controls.clear()
        self.path_field.value = self.current_directory
        
        try:
            path = Path(self.current_directory)
            
            # Добавляем ссылку на родительскую папку ".."
            if self.current_directory != str(Path(self.current_directory).root):
                parent_item = ft.ListTile(
                    leading=ft.Text("📁"),
                    title=ft.Text(".."),
                    subtitle=ft.Text("Родительская папка"),
                    on_click=lambda e: self.go_to_parent(page)
                )
                self.file_list.controls.append(parent_item)
            
            folders = []
            files = []
            
            for item in path.iterdir():
                try:
                    if item.is_dir():
                        folders.append(item)
                    else:
                        files.append(item)
                except PermissionError:
                    continue
            
            folders.sort(key=lambda x: x.name.lower())
            files.sort(key=lambda x: x.name.lower())
            
            # Добавляем папки
            for folder in folders:
                self.file_list.controls.append(
                    ft.ListTile(
                        leading=ft.Text("📁"),
                        title=ft.Text(folder.name),
                        subtitle=ft.Text("Папка"),
                        on_click=lambda e, p=folder: self.open_folder(p, page)
                    )
                )
            
            # Добавляем файлы
            for file in files:
                size = file.stat().st_size
                size_str = self.format_file_size(size)
                self.file_list.controls.append(
                    ft.ListTile(
                        leading=ft.Text("📄"),
                        title=ft.Text(file.name),
                        subtitle=ft.Text(f"Файл • {size_str}"),
                        on_click=lambda e, p=file: self.preview_file_content(p, page)
                    )
                )
            
            self.status_text.value = f"Загружено: {len(folders)} папок, {len(files)} файлов в {self.current_directory}"
            
        except PermissionError:
            self.status_text.value = f"Нет доступа к папке: {self.current_directory}"
        except Exception as e:
            self.status_text.value = f"Ошибка: {str(e)}"
        
        page.update()
    
    def go_to_parent(self, page):
        """Переход в родительскую папку"""
        parent_path = Path(self.current_directory).parent
        if parent_path != Path(self.current_directory):
            self.current_directory = str(parent_path)
            self.load_directory_contents(page)
    
    def open_folder(self, folder_path, page):
        """Открывает папку"""
        self.current_directory = str(folder_path)
        self.load_directory_contents(page)
    
    def preview_file_content(self, filepath, page):
        """Показывает содержимое файла"""
        text_extensions = {'.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.md', '.csv', '.log', '.ini', '.cfg'}
        
        if filepath.suffix.lower() in text_extensions:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if len(content) > 20000:
                        content = content[:20000] + "\n\n... (файл обрезан, показано 20000 символов)"
                    self.preview_text.value = content
                    self.status_text.value = f"Просмотр: {filepath.name} ({self.format_file_size(filepath.stat().st_size)})"
            except Exception as e:
                self.preview_text.value = f"Ошибка чтения файла: {str(e)}"
                self.status_text.value = f"Не удалось прочитать {filepath.name}"
        else:
            self.preview_text.value = f"[Бинарный файл]\n\nИмя: {filepath.name}\nРазмер: {self.format_file_size(filepath.stat().st_size)}\n\nНевозможно отобразить содержимое бинарного файла."
            self.status_text.value = f"Бинарный файл: {filepath.name}"
        
        page.update()
    
    def search_in_files(self, e):
        """Поиск текста в файлах"""
        search_text = self.search_field.value.strip()
        
        if not search_text:
            self.status_text.value = "Введите текст для поиска"
            e.page.update()
            return
        
        self.results_list.controls.clear()
        self.preview_text.value = ""
        self.status_text.value = f"Поиск текста '{search_text}' в папке {self.current_directory}..."
        e.page.update()
        
        root_path = Path(self.current_directory)
        results = []
        file_count = 0
        scanned_count = 0
        
        text_extensions = {'.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.md', '.csv', '.log', '.ini', '.cfg'}
        
        # Рекурсивный поиск
        for file_path in root_path.rglob("*"):
            if file_path.is_file():
                file_count += 1
                
                # Обновляем статус каждые 20 файлов
                if file_count % 20 == 0:
                    self.status_text.value = f"Поиск... проверено {file_count} файлов"
                    e.page.update()
                
                # Проверяем только текстовые файлы
                if file_path.suffix.lower() in text_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read(50000)  # Читаем первые 50KB для скорости
                            if search_text.lower() in content.lower():
                                # Находим строку с совпадением
                                lines = content.split('\n')
                                found_lines = []
                                for i, line in enumerate(lines[:10]):  # Берём первые 10 строк
                                    if search_text.lower() in line.lower():
                                        found_lines.append(f"Строка {i+1}: {line[:80]}")
                                
                                results.append((file_path, found_lines[:3]))  # Первые 3 совпадения
                                scanned_count += 1
                    except:
                        pass
        
        # Отображаем результаты
        if results:
            for file_path, matches in results:
                match_text = "\n".join(matches) if matches else "Совпадения найдены"
                self.results_list.controls.append(
                    ft.ListTile(
                        leading=ft.Text("📄"),
                        title=ft.Text(file_path.name, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"{file_path.parent}\n{self.format_file_size(file_path.stat().st_size)} • {len(matches)} совпадений"),
                        on_click=lambda e, p=file_path: self.preview_file_content(p, e.page)
                    )
                )
            
            self.status_text.value = f"✅ Найдено {len(results)} файлов с текстом '{search_text}' (проверено {file_count} файлов)"
        else:
            self.status_text.value = f"❌ Текст '{search_text}' не найден (проверено {file_count} файлов)"
        
        e.page.update()
    
    def search_by_name(self, e):
        """Поиск файлов по имени"""
        search_name = self.search_field.value.strip()
        
        if not search_name:
            self.status_text.value = "Введите имя файла для поиска"
            e.page.update()
            return
        
        self.results_list.controls.clear()
        self.preview_text.value = ""
        self.status_text.value = f"Поиск файлов по имени '{search_name}' в папке {self.current_directory}..."
        e.page.update()
        
        root_path = Path(self.current_directory)
        results = []
        
        # Рекурсивный поиск по шаблону
        pattern = f"*{search_name}*"
        for file_path in root_path.rglob(pattern):
            if file_path.is_file():
                results.append(file_path)
        
        # Отображаем результаты
        if results:
            for file_path in results:
                self.results_list.controls.append(
                    ft.ListTile(
                        leading=ft.Text("📄"),
                        title=ft.Text(file_path.name, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"{file_path.parent}\n{self.format_file_size(file_path.stat().st_size)}"),
                        on_click=lambda e, p=file_path: self.preview_file_content(p, e.page)
                    )
                )
            
            self.status_text.value = f"✅ Найдено {len(results)} файлов по имени '{search_name}'"
        else:
            self.status_text.value = f"❌ Файлы с именем '{search_name}' не найдены"
        
        e.page.update()
    
    def go_back(self, e):
        """Возврат на уровень выше"""
        parent_path = Path(self.current_directory).parent
        if parent_path != Path(self.current_directory):
            self.current_directory = str(parent_path)
            self.load_directory_contents(e.page)
    
    @staticmethod
    def format_file_size(size_bytes):
        """Форматирует размер файла в человекочитаемый вид"""
        if size_bytes == 0:
            return "0 Б"
        
        size_names = ["Б", "КБ", "МБ", "ГБ", "ТБ"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"


# Запуск приложения
if __name__ == "__main__":
    app = FileSearchApp()
    ft.app(target=app.main)
