"""Модуль графического интерфейса: вкладки и обработки действий пользователя.

Автор: Давыдов Д.О.
"""
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import tkinter.font as tkfont
import pandas as pd
from forms import create_character_form, create_battle_form
from library.utils import save_settings


def refresh_table(tree, dataframe):
    """
    Обновляет содержимое таблицы на основе переданного DataFrame.

    Описание:
        Удаляет все старые строки и вставляет новые из dataframe.
    Входные параметры:
        tree (ttk.Treeview) - виджет таблицы.
        dataframe (pd.DataFrame) - данные для отображения.
    Возвращаемый объект: Нет.
    Автор: Давыдов Д.О.
    """
    # Обновляет содержимое таблицы после
    # каждого изменения справочника
    # (добавление, удаление, изменение)
    # с последующим отображением в графическом интерфейсе
    for item in tree.get_children():
        tree.delete(item)
    for _, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))


def delete_character(df_characters, char_tree):
    """
    Удаляет выбранного персонажа из DataFrame и обновляет таблицу.

    Описание:
        Удаляет выбранного персонажа из DataFrame и обновляет таблицу.
    Входные параметры:
        df_characters (pd.DataFrame) - текущий DataFrame.
        char_tree (ttk.Treeview) - таблица.
    Возвращаемый объект:
        pd.DataFrame - DataFrame без удалённой записи.
    Автор: Давыдов Д.О.
    """
    selected = char_tree.selection()
    if not selected:
        messagebox.showwarning("Внимание",
                               "Выберите строку"
                               " для удаления!")
        return df_characters
    # Получение строки из графического интерфейса
    record_id = int(char_tree.item(selected[0], "values")[0])
    if messagebox.askyesno("Подтверждение",
                           f"Удалить персонажа с ID {record_id}?"):
        # Удаление строки
        df_characters = df_characters[df_characters["id"] != record_id]
        # Обновление справочника
        refresh_table(char_tree, df_characters)
    return df_characters


def add_character(root, df_characters, char_tree, settings):
    """
    Добавляет нового персонажа через диалоговое окно.

    Описание:
        Открывает форму, при сохранении
        создаёт новый id и добавляет строку в DataFrame.
    Входные параметры:
        root (tk.Tk) - главное окно.
        df_characters (pd.DataFrame) - текущий DataFrame персонажей.
        char_tree (ttk.Treeview) - виджет таблицы персонажей.
        settings (dict) - настройки интерфейса.
    Возвращаемый объект:
        pd.DataFrame - обновлённый DataFrame персонажей.
    Автор: Давыдов Д.О.
    """
    df_container = [df_characters]
    # Изменяемый контейнер создан, чтобы его можно было передать в функцию
    # on_save, своего рода передача массива по
    # указателю, иначе бы в функции создалась локальная версия

    def on_save(data):
        if data["id"] is None:
            new_id = df_container[0]["id"].max() + 1 \
                if len(df_container[0]) > 0 else 1
            new_row = pd.DataFrame([{**data, "id": new_id}])
            df_container[0] = pd.concat([df_container[0], new_row],
                                        ignore_index=True)
        else:
            idx = df_container[0][df_container[0]["id"] == data["id"]].index[0]
            for k, v in data.items():
                if k != "id":
                    df_container[0].loc[idx, k] = v
        refresh_table(char_tree, df_container[0])

    create_character_form(root, "Добавить персонажа", settings, on_save)
    return df_container[0]


def edit_character(root, df_characters, char_tree, settings):
    """
    Редактирует выбранного персонажа через диалоговое окно.

    Описание:
        Получает выделенную строку, открывает форму с предзаполненными данными,
        при сохранении обновляет DataFrame.
    Входные параметры:
        root (tk.Tk) - главное окно.
        df_characters (pd.DataFrame) - текущий DataFrame.
        char_tree (ttk.Treeview) - таблица.
        settings (dict) - настройки.
    Возвращаемый объект:
        pd.DataFrame - обновлённый DataFrame
        (или исходный, если ничего не выбрано).
    Автор: Давыдов Д.О.
    """
    selected = char_tree.selection()
    if not selected:
        messagebox.showwarning("Внимание", "Выберите персонажа!")
        return df_characters

    values = char_tree.item(selected[0], "values")
    # Здесь мы просто меняем значение в справочнике,
    # не меняя ссылку на него

    def on_save(data):
        idx = df_characters[df_characters["id"] == int(data["id"])].index[0]
        for k, v in data.items():
            if k != "id":
                df_characters.loc[idx, k] = v
        refresh_table(char_tree, df_characters)

    create_character_form(root,
                          "Редактировать персонажа",
                          settings,
                          on_save,
                          character_data=values)
    return df_characters


def add_battle(root, df_battles, battle_tree, settings):
    """
    Добавляет новое сражение через диалоговое окно.

    Описание:
        Добавление нового сражения (аналогично add_character).
    Входные параметры:
        root (tk.Tk) - главное окно.
        df_battles (pd.DataFrame) - текущий DataFrame сражений.
        battle_tree (ttk.Treeview) - таблица сражений.
        settings (dict) - настройки интерфейса.
    Возвращаемый объект:
        pd.DataFrame - обновлённый DataFrame сражений.
    Автор: Давыдов Д.О.
    """
    df_container = [df_battles]

    def on_save(data):
        if data["id"] is None:
            new_id = df_container[0]["id"].max() + 1 \
                if len(df_container[0]) > 0 else 1
            new_row = pd.DataFrame([{**data, "id": new_id}])
            df_container[0] = pd.concat([df_container[0],
                                         new_row],
                                        ignore_index=True)
        else:
            idx = df_container[0][df_container[0]["id"] == data["id"]].index[0]
            for k, v in data.items():
                if k != "id":
                    df_container[0].loc[idx, k] = v
        refresh_table(battle_tree, df_container[0])

    create_battle_form(root, "Добавить сражение", settings, on_save)
    return df_container[0]


def edit_battle(root, df_battles, battle_tree, settings):
    """
    Редактирует выбранное сражение через диалоговое окно.

    Описание:
        Редактирование выбранного сражения (аналогично edit_character).
    Входные параметры:
        root (tk.Tk) - главное окно.
        df_battles (pd.DataFrame) - текущий DataFrame сражений.
        battle_tree (ttk.Treeview) - таблица сражений.
        settings (dict) - настройки.
    Возвращаемый объект:
        pd.DataFrame - обновлённый DataFrame сражений.
    Автор: Давыдов Д.О.
    """
    selected = battle_tree.selection()
    if not selected:
        messagebox.showwarning("Внимание", "Выберите сражение!")
        return df_battles

    values = battle_tree.item(selected[0], "values")

    def on_save(data):
        idx = df_battles[df_battles["id"] == int(data["id"])].index[0]
        for k, v in data.items():
            if k != "id":
                df_battles.loc[idx, k] = v
        refresh_table(battle_tree, df_battles)

    create_battle_form(root,
                       "Редактировать сражение",
                       settings,
                       on_save,
                       battle_data=values)
    return df_battles


def delete_battle(df_battles, battle_tree):
    """
    Удаляет выбранное сражение из DataFrame и обновляет таблицу.

    Описание:
        Удаление выбранного сражения (аналогично delete_character).
    Входные параметры:
        df_battles (pd.DataFrame) - текущий DataFrame сражений.
        battle_tree (ttk.Treeview) - таблица сражений.
    Возвращаемый объект:
        pd.DataFrame - DataFrame без удалённой записи.
    Автор: Давыдов Д.О.
    """
    selected = battle_tree.selection()
    if not selected:
        messagebox.showwarning("Внимание", "Выберите строку!")
        return df_battles

    record_id = int(battle_tree.item(selected[0], "values")[0])
    if messagebox.askyesno("Подтверждение",
                           f"Удалить сражение "
                           f"с ID {record_id}?"):
        df_battles = df_battles[df_battles["id"] != record_id]
        refresh_table(battle_tree, df_battles)
    return df_battles


def create_characters_tab(parent, settings, add_cmd, edit_cmd, del_cmd):
    """
    Создаёт вкладку с таблицей персонажей.

    Описание:
        Создаёт панель инструментов и таблицу для вкладки "Персонажи".
        Возвращает объект Treeview для дальнейшего обновления.
    Входные параметры:
        parent (tk.Frame) - родительский фрейм.
        settings (dict) - настройки оформления.
        add_cmd, edit_cmd, del_cmd (callable) - команды для кнопок.
    Возвращаемый объект:
        ttk.Treeview - созданная таблица.
    Автор: Давыдов Д.О.
    """
    # Создаем в отцовском фрейме фрейм для кнопок
    toolbar = tk.Frame(parent, bg=settings["bg_color"])
    toolbar.pack(side="top", fill="x", pady=5)

    # Создаем кнопки
    tk.Button(toolbar,
              text="Добавить",
              font=(settings["font_family"],
                    settings["font_size"]),
              bg="#d4edda",
              command=add_cmd).pack(side="left", padx=5)

    tk.Button(toolbar,
              text="Редактировать",
              font=(settings["font_family"],
                    settings["font_size"]),
              bg=settings["btn_color"],
              command=edit_cmd).pack(side="left", padx=5)

    tk.Button(toolbar,
              text="Удалить",
              font=(settings["font_family"],
                    settings["font_size"]),
              bg="#f8d7da",
              command=del_cmd).pack(side="left", padx=5)

    columns = ["id", "имя", "дом", "культура", "пол", "возраст", "жив/мертв"]
    # Создаем таблицу в старшем фрейме
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    # Заполняем ее
    for col in columns:
        tree.heading(col, text=col.upper())
        tree.column(col, width=110, anchor="center")
    # Создаем скролл для ориентации по таблице
    scrollbar = ttk.Scrollbar(parent,
                              orient="vertical",
                              command=tree.yview)
    # Собираем его
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", expand=True, fill="both")
    scrollbar.pack(side="right", fill="y")
    return tree


def create_battles_tab(parent, settings,
                       add_cmd, edit_cmd, del_cmd):
    """
    Создаёт вкладку с таблицей сражений.

    Описание:
        Создаёт панель инструментов и
        таблицу для вкладки "Сражения".
    Входные параметры:
        parent (tk.Frame) - родительский фрейм.
        settings (dict) - настройки оформления.
        add_cmd, edit_cmd, del_cmd (callable)
        - команды для кнопок.
    Возвращаемый объект:
        ttk.Treeview - созданная таблица.
    Автор: Давыдов Д.О.
    """
    toolbar = tk.Frame(parent, bg=settings["bg_color"])
    toolbar.pack(side="top", fill="x", pady=5)

    tk.Button(toolbar,
              text="Добавить",
              font=(settings["font_family"],
                    settings["font_size"]),
              bg="#d4edda",
              command=add_cmd).pack(side="left", padx=5)

    tk.Button(toolbar,
              text="Редактировать",
              font=(settings["font_family"],
                    settings["font_size"]),
              bg=settings["btn_color"],
              command=edit_cmd).pack(side="left", padx=5)

    tk.Button(toolbar,
              text="Удалить",
              font=(settings["font_family"],
                    settings["font_size"]),
              bg="#f8d7da",
              command=del_cmd).pack(side="left", padx=5)

    columns = ["id", "название", "регион",
               "атакующая сторона",
               "обороняющая сторона", "год", "победитель"]
    tree = ttk.Treeview(parent,
                        columns=columns,
                        show="headings")
    for col in columns:
        tree.heading(col, text=col.upper())
        tree.column(col, width=110, anchor="center")

    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", expand=True, fill="both")
    scrollbar.pack(side="right", fill="y")
    return tree


def open_settings_window(root, settings_dict, on_save_callback, ini_path):
    """
    Открывает окно настройки цветов и шрифтов.

    Описание:
        Открывает окно настройки цветов и шрифтов.
        Позволяет выбрать цвет фона, шрифт и его размер.
        Сохраняет изменения в settings.ini
        и вызывает on_save_callback для частичного обновления.
    Входные параметры:
        root (tk.Tk) - главное окно.
        settings_dict (dict) - текущий словарь настроек.
        on_save_callback (callable) - функция, принимающая новые настройки.
        ini_path (str) - путь к файлу settings.ini.
    Возвращаемый объект: Нет.
    Автор: Давыдов Д.О.
    """
    win = tk.Toplevel(root)
    win.title("Настройки интерфейса")
    win.geometry("550x400")
    win.resizable(False, False)
    win.grab_set()

    bg_color_var = tk.StringVar(value=settings_dict["bg_color"])
    font_family_var = tk.StringVar(value=settings_dict["font_family"])
    font_size_var = tk.IntVar(value=settings_dict["font_size"])

    preview_frame = tk.Frame(win, bg=bg_color_var.get(), padx=20, pady=20)
    preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

    preview_label = None
    # Меню выбора цвета

    def choose_bg_color():
        color = colorchooser.askcolor(title="Выберите цвет фона",
                                      initialcolor=bg_color_var.get())
        if color[1]:
            bg_color_var.set(color[1])
            preview_frame.configure(bg=bg_color_var.get())
            if preview_label:
                preview_label.configure(bg=bg_color_var.get())

    # Меню выбора шрифта
    def update_preview_font(*args):
        family = font_family_var.get()
        size = font_size_var.get()
        try:
            if preview_label:
                preview_label.configure(font=(family, size))
        except Exception:
            pass

    font_family_var.trace_add('write', update_preview_font)
    font_size_var.trace_add('write', update_preview_font)

    # Кнопки, текст меню settings
    tk.Label(preview_frame,
             text="Фон главного окна",
             bg=bg_color_var.get(),
             fg="black")\
        .grid(row=0, column=0, sticky="w", padx=5, pady=5)

    tk.Button(preview_frame,
              text="Выбрать цвет фона",
              command=choose_bg_color)\
        .grid(row=0, column=1, padx=5, pady=5)

    tk.Label(preview_frame, text="Шрифт",
             bg=bg_color_var.get(),
             fg="black")\
        .grid(row=1, column=0, sticky="w", padx=5, pady=5)

    fonts = list(tkfont.families())

    font_combo = ttk.Combobox(preview_frame,
                              values=fonts,
                              textvariable=font_family_var,
                              width=25)

    font_combo.grid(row=1,
                    column=1,
                    padx=5,
                    pady=5,
                    sticky="w")

    tk.Label(preview_frame,
             text="Размер шрифта",
             bg=bg_color_var.get(),
             fg="black")\
        .grid(row=2, column=0, sticky="w", padx=5, pady=5)

    size_spin = tk.Spinbox(preview_frame,
                           from_=8,
                           to=24,
                           textvariable=font_size_var,
                           width=5)

    size_spin.grid(row=2,
                   column=1,
                   padx=5,
                   pady=5,
                   sticky="w")

    preview_label = tk.Label(preview_frame,
                             text="Пример текста (шрифт изменится)",
                             bg=bg_color_var.get(),
                             fg="black")

    preview_label.grid(row=3, column=0, columnspan=2, pady=10)
    # Сохранение изменений внешнего вида интерфейса

    def save_and_close():
        new_settings = {
            "bg_color": bg_color_var.get(),
            "btn_color": settings_dict.get("btn_color", "#e1e1e1"),
            "font_family": font_family_var.get(),
            "font_size": font_size_var.get()
        }
        try:
            save_settings(new_settings, ini_path)
            settings_dict.update(new_settings)
            on_save_callback(new_settings)
            messagebox.showinfo("Настройки",
                                "Настройки сохранены "
                                "и применены.")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось "
                                 f"сохранить настройки:\n{e}")

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame,
              text="Сохранить",
              command=save_and_close,
              bg="#4CAF50",
              fg="white",
              padx=10)\
        .pack(side="left", padx=10)

    tk.Button(btn_frame,
              text="Отмена",
              command=win.destroy,
              bg="#f44336",
              fg="white",
              padx=10)\
        .pack(side="left")
