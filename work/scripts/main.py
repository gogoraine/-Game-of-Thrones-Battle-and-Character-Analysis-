"""
Главный модуль приложения "Анализ битв и персонажей 'Игры престолов'".

Автор: Давыдов Д.О.
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from work.library.utils import (load_settings, init_dataframes,
                                save_dataframes_pickle)
from gui import (
    create_characters_tab, create_battles_tab,
    add_character, edit_character, delete_character,
    add_battle, edit_battle, delete_battle,
    refresh_table, open_settings_window
)
from reports import (
    generate_simple_report, generate_stat_report, generate_pivot_report,
    generate_clustered_bar_chart, generate_categorized_histogram,
    generate_boxplot, generate_scatter_plot
)

current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(base_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


def main():
    """
    Главная функция запуска приложения.

    Описание:
        Загружает настройки интерфейса, инициализирует данные.
        Создаёт главное окно Tkinter, вкладки, меню, и запускает mainloop.

    Входные параметры: нет.

    Возвращаемый объект: нет.

    Автор: Давыдов Д.О.
    """
    # Пути к файлам и папкам
    settings_path = os.path.join(current_dir, "settings.ini")
    datasets_dir = os.path.join(base_dir, "datasets")
    data_dir = os.path.join(base_dir, "data")

    battles_csv = os.path.join(datasets_dir, "battles.csv")
    characters_csv = os.path.join(datasets_dir, "character-predictions.csv")

    # Загрузка настроек интерфейса
    settings = load_settings(settings_path)

    # Инициализация данных
    try:
        df_characters, df_battles = init_dataframes(
            battles_csv, characters_csv, data_dir, target_battles=100
        )
    except Exception as e:
        root_err = tk.Tk()
        root_err.withdraw()
        messagebox.showerror("Критическая ошибка",
                             f"Не удалось загрузить данные:\n{e}")
        return

    data = {'char': df_characters, 'batt': df_battles}

    # Главное окно
    root = tk.Tk()
    root.title("Приложение: Игра Престолов")
    root.geometry("1000x650")
    root.configure(bg=settings["bg_color"])

    style = ttk.Style()
    style.configure("Treeview.Heading",
                    font=(settings["font_family"],
                          settings["font_size"], "bold"))
    style.configure("Treeview",
                    font=(settings["font_family"],
                          settings["font_size"]), rowheight=25)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Вкладка Персонажи
    char_frame = tk.Frame(notebook, bg=settings["bg_color"])

    def add_char():
        data['char'] = add_character(root, data['char'], char_tree, settings)
        refresh_table(char_tree, data['char'])

    def edit_char():
        data['char'] = edit_character(root, data['char'], char_tree, settings)
        refresh_table(char_tree, data['char'])

    def del_char():
        data['char'] = delete_character(data['char'], char_tree)
        refresh_table(char_tree, data['char'])

    char_tree = create_characters_tab(char_frame,
                                      settings, add_char,
                                      edit_char, del_char)
    refresh_table(char_tree, data['char'])
    notebook.add(char_frame, text=" Персонажи ")

    # Вкладки Сражения
    battle_frame = tk.Frame(notebook, bg=settings["bg_color"])

    def add_batt():
        data['batt'] = add_battle(root, data['batt'], battle_tree, settings)
        refresh_table(battle_tree, data['batt'])

    def edit_batt():
        data['batt'] = edit_battle(root, data['batt'], battle_tree, settings)
        refresh_table(battle_tree, data['batt'])

    def del_batt():
        data['batt'] = delete_battle(data['batt'], battle_tree)
        refresh_table(battle_tree,
                      data['batt'])

    battle_tree = create_battles_tab(battle_frame,
                                     settings, add_batt,
                                     edit_batt, del_batt)
    refresh_table(battle_tree, data['batt'])
    notebook.add(battle_frame, text=" Сражения ")

    # Главное меню
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Файл
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(
        label="Сохранить БД",
        command=lambda: save_dataframes_pickle(data['char'],
                                               data['batt'], data_dir)
    )
    file_menu.add_separator()
    file_menu.add_command(label="Выход", command=root.quit)
    menubar.add_cascade(label="Файл", menu=file_menu)

    # Текстовые отчёты
    report_menu = tk.Menu(menubar, tearoff=0)
    report_menu.add_command(
        label="Простой текстовый отчет",
        command=lambda: generate_simple_report(data['char'])
    )
    report_menu.add_command(
        label="Статистический отчет",
        command=lambda: generate_stat_report(data['char'])
    )
    report_menu.add_command(
        label="Сводная таблица",
        command=lambda: generate_pivot_report(data['char'])
    )
    menubar.add_cascade(label="Текстовые отчеты", menu=report_menu)

    # Графические отчёты
    graph_menu = tk.Menu(menubar, tearoff=0)
    graph_menu.add_command(
        label="1. Дом — Статус (Столбчатая)",
        command=lambda: generate_clustered_bar_chart(data['char'])
    )
    graph_menu.add_command(
        label="2. Возраст — Пол (Гистограмма)",
        command=lambda: generate_categorized_histogram(data['char'])
    )
    graph_menu.add_command(
        label="3. Возраст — Дом (Boxplot)",
        command=lambda: generate_boxplot(data['char'])
    )
    graph_menu.add_command(
        label="4. Хронология битв (Scatter Plot)",
        command=lambda: generate_scatter_plot(data['batt'])
    )
    menubar.add_cascade(label="Графические отчеты", menu=graph_menu)

    # Настройки интерфейса
    def apply_settings(new_settings):
        settings.update(new_settings)
        root.configure(bg=settings["bg_color"])
        style.configure("Treeview.Heading",
                        font=(settings["font_family"],
                              settings["font_size"], "bold"))
        style.configure("Treeview",
                        font=(settings["font_family"],
                              settings["font_size"]),
                        rowheight=25)
        for tab_id in notebook.tabs():
            child = notebook.nametowidget(tab_id)
            if isinstance(child, tk.Frame):
                child.configure(bg=settings["bg_color"])

    settings_menu = tk.Menu(menubar, tearoff=0)
    settings_menu.add_command(
        label="Параметры интерфейса",
        command=lambda: open_settings_window(root,
                                             settings,
                                             apply_settings,
                                             settings_path)
    )
    menubar.add_cascade(label="Настройки", menu=settings_menu)

    root.mainloop()


if __name__ == "__main__":
    main()
