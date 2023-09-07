import pandas as pd
import datetime as dt
from params import *


def create_html() -> None:
    df = pd.read_csv(CSV_FILE_NAME, index_col=0)

    # Create useful params
    ALL_DAYS = pd.date_range(start="08-28-2023", end="12-31-2023")
    WEEKS = ALL_DAYS
    WEEKS = [WEEKS[i:i+7] for i in range(0, len(WEEKS), 7)]
    # TODAY = dt.datetime.today().strftime("%Y-%m-%d")
    TODAY = pd.to_datetime("08-28-23")
    CURRENT_WEEK = [week for week in WEEKS if TODAY in week][0]
    CURRENT_WEEK_NUM = [NUM for NUM, week in enumerate(WEEKS) if TODAY in week][0]
    NEXT_WEEK = WEEKS[CURRENT_WEEK_NUM + 1]
    TIMES = {
        1: "9:00-10:30",
        2: "10:45-12:15",
        3: "13:15-14:45",
        4: "15:00-16:30",
        5: "16:45-18:15",
        # 6: "18:45-20:20",
        # 7: "20:25-22:00",
    }
    DAYS = {
        "ПН": "Понедельник",
        "ВТ": "Вторник",
        "СР": "Среда",
        "ЧТ": "Четверг",
        "ПТ": "Пятница",
        "СБ": "Суббота",
        "ВС": "Воскресенье"
    }

    # Create empty schedule template
    schedule_template = pd.DataFrame({
        "Пары": TIMES.keys(),
        "Часы": TIMES.values()
    })
    schedule = pd.DataFrame({
        "Дни": ALL_DAYS,
        "День недели": list(DAYS.values()) * len(WEEKS)
    }).merge(schedule_template, how='cross')

    schedule["Дни"] = pd.to_datetime(schedule["Дни"])
    schedule["Дисциплина"] = ""
    schedule["Аудитория"] = ""
    schedule["Преподаватель"] = ""

    # Iteration by days
    for date in ALL_DAYS:
        day = date.day
        month = date.month
        year = date.year

        day_info = df.query("День == @day & Месяц == @month & Год == @year")

        if day_info.empty:
            # Empty month
            continue
        else:
            for i, row in day_info.iterrows():
                # Parse information
                day_of_week = DAYS[row["День недели"]]
                start = row["Начало"]
                end = row["Окончание"]
                disp = row["Дисциплина"]
                address = row["Адрес"]
                room = row["Аудитория"]
                teacher = row["Преподаватель"]

                # Remove garbage
                clear_teachers = []
                for one_teacher in teacher.split(","):
                    clear_teachers.append(one_teacher.split("(")[0].strip().replace("  ", " "))
                clear_teachers = ", ".join(clear_teachers)

                lesson_description = f"{disp}\n{clear_teachers}\nауд. {room} ({address})"

                # Replacement cells in template
                schedule.loc[
                    (schedule["День недели"] == day_of_week)
                    &
                    (schedule["Дни"] == pd.to_datetime(date))
                    &
                    (
                        (schedule["Часы"].str.contains(start))
                        |
                        (schedule["Часы"].str.contains(end))
                    ),
                    "Преподаватель"
                ] = clear_teachers

                schedule.loc[
                    (schedule["День недели"] == day_of_week)
                    &
                    (schedule["Дни"] == pd.to_datetime(date))
                    &
                    (
                        (schedule["Часы"].str.contains(start))
                        |
                        (schedule["Часы"].str.contains(end))
                    ),
                    "Аудитория"
                ] = room

                schedule.loc[
                    (schedule["День недели"] == day_of_week)
                    &
                    (schedule["Дни"] == pd.to_datetime(date))
                    &
                    (
                        (schedule["Часы"].str.contains(start))
                        |
                        (schedule["Часы"].str.contains(end))
                    ),
                    "Дисциплина"
                ] = disp

    schedule["Дни"] = schedule["Дни"].astype(str)
    schedule["День недели"] = schedule["Дни"] + " (" + schedule["День недели"] + ")"
    schedule = schedule.drop("Дни", axis=1)
    schedule = schedule.set_index(["День недели", "Часы"])

    # Save html code
    schedule.to_html(HTML_FILE_NAME, na_rep=" ", justify='center', border=3, encoding="utf-8")
