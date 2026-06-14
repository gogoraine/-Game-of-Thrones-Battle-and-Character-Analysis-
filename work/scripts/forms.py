"""
Модуль диалоговых окон для добавления/редактирования записей справочников.

Автор: Давыдов Д.О.
"""
import tkinter as tk
from tkinter import ttk, messagebox


def create_character_form(parent, title, settings,
                          on_save_callback,
                          character_data=None):
    """
    Создаёт окно для ввода/редактирования данных персонажа.

    Описание:
        Создаёт окно для ввода/редактирования данных персонажа.
        Окно содержит поля: имя, дом, культура, пол, возраст, статус.
        Выполняет валидацию возраста и обязательность имени.
    Входные параметры:
        parent (tk.Tk/tk.Toplevel) - родительское окно.
        title (str) - заголовок окна.
        settings (dict) - настройки шрифтов/цветов.
        on_save_callback (callable) -
        функция, принимающая словарь данных при сохранении.
        character_data (tuple, optional) -
        кортеж (id, имя, дом, культура, пол, возраст, статус)
        для режима редактирования.
    Возвращаемый объект: Нет.
    """
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("460x400")
    dialog.resizable(False, False)
    dialog.grab_set()

    main_frame = ttk.LabelFrame(dialog, text=" Данные персонажа ", padding=15)
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)

    # Переменные для полей ввода
    name_var = tk.StringVar()
    house_var = tk.StringVar()
    culture_var = tk.StringVar()
    gender_var = tk.StringVar(value="Муж")
    age_var = tk.StringVar(value="0")
    status_var = tk.StringVar(value="Жив")

    # Заполнение, если редактирование
    if character_data:
        name_var.set(character_data[1])
        house_var.set(character_data[2])
        culture_var.set(character_data[3])
        gender_var.set(character_data[4])
        age_var.set(str(character_data[5]))
        status_var.set(character_data[6])

    # Поля ввода
    label = ttk.Label(main_frame, text="Имя персонажа:")
    label.grid(row=0, column=0, sticky="w", pady=6)

    entry_name = ttk.Entry(main_frame, textvariable=name_var, width=30)
    entry_name.grid(row=0, column=1, pady=6, padx=10, sticky="w")

    label_house = ttk.Label(main_frame, text="Великий Дом:")
    label_house.grid(row=1, column=0, sticky="w", pady=6)

    entry_house = ttk.Entry(main_frame, textvariable=house_var, width=30)
    entry_house.grid(row=1, column=1, pady=6, padx=10, sticky="w")

    label_culture = ttk.Label(main_frame, text="Культура:")
    label_culture.grid(row=2, column=0, sticky="w", pady=6)

    entry_culture = ttk.Entry(main_frame, textvariable=culture_var, width=30)
    entry_culture.grid(row=2, column=1, pady=6, padx=10, sticky="w")

    label_gender = ttk.Label(main_frame, text="Пол персонажа:")
    label_gender.grid(row=3, column=0, sticky="w", pady=6)

    combo_gender = ttk.Combobox(
        main_frame,
        values=["Муж", "Жен"],
        state="readonly",
        textvariable=gender_var,
        width=28
    )
    combo_gender.grid(row=3, column=1, pady=6, padx=10, sticky="w")

    label_age = ttk.Label(main_frame, text="Полных лет (возраст):")
    label_age.grid(row=4, column=0, sticky="w", pady=6)

    spin_age = tk.Spinbox(
        main_frame,
        from_=0,
        to=150,
        width=10,
        textvariable=age_var,
        font=(settings["font_family"], settings["font_size"])
    )
    spin_age.grid(row=4, column=1, pady=6, padx=10, sticky="w")

    label_status = ttk.Label(main_frame, text="Текущий статус:")
    label_status.grid(row=5, column=0, sticky="w", pady=6)

    combo_status = ttk.Combobox(
        main_frame,
        values=["Жив", "Мертв"],
        state="readonly",
        textvariable=status_var,
        width=28
    )
    combo_status.grid(row=5, column=1, pady=6, padx=10, sticky="w")

    def save():
        """Обработчик сохранения: валидация и вызов колбэка."""
        name = name_var.get().strip()
        if not name:
            messagebox.showwarning("Валидация",
                                   "Поле 'Имя персонажа' обязательно!")
            return
        try:
            age = int(age_var.get())
            if age < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка",
                                 "Возраст должен быть "
                                 "целым неотрицательным числом!")
            return

        data = {
            "id": character_data[0] if character_data else None,
            "имя": name,
            "дом": house_var.get().strip(),
            "культура": culture_var.get().strip(),
            "пол": gender_var.get(),
            "возраст": age,
            "жив/мертв": status_var.get()
        }
        on_save_callback(data)
        dialog.destroy()

    btn_frame = ttk.Frame(main_frame)
    btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

    ttk.Button(btn_frame,
               text="Сохранить",
               command=save).pack(side="left", padx=10)

    ttk.Button(btn_frame,
               text="Отмена",
               command=dialog.destroy).pack(side="left", padx=10)


def create_battle_form(parent, title, settings,
                       on_save_callback, battle_data=None):
    """
    Создаёт окно для ввода/редактирования данных о сражении.

    Описание:
        Создаёт окно для ввода/редактирования данных о сражении.
        Поля: название, регион, атакующая сторона,
        обороняющая сторона, год, победитель.
    Входные параметры:
        parent (tk.Tk/tk.Toplevel) - родительское окно.
        title (str) - заголовок окна.
        settings (dict) - настройки шрифтов.
        on_save_callback (callable) -
        функция, принимающая словарь данных.
        battle_data (tuple, optional) -
        данные редактируемой записи.
    Возвращаемый объект: Нет.
    """
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("460x400")
    dialog.resizable(False, False)
    dialog.grab_set()

    main_frame = ttk.LabelFrame(dialog,
                                text=" Параметры сражения ",
                                padding=15)
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)

    name_var = tk.StringVar()
    region_var = tk.StringVar()
    attacker_var = tk.StringVar()
    defender_var = tk.StringVar()
    year_var = tk.StringVar(value="298")
    winner_var = tk.StringVar()

    if battle_data:
        name_var.set(battle_data[1])
        region_var.set(battle_data[2])
        attacker_var.set(battle_data[3])
        defender_var.set(battle_data[4])
        year_var.set(str(battle_data[5]))
        winner_var.set(battle_data[6])

    # Поля ввода
    ttk.Label(main_frame,
              text="Название битвы:").grid(row=0,
                                           column=0,
                                           sticky="w",
                                           pady=6)
    entry_name = ttk.Entry(main_frame, textvariable=name_var, width=30)
    entry_name.grid(row=0, column=1, pady=6, padx=10, sticky="w")

    ttk.Label(main_frame,
              text="Регион проведения:").grid(row=1,
                                              column=0,
                                              sticky="w",
                                              pady=6)
    entry_region = ttk.Entry(main_frame, textvariable=region_var, width=30)
    entry_region.grid(row=1, column=1, pady=6, padx=10, sticky="w")

    ttk.Label(main_frame,
              text="Атакующая сторона:").grid(row=2,
                                              column=0,
                                              sticky="w",
                                              pady=6)
    entry_attacker = ttk.Entry(main_frame, textvariable=attacker_var, width=30)
    entry_attacker.grid(row=2, column=1, pady=6, padx=10, sticky="w")

    ttk.Label(main_frame,
              text="Обороняющая сторона:").grid(row=3,
                                                column=0,
                                                sticky="w",
                                                pady=6)
    entry_defender = ttk.Entry(main_frame, textvariable=defender_var, width=30)
    entry_defender.grid(row=3, column=1, pady=6, padx=10, sticky="w")

    ttk.Label(main_frame,
              text="Год сражения:").grid(row=4,
                                         column=0,
                                         sticky="w",
                                         pady=6)
    spin_year = tk.Spinbox(
        main_frame,
        from_=0,
        to=500,
        width=10,
        textvariable=year_var,
        font=(settings["font_family"], settings["font_size"])
    )
    spin_year.grid(row=4, column=1, pady=6, padx=10, sticky="w")

    ttk.Label(main_frame,
              text="Победитель битвы:").grid(row=5,
                                             column=0,
                                             sticky="w",
                                             pady=6)
    entry_winner = ttk.Entry(main_frame,
                             textvariable=winner_var, width=30)
    entry_winner.grid(row=5,
                      column=1,
                      pady=6,
                      padx=10,
                      sticky="w")

    def save():
        name = name_var.get().strip()
        if not name:
            messagebox.showwarning("Валидация",
                                   "Поле "
                                   "'Название битвы' обязательно!")
            return
        try:
            year = int(year_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return
        data = {
            "id": battle_data[0] if battle_data else None,
            "название": name,
            "регион": region_var.get().strip(),
            "атакующая сторона": attacker_var.get().strip(),
            "обороняющая сторона": defender_var.get().strip(),
            "год": year,
            "победитель": winner_var.get().strip()
        }
        on_save_callback(data)
        dialog.destroy()

    btn_frame = ttk.Frame(main_frame)
    btn_frame.grid(row=6,
                   column=0,
                   columnspan=2,
                   pady=20)
    ttk.Button(btn_frame,
               text="Сохранить",
               command=save).pack(side="left",
                                  padx=10)

    ttk.Button(btn_frame,
               text="Отмена",
               command=dialog.destroy).pack(side="left",
                                            padx=10)
