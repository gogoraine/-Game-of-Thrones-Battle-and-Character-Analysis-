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
    Автор: Давыдов Д.О.
    """
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.geometry("460x400")
    dialog.resizable(False, False)
    dialog.grab_set()

    main_frame = ttk.LabelFrame(dialog, text=" Данные персонажа ", padding=15)
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)

    # Переменные для полей ввода
    v_name, v_house, v_culture = tk.StringVar(), tk.StringVar(), tk.StringVar()
    v_gender = tk.StringVar(value="Муж")
    v_age = tk.StringVar(value="0")
    v_status = tk.StringVar(value="Жив")

    # Заполнение, если редактирование
    if character_data is not None:
        _, c_nm, c_hs, c_cl, c_gn, c_ag, c_st = character_data
        v_name.set(c_nm)
        v_house.set(c_hs)
        v_culture.set(c_cl)
        v_gender.set(c_gn)
        v_age.set(str(c_ag))
        v_status.set(c_st)

    c_grid_labels = {"sticky": "w", "pady": 6}
    c_grid_inputs = {"pady": 6, "padx": 10, "sticky": "w"}

    # Поля ввода
    label = ttk.Label(main_frame, text="Имя персонажа:")
    entry_name = ttk.Entry(main_frame, textvariable=v_name, width=30)

    label_house = ttk.Label(main_frame, text="Великий Дом:")
    entry_house = ttk.Entry(main_frame, textvariable=v_house, width=30)

    label_culture = ttk.Label(main_frame, text="Культура:")
    entry_culture = ttk.Entry(main_frame, textvariable=v_culture, width=30)

    label_gender = ttk.Label(main_frame, text="Пол персонажа:")
    combo_gender = ttk.Combobox(
        main_frame,
        values=["Муж", "Жен"],
        state="readonly",
        textvariable=v_gender,
        width=28
    )

    label_age = ttk.Label(main_frame, text="Полных лет (возраст):")
    spin_age = tk.Spinbox(
        main_frame,
        from_=0,
        to=150,
        width=10,
        textvariable=v_age,
        font=(settings["font_family"], settings["font_size"])
    )

    label_status = ttk.Label(main_frame, text="Текущий статус:")
    combo_status = ttk.Combobox(
        main_frame,
        values=["Жив", "Мертв"],
        state="readonly",
        textvariable=v_status,
        width=28
    )

    label.grid(row=0, column=0, **c_grid_labels)
    entry_name.grid(row=0, column=1, **c_grid_inputs)
    label_house.grid(row=1, column=0, **c_grid_labels)
    entry_house.grid(row=1, column=1, **c_grid_inputs)
    label_culture.grid(row=2, column=0, **c_grid_labels)
    entry_culture.grid(row=2, column=1, **c_grid_inputs)
    label_gender.grid(row=3, column=0, **c_grid_labels)
    combo_gender.grid(row=3, column=1, **c_grid_inputs)
    label_age.grid(row=4, column=0, **c_grid_labels)
    spin_age.grid(row=4, column=1, **c_grid_inputs)
    label_status.grid(row=5, column=0, **c_grid_labels)
    combo_status.grid(row=5, column=1, **c_grid_inputs)

    def save():
        """Обработчик сохранения: валидация и вызов колбэка."""
        extracted_name = v_name.get().strip()
        if len(extracted_name) == 0:
            messagebox.showwarning("Валидация",
                                   "Поле 'Имя персонажа' обязательно!")
            return
        try:
            parsed_age = int(v_age.get())
            if parsed_age < 0:
                raise ArithmeticError
        except (ValueError, ArithmeticError):
            messagebox.showerror("Ошибка",
                                 "Возраст должен быть "
                                 "целым неотрицательным числом!")
            return

        record_id = character_data[0] if character_data else None
        character_payload = {
            "id": record_id,
            "имя": extracted_name,
            "дом": v_house.get().strip(),
            "культура": v_culture.get().strip(),
            "пол": v_gender.get(),
            "возраст": parsed_age,
            "жив/мертв": v_status.get()
        }
        on_save_callback(character_payload)
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
    Автор: Давыдов Д.О.
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

    v_b_name, v_b_region = tk.StringVar(), tk.StringVar()
    v_b_attacker, v_b_defender = tk.StringVar(), tk.StringVar()
    v_b_year = tk.StringVar(value="298")
    v_b_winner = tk.StringVar()

    if battle_data is not None:
        _, b_nm, b_rg, b_at, b_df, b_yr, b_wn = battle_data
        v_b_name.set(b_nm)
        v_b_region.set(b_rg)
        v_b_attacker.set(b_at)
        v_b_defender.set(b_df)
        v_b_year.set(str(b_yr))
        v_b_winner.set(b_wn)

    b_grid_lbls = {"pady": 6, "sticky": "w"}
    b_grid_inps = {"sticky": "w", "padx": 10, "pady": 6}

    # Поля ввода
    lbl_b_name = ttk.Label(main_frame, text="Название битвы:")
    entry_name = ttk.Entry(main_frame, textvariable=v_b_name, width=30)

    lbl_b_region = ttk.Label(main_frame, text="Регион проведения:")
    entry_region = ttk.Entry(main_frame, textvariable=v_b_region, width=30)

    lbl_b_attacker = ttk.Label(main_frame, text="Атакующая сторона:")
    entry_attacker = ttk.Entry(main_frame, textvariable=v_b_attacker, width=30)

    lbl_b_defender = ttk.Label(main_frame, text="Обороняющая сторона:")
    entry_defender = ttk.Entry(main_frame, textvariable=v_b_defender, width=30)

    lbl_b_year = ttk.Label(main_frame, text="Год сражения:")
    spin_year = tk.Spinbox(
        main_frame,
        from_=0,
        to=500,
        width=10,
        textvariable=v_b_year,
        font=(settings["font_family"], settings["font_size"])
    )

    lbl_b_winner = ttk.Label(main_frame, text="Победитель битвы:")
    entry_winner = ttk.Entry(main_frame, textvariable=v_b_winner, width=30)

    lbl_b_name.grid(row=0, column=0, **b_grid_lbls)
    entry_name.grid(row=0, column=1, **b_grid_inps)
    lbl_b_region.grid(row=1, column=0, **b_grid_lbls)
    entry_region.grid(row=1, column=1, **b_grid_inps)
    lbl_b_attacker.grid(row=2, column=0, **b_grid_lbls)
    entry_attacker.grid(row=2, column=1, **b_grid_inps)
    lbl_b_defender.grid(row=3, column=0, **b_grid_lbls)
    entry_defender.grid(row=3, column=1, **b_grid_inps)
    lbl_b_year.grid(row=4, column=0, **b_grid_lbls)
    spin_year.grid(row=4, column=1, **b_grid_inps)
    lbl_b_winner.grid(row=5, column=0, **b_grid_lbls)
    entry_winner.grid(row=5, column=1, **b_grid_inps)

    def save():
        battle_title = v_b_name.get().strip()
        if len(battle_title) == 0:
            messagebox.showwarning("Валидация",
                                   "Поле "
                                   "'Название битвы' обязательно!")
            return
        try:
            battle_year = int(v_b_year.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return

        battle_id = battle_data[0] if battle_data else None
        battle_payload = {
            "id": battle_id,
            "название": battle_title,
            "регион": v_b_region.get().strip(),
            "атакующая сторона": v_b_attacker.get().strip(),
            "обороняющая сторона": v_b_defender.get().strip(),
            "год": battle_year,
            "победитель": v_b_winner.get().strip()
        }
        on_save_callback(battle_payload)
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
