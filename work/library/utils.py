"""
Утилиты для загрузки/сохранения настроек, работы с данными и размножения битв.

Модуль функций: загрузка/сохранение настроек, работа с данными,
приведение к 3НФ, размножение записей о битвах, сохранение/загрузка pickle.
Автор: Давыдов Д.О.
"""
import os
import configparser
import random
import pandas as pd
import numpy as np


def load_settings(ini_path):
    """
    Загружает настройки интерфейса из .ini файла.

    Описание:
        Загружает настройки интерфейса из .ini файла.
        Если файла или секции нет, возвращает значения по умолчанию.
    Входные параметры:
        ini_path (str) - путь к файлу settings.ini.
    Возвращаемый объект:
        dict - словарь с ключами: bg_color, btn_color, font_family, font_size.
    """
    defaults = {
        "bg_color": "#f0f0f0",
        "btn_color": "#e1e1e1",
        "font_family": "Calibri Light",
        "font_size": 12
    }
    if os.path.exists(ini_path):
        config = configparser.ConfigParser()
        config.read(ini_path, encoding="utf-8")
        for key in defaults:
            if key == "font_size":
                defaults[key] = config.getint("Theme", key, fallback=defaults[key])
            else:
                defaults[key] = config.get("Theme", key, fallback=defaults[key])
    return defaults


def save_settings(settings_dict, ini_path):
    """
    Сохраняет настройки интерфейса в .ini файл.

    Описание:
        Сохраняет настройки интерфейса в .ini файл.
        Если файла нет, он будет создан.
    Входные параметры:
        settings_dict (dict) - словарь с ключами настроек.
        ini_path (str) - путь к файлу settings.ini.
    Возвращаемый объект: Нет.
    """
    config = configparser.ConfigParser()
    config.read(ini_path, encoding="utf-8")
    if not config.has_section("Theme"):
        config.add_section("Theme")
    for key, value in settings_dict.items():
        config.set("Theme", key, str(value))
    with open(ini_path, "w", encoding="utf-8") as f:
        config.write(f)


def save_dataframes_pickle(df_char, df_batt, data_dir):
    """
    Сохраняет DataFrame персонажей и сражений в бинарные файлы pickle.

    Описание:
        Сохраняет DataFrame персонажей и сражений в бинарные файлы pickle.
        Папка data_dir создаётся автоматически, если её нет.
    Входные параметры:
        df_char (pd.DataFrame) - DataFrame персонажей.
        df_batt (pd.DataFrame) - DataFrame сражений.
        data_dir (str) - путь к папке для сохранения.
    Возвращаемый объект: Нет.
    """
    os.makedirs(data_dir, exist_ok=True)
    char_path = os.path.join(data_dir, "characters.pkl")
    batt_path = os.path.join(data_dir, "battles.pkl")
    df_char.to_pickle(char_path)
    df_batt.to_pickle(batt_path)


def load_dataframes_pickle(data_dir):
    """
    Загружает DataFrame из pickle, если файлы существуют.

    Описание:
        Загружает DataFrame из pickle, если файлы существуют.
    Входные параметры:
        data_dir (str) - путь к папке с .pkl файлами.
    Возвращаемый объект:
        tuple - (df_characters, df_battles) или (None, None), если файлов нет.
    """
    char_path = os.path.join(data_dir, "characters.pkl")
    batt_path = os.path.join(data_dir, "battles.pkl")
    if os.path.exists(char_path) and os.path.exists(batt_path):
        return pd.read_pickle(char_path), pd.read_pickle(batt_path)
    return None, None


def expand_battles_data(df_battles, target_count=100):
    """
    Увеличивает количество записей о битвах до target_count путём размножения.

    Описание:
        Увеличивает количество записей о битвах до target_count путём размножения.
        Копиям меняется id, название (добавляется суффикс), год сдвигается на случайное число.
    Входные параметры:
        df_battles (pd.DataFrame) - исходный DataFrame с битвами.
        target_count (int) - желаемое минимальное количество записей.
    Возвращаемый объект:
        pd.DataFrame - расширенный DataFrame.
    """
    if len(df_battles) >= target_count:
        return df_battles

    expanded = df_battles.copy()
    current_count = len(expanded)
    needed = target_count - current_count
    repeat_times = (needed // current_count) + 1
    new_rows = []

    for _, row in df_battles.iterrows():
        for rep in range(repeat_times):
            if len(new_rows) >= needed:
                break
            new_row = row.to_dict()
            new_id = expanded['id'].max() + len(new_rows) + 1
            new_row['id'] = new_id
            new_row['название'] = f"{row['название']} (копия {rep+1})"
            year_shift = random.randint(-5, 5)
            new_year = max(0, row['год'] + year_shift)
            new_row['год'] = new_year
            new_rows.append(pd.DataFrame([new_row]))

    if new_rows:
        expanded = pd.concat([expanded] + new_rows, ignore_index=True)

    while len(expanded) < target_count:
        last_row = expanded.iloc[-1].to_dict()
        last_row['id'] = expanded['id'].max() + 1
        last_row['название'] = last_row['название'] + " (доп)"
        expanded = pd.concat([expanded, pd.DataFrame([last_row])], ignore_index=True)

    return expanded


def create_initial_data(battles_csv, characters_csv, target_battles=100):
    """
    Создаёт DataFrame персонажей и сражений из исходных CSV-файлов.

    Описание:
        Создаёт DataFrame персонажей и сражений из исходных CSV-файлов,
        приводит к 3 нормальной форме, размножает битвы.
    Входные параметры:
        battles_csv (str) - путь к battles.csv.
        characters_csv (str) - путь к character-predictions.csv.
        target_battles (int) - требуемое количество записей о битвах.
    Возвращаемый объект:
        tuple - (df_characters, df_battles) два подготовленных DataFrame.
    """
    # --- Персонажи ---
    data_char_pred = pd.read_csv(characters_csv)
    char = data_char_pred[["name", "house", "culture", "male", "age", "isAlive"]].copy()
    char["male"] = char["male"].map({1: "Муж", 0: "Жен"})
    char["isAlive"] = char["isAlive"].map({1: "Жив", 0: "Мертв"})
    char["house"] = char["house"].fillna("Нет дома")
    char["culture"] = char["culture"].fillna("Неизвестно")
    median_age = char["age"].median()
    char["age"] = char["age"].fillna(median_age)
    char["age"] = char["age"].apply(lambda x: int(x) if x >= 0 else median_age)
    char.insert(0, "id", range(1, len(char)+1))
    char.columns = ["id", "имя", "дом", "культура", "пол", "возраст", "жив/мертв"]

    # --- Сражения ---
    data_battles = pd.read_csv(battles_csv)
    batt = data_battles[["name", "region", "attacker_king", "defender_king", "attacker_outcome", "year"]].copy()
    batt["winner"] = np.where(batt["attacker_outcome"] == "win", batt["attacker_king"], batt["defender_king"])
    batt = batt.drop(columns=["attacker_outcome"])
    batt["attacker_king"] = batt["attacker_king"].fillna("Неизвестный лидер")
    batt["defender_king"] = batt["defender_king"].fillna("Неизвестный лидер")
    batt["winner"] = batt["winner"].fillna("Ничья")
    batt.insert(0, "id", range(1, len(batt)+1))
    batt.columns = ["id", "название", "регион", "атакующая сторона", "обороняющая сторона", "год", "победитель"]
    batt = expand_battles_data(batt, target_battles)
    return char, batt


def init_dataframes(battles_csv, characters_csv, data_dir, target_battles=100):
    """
    Инициализирует DataFrame, используя кэш в папке data.

    Описание:
        Инициализирует DataFrame, используя кэш в папке data.
        Если кэш существует, загружает из него, иначе создаёт из CSV и сохраняет.
    Входные параметры:
        battles_csv (str) - путь к battles.csv.
        characters_csv (str) - путь к character-predictions.csv.
        data_dir (str) - папка для хранения .pkl файлов.
        target_battles (int) - требуемое количество битв.
    Возвращаемый объект:
        tuple - (df_characters, df_battles).
    """
    df_char, df_batt = load_dataframes_pickle(data_dir)
    if df_char is None or df_batt is None:
        os.makedirs(data_dir, exist_ok=True)
        df_char, df_batt = create_initial_data(battles_csv, characters_csv, target_battles)
        save_dataframes_pickle(df_char, df_batt, data_dir)
    return df_char, df_batt
