"""
Функции генерации текстовых и графических отчётов.

Автор: Давыдов Д.О.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox


def generate_simple_report(df_characters):
    """
    Генерирует простой текстовый отчёт со списком погибших персонажей.

    Описание:
        Создает простой текстовый отчет, содержащий отфильтрованный список
        погибших персонажей, и сохраняет его во внешний файл.
    Входные параметры:
        df_characters (pd.DataFrame) - таблица с данными персонажей.
    Возвращаемый объект: Нет.
    """
    try:
        output_dir = "../output"
        os.makedirs(output_dir, exist_ok=True)
        # Фильтрация справочника по мертвым
        filtered_df = df_characters[df_characters["жив/мертв"] == "Мертв"]
        final_df = filtered_df[["id", "имя", "дом", "культура", "пол", "возраст"]]

        report_path = os.path.join(output_dir, "1_simple_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            line_length = 115
            sep_line = "=" * line_length
            title = "ОТЧЕТ: СПИСОК ПОГИБШИХ ПЕРСОНАЖЕЙ"
            centered_title = title.center(line_length)
            f.write(f"{sep_line}\n{centered_title}\n{sep_line}\n")
            f.write(final_df.to_string(index=False))

        messagebox.showinfo("Успешно", f"Отчет сохранен в:\n{report_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сгенерировать отчет: {e}")


def generate_stat_report(df_characters):
    """
    Вычисляет статистические показатели для качественных и количественных переменных.

    Описание:
        Вычисляет статистические показатели для качественных переменных (частоты, доли)
        и количественных признаков (минимум, максимум, среднее, дисперсия,
        стандартное отклонение возраста) с фиксацией результатов в текстовом файле.
    Входные параметры:
        df_characters (pd.DataFrame) - таблица с данными персонажей.
    Возвращаемый объект: Нет.
    """
    try:
        output_dir = "../output"
        os.makedirs(output_dir, exist_ok=True)

        report_path = os.path.join(output_dir, "2_stat_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(
                "==================================================\n"
                "          СТАТИСТИЧЕСКИЙ ТЕКСТОВЫЙ ОТЧЕТ          \n"
                "==================================================\n\n"
                "--- АНАЛИЗ КАЧЕСТВЕННЫХ ПЕРЕМЕННЫХ ---\n\n"
            )
            # Анализ долей персонажей по полу и статусу жизни
            for col in ["жив/мертв", "пол"]:
                f.write(f"Переменная: {col.upper()}\n")
                f.write("-" * 30 + "\n")
                counts = df_characters[col].value_counts()
                percentages = df_characters[col].value_counts(normalize=True) * 100
                for idx in counts.index:
                    f.write(f"  {idx:<10} | Количество: {counts[idx]:<5} | Доля: {percentages[idx]:.2f}%\n")
                f.write("\n")
            # Качественные признаки возраста
            f.write("--- АНАЛИЗ КОЛИЧЕСТВЕННЫХ ПЕРЕМЕННЫХ (ВОЗРАСТ) ---\n\n")
            age_col = df_characters["возраст"]
            f.write(f"Минимум (min):      {age_col.min()} лет\n")
            f.write(f"Максимум (max):     {age_col.max()} лет\n")
            f.write(f"Среднее (mean):     {age_col.mean():.2f} лет\n")
            f.write(f"Дисперсия (var):    {age_col.var():.2f}\n")
            f.write(f"Станд. отклонение:  {age_col.std():.2f} лет\n")
            f.write("==================================================\n")

        messagebox.showinfo("Успех", f"Статистический отчет сохранен в:\n{report_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сгенерировать отчет: {e}")


def generate_pivot_report(df_characters):
    """
    Строит сводную таблицу распределения полов по домам.

    Описание:
        Строит двухмерную сводную таблицу взаимного распределения полов персонажей
        по топ-10 наиболее часто встречающимся Великим Домам и сохраняет её в файл.
    Входные параметры:
        df_characters (pd.DataFrame) - таблица с данными персонажей.
    Возвращаемый объект: Нет.
    """
    try:
        output_dir = "../output"
        os.makedirs(output_dir, exist_ok=True)
        # Создание pivot_table
        top_houses = df_characters["дом"].value_counts().head(10).index.tolist()
        df_filtered = df_characters[df_characters["дом"].isin(top_houses)]
        pivot_table = pd.pivot_table(
            df_filtered,
            values="id",
            index="дом",
            columns="пол",
            aggfunc="count",
            fill_value=0,
        )

        report_path = os.path.join(output_dir, "3_pivot_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(
                "==================================================\n"
                "      СВОДНАЯ ТАБЛИЦА: РАСПРЕДЕЛЕНИЕ ПОЛ / ДОМ    \n"
                "==================================================\n\n"
            )
            f.write(pivot_table.to_string())
            f.write("\n\n==================================================\n")

        messagebox.showinfo("Успех", f"Сводная таблица сохранена в:\n{report_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сгенерировать отчет: {e}")


def generate_clustered_bar_chart(df_characters):
    """
    Создаёт кластеризованную столбчатую диаграмму соотношения живых и погибших по домам.

    Описание:
        Создает и сохраняет кластеризованную столбчатую диаграмму, отражающую
        соотношение живых и погибших членов для топ-5 Домов и сводной группы.
    Входные параметры:
        df_characters (pd.DataFrame) - таблица с данными персонажей.
    Возвращаемый объект: Нет.
    """
    try:
        graphics_dir = "../graphics"
        os.makedirs(graphics_dir, exist_ok=True)

        df_copy = df_characters.copy()
        # топ-5 домов по численности
        top_houses = df_copy["дом"].value_counts().iloc[1:6].index.tolist()
        # объединяем остальные в "Другие Великие Дома"
        df_copy["дом_группа"] = df_copy["дом"].apply(lambda x: x if x in top_houses else "Другие Великие Дома")
        # таблица: строки - дома, столбцы - жив/мертв
        pivot_data = pd.crosstab(df_copy["дом_группа"], df_copy["жив/мертв"])
        # фиксируем порядок строк
        pivot_data = pivot_data.reindex(top_houses + ["Другие Великие Дома"])

        fig, ax = plt.subplots(figsize=(10, 6))
        # группированная столбчатая диаграмма
        pivot_data.plot(kind="bar", ax=ax, color=["#e74c3c", "#2ecc71"], width=0.8)
        ax.set_title("Соотношение живых и погибших персонажей по Великим Домам", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Великие Дома Вестероса", fontsize=12)
        ax.set_ylabel("Количество персонажей (чел.)", fontsize=12)
        ax.set_xticklabels(pivot_data.index, rotation=15)
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        ax.legend(title="Статус персонажа")
        # подписываем значения над столбцами
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f"{int(height)}", (p.get_x() + p.get_width() / 2.0, height),
                            ha="center", va="baseline", fontsize=10, xytext=(0, 3), textcoords="offset points")
        plt.tight_layout()
        img_path = os.path.join(graphics_dir, "1_clustered_bar.png")
        plt.savefig(img_path, dpi=150)
        plt.close()

        messagebox.showinfo("Успех", f"График сохранен в:\n{img_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сгенерировать график: {e}")


def generate_categorized_histogram(df_characters):
    """
    Строит категоризированную гистограмму распределения возраста по полу.

    Описание:
        Строит гистограмму распределения возраста персонажей, категоризированную
        по половому признаку с помощью наложения полупрозрачных слоев частот.
    Входные параметры:
        df_characters (pd.DataFrame) - таблица с данными персонажей.
    Возвращаемый объект: Нет.
    """
    try:
        graphics_dir = "../graphics"
        os.makedirs(graphics_dir, exist_ok=True)

        df_copy = df_characters.copy()
        male_ages = df_copy[df_copy["пол"] == "Муж"]["возраст"]
        female_ages = df_copy[df_copy["пол"] == "Жен"]["возраст"]

        fig, ax = plt.subplots(figsize=(10, 6))
        # Гистограмма мужчин
        ax.hist(male_ages, bins=20, alpha=0.6, color="#3498db", label="Мужчины", edgecolor="black")
        # Гистограмма женщин
        ax.hist(female_ages, bins=20, alpha=0.6, color="#e74c3c", label="Женщины", edgecolor="black")
        ax.set_title("Категоризированная гистограмма распределения возраста", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Возраст персонажей (лет)", fontsize=12)
        ax.set_ylabel("Частота (кол-во персонажей)", fontsize=12)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.legend(title="Пол персонажа", fontsize=11)
        plt.tight_layout()
        img_path = os.path.join(graphics_dir, "2_categorized_histogram.png")
        plt.savefig(img_path, dpi=150)
        plt.close()

        messagebox.showinfo("Успех", f"График сохранен в:\n{img_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сгенерировать график: {e}")


def generate_boxplot(df_characters):
    """
    Строит диаграммы Бокса-Вискера для возраста по топ-5 домам.

    Описание:
        Визуализирует распределение возраста персонажей по топ-5 Великим Домам
        путем построения одномерных диаграмм Бокса-Вискера (ящиков с усами).
    Входные параметры:
        df_characters (pd.DataFrame) - таблица с данными персонажей.
    Возвращаемый объект: Нет.
    """
    try:
        graphics_dir = "../graphics"
        os.makedirs(graphics_dir, exist_ok=True)

        df_copy = df_characters.copy()
        # Топ-5 домов по численности
        top_houses = df_copy["дом"].value_counts().head(5).index.tolist()
        # Список возрастов для каждого дома
        data_to_plot = [df_copy[df_copy["дом"] == house]["возраст"] for house in top_houses]

        fig, ax = plt.subplots(figsize=(10, 6))
        # Ящик с усами
        box = ax.boxplot(data_to_plot, patch_artist=True, labels=top_houses,
                         medianprops=dict(color="black", linewidth=1.5),
                         flierprops=dict(marker="o", markerfacecolor="red", markersize=6, linestyle="none"))
        # Заливка ящиков
        for patch in box["boxes"]:
            patch.set_facecolor("#3498db")
            patch.set_alpha(0.7)
        ax.set_title("Диаграмма Бокса-Вискера: Распределение возраста по Домам", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Великие Дома Вестероса", fontsize=12)
        ax.set_ylabel("Возраст персонажей (лет)", fontsize=12)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        img_path = os.path.join(graphics_dir, "3_boxplot.png")
        plt.savefig(img_path, dpi=150)
        plt.close()

        messagebox.showinfo("Успех", f"График сохранен в:\n{img_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сгенерировать график: {e}")


def generate_scatter_plot(df_battles):
    """
    Строит диаграмму рассеивания сражений по годам с цветовой кодировкой регионов.

    Описание:
        Строит двухмерную диаграмму рассеивания хронологической последовательности
        сражений (год проведения относительно ID записи) с цветовым кодированием регионов.
    Входные параметры:
        df_battles (pd.DataFrame) - таблица с историческими данными сражений.
    Возвращаемый объект: Нет.
    """
    try:
        graphics_dir = "../graphics"
        os.makedirs(graphics_dir, exist_ok=True)

        df_copy = df_battles.copy()
        fig, ax = plt.subplots(figsize=(10, 6))
        # Уникальные регионы
        regions = df_copy["регион"].unique()
        # Цветовая карта для регионов
        colors = plt.get_cmap("tab10", len(regions))
        # точечная диаграмма по регионам
        for i, region in enumerate(regions):
            region_data = df_copy[df_copy["регион"] == region]
            ax.scatter(region_data["год"], region_data["id"], label=region,
                       s=60, alpha=0.8, color=colors(i), edgecolors="none")
        ax.set_title("Диаграмма рассеивания сражений по годам и регионам", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Год сражения", fontsize=12)
        ax.set_ylabel("Порядковый номер битвы (ID)", fontsize=12)
        ax.set_xticks(df_copy["год"].unique())
        ax.grid(True, linestyle="--", alpha=0.5)
        # Легенда справа за границами графика
        ax.legend(title="Регионы Вестероса", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=10)
        plt.tight_layout()
        img_path = os.path.join(graphics_dir, "4_scatter_plot.png")
        plt.savefig(img_path, dpi=150)
        plt.close()

        messagebox.showinfo("Успех", f"График сохранен в:\n{img_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сгенерировать график: {e}")
