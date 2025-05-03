from PyQt5.QtWidgets import *
import json

app = QApplication([])

# Загружаем заметки из файла, если он существует
try:
    with open('notes_data.json', 'r', encoding='utf-8') as file:
        notes = json.load(file)
except FileNotFoundError:
    notes = {
        'Добро пожаловать!': {
            'текст': 'Это топ приложение для заметок!',
            'теги': ['заметки', 'программа']
        }
    }

# Окно приложения
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(1300, 700)

# Список заметок
list_notes_label = QLabel('Список заметок')
list_notes = QListWidget()

# Кнопки заметок
button_note_create = QPushButton("Создать заметку")
button_note_del = QPushButton("Удалить заметку")
button_note_save = QPushButton("Сохранить заметку")

# Список тегов
list_tags_label = QLabel('Список тегов')
list_tags = QListWidget()
field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег ...')

# Кнопки тегов
button_tags_add = QPushButton("Добавить тег")
button_tags_del = QPushButton("Удалить тег")
button_tags_search = QPushButton("Искать заметку по тегу")
button_reset_search = QPushButton("Сбросить поиск")

# Область текста заметки
field_text = QTextEdit()

# Лайауты
layout_notes = QHBoxLayout()

col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)

row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tags_add)
row_3.addWidget(button_tags_del)

row_4 = QHBoxLayout()
row_4.addWidget(button_tags_search)

row_5 = QHBoxLayout()
row_5.addWidget(button_reset_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)
col_2.addLayout(row_5)

layout_notes.addLayout(col_1, stretch=3)
layout_notes.addLayout(col_2, stretch=2)

notes_win.setLayout(layout_notes)

def save_notes_to_file():
    with open('notes_data.json', 'w', encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False)  # Сохраняем заметки в файл

def show_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        field_text.setText(notes[name]['текст'])
        list_tags.clear()
        list_tags.addItems(notes[name]['теги'])

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить заметку', 'Название заметки:')
    if ok and note_name != '':
        notes[note_name] = {'текст': '', 'теги': []}  # Добавляем заметку в словарь
        list_notes.addItem(note_name)  # Добавляем заметку в QListWidget
        field_text.clear()  # Очищаем текстовое поле
        list_tags.clear()  # Очищаем список тегов
        save_notes_to_file()  # Сохраняем изменения в файл
        print('Заметка добавлена\n', notes)

def del_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        del notes[name]  # Удаляем заметку из словаря
        list_notes.clear()  # Очищаем список заметок
        list_tags.clear()  # Очищаем список тегов
        field_text.clear()  # Очищаем текстовое поле
        list_notes.addItems(notes.keys())  # Добавляем оставшиеся заметки в QListWidget
        save_notes_to_file()  # Сохраняем изменения в файл
        print(notes)
    else:
        print('Заметка для удаления не выбрана!')

def save_note():
    if list_notes.selectedItems():
        name = list_notes.selectedItems()[0].text()
        notes[name]['текст'] = field_text.toPlainText()  #

def add_tag():
    if list_notes.selectedItems() and field_tag.text():
        name = list_notes.selectedItems()[0].text()  # Получаем название выбранной заметки
        tag = field_tag.text()  # Получаем текст тега из поля ввода
        if tag and tag not in notes[name]['теги']:  # Проверяем, есть ли уже этот тег
            notes[name]['теги'].append(tag)  # Добавляем тег к заметке
            list_tags.addItem(tag)  # Отображаем тег в списке тегов
            field_tag.clear()  # Очищаем поле ввода тега
            save_notes_to_file()  # Сохраняем изменения в файл


def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems():
        name = list_notes.selectedItems()[0].text()  # Получаем название выбранной заметки
        tag = list_tags.selectedItems()[0].text()  # Получаем выбранный тег
        notes[name]['теги'].remove(tag)  # Удаляем тег из заметки
        list_tags.takeItem(list_tags.row(list_tags.selectedItems()[0]))  # Удаляем тег из списка
        save_notes_to_file()  # Сохраняем изменения в файл

def search_note_by_tag():
    tag = field_tag.text()  # Получаем текст тега из поля ввода
    filtered_notes = [name for name, data in notes.items() if tag in data['теги']]  # Фильтруем заметки по тегу
    list_notes.clear()  # Очищаем список заметок
    if filtered_notes:
        list_notes.addItems(filtered_notes)  # Отображаем только заметки с указанным тегом
    else:
        list_notes.addItems(notes.keys())  # Если нет совпадений, отображаем все заметки
    field_tag.clear()  # Очищаем поле ввода тега

def reset_search():
    list_notes.clear()  # Очищаем список заметок
    list_notes.addItems(notes.keys())  # Отображаем все заметки
    field_tag.clear()  # Очищаем поле ввода тега

# Подключаем кнопку "Сбросить поиск" к функции
button_reset_search.clicked.connect(reset_search)
button_note_create.clicked.connect(add_note)
button_note_del.clicked.connect(del_note)
button_note_save.clicked.connect(save_note)
button_tags_add.clicked.connect(add_tag)
button_tags_del.clicked.connect(del_tag)
button_tags_search.clicked.connect(search_note_by_tag)

list_notes.itemClicked.connect(show_note)

notes_win.show()

with open('notes_data.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)

list_notes.addItems(notes.keys()) 


app.exec()