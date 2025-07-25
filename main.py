import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
import numpy as np
from wind_table import WindTreeview
import wind_table_required_range as wdt


data_pd = pd.read_csv("data.csv", encoding="utf-8")

wind = WindTreeview(title="data")


def table_treb_znach():
    wind_stab = wdt.WindTreeview_required_range("required_range", "850x700+350+150")
    wind_stab.treeview()


def sort_by_index():
    wind.clian_all()
    wind_menu()
    data_pd = pd.read_csv("data.csv", encoding="utf-8")
    combo_index = [data_pd.loc[id]["Индекс"].split(",")[0] for id in data_pd.index]
    ##    print(combo_index)
    index_sort = ttk.Combobox(wind, values=combo_index)
    index_sort.grid(column=0, row=0)

    def sort():
        data_pd_tr = pd.read_csv("required_range.csv", encoding="utf-8")
        wind.treb_znac = [
            data_pd_tr.loc[id]
            for id in data_pd_tr.index
            if data_pd_tr.loc[id]["Индекс"].split(",")[0] == index_sort.get()
        ]
        value = [
            list(data_pd.loc[id])
            for id in data_pd.index
            if data_pd.loc[id]["Индекс"].split(",")[0] == index_sort.get()
        ]
        wind.value = [value[0], ochenca_stab(value=value, treb_znac=wind.treb_znac)]
        wind.columns = list(data_pd.columns)

        wind.treeview()
        ##        print(wind.treb_znac)
        lbt_treb = ttk.Label(wind, text=wind.treb_znac[0])
        lbt_treb.grid(column=102, row=1)

    btn_sort = ttk.Button(wind, text="Сортировка", command=sort)
    btn_sort.grid(column=1, row=0, sticky="ew")
    btn_grafik = ttk.Button(
        wind,
        text="График",
        command=lambda: grafik(
            valueX=wind.columns, valueY1=wind.value, valueY2=wind.treb_znac
        ),
    )
    btn_grafik.grid(column=2, row=0, sticky="ew")


def sort_by_year():
    wind.clian_all()
    wind_menu()
    data_pd = pd.read_csv("data.csv", encoding="utf-8")
    data_pd_tr = pd.read_csv("required_range.csv", encoding="utf-8")
    columns_index, *columns_year = data_pd.columns
    combo_year = columns_year
    year_sort_from = ttk.Combobox(wind, values=combo_year, width=6)
    lbt_year_sort_from = ttk.Label(wind, text="От")
    year_sort_from.grid(column=1, row=0)
    lbt_year_sort_from.grid(column=0, row=0)
    year_sort_to = ttk.Combobox(wind, values=combo_year, width=6)
    lbt_year_sort_to = ttk.Label(wind, text="До")
    year_sort_to.grid(column=3, row=0)
    lbt_year_sort_to.grid(column=2, row=0)

    def sort():
        if year_sort_from.get() > year_sort_to.get():
            lbt = ttk.Label(wind, text="Что, тут")
            lbt.grid(columnspan=100, row=1)
        else:
            frame_ocenki = pd.DataFrame(index=list(data_pd.columns))
            for index in data_pd["Индекс"]:
                data_pd_tr = pd.read_csv("required_range.csv", encoding="utf-8")
                value = [
                    list(data_pd.loc[id])
                    for id in data_pd.index
                    if data_pd.loc[id]["Индекс"].split(",")[0] == index.split(",")[0]
                ]
                treb_znac = [
                    data_pd_tr.loc[id]
                    for id in data_pd_tr.index
                    if data_pd_tr.loc[id]["Индекс"].split(",")[0] == index.split(",")[0]
                ]
                serias_v = pd.Series(value[0], index=list(data_pd.columns))
                serias_s = pd.Series(
                    ochenca_stab(value=value, treb_znac=treb_znac),
                    index=list(data_pd.columns),
                )
                frame_ocenki[value[0][0]] = serias_v
                frame_ocenki[value[0][0] + " " + "Оценка"] = serias_s
            data_pd_ocenka = frame_ocenki.T

            list_index = []
            for i in range(len(list(data_pd_ocenka["Индекс"]))):
                if list(data_pd_ocenka["Индекс"])[i][:-1].isalpha():
                    list_index.append(
                        f"{'Для:'}\n{data_pd_ocenka['Индекс'][i-1].split(',')[0]}:"
                    )
                else:
                    list_index.append(list(data_pd_ocenka["Индекс"])[i])

            data_pd_ocenka["Индекс"] = list_index
            columns_index, *columns_year = data_pd_ocenka.columns
            columns_year_sort = [
                i
                for i in columns_year
                if year_sort_from.get() <= i <= year_sort_to.get()
            ]
            wind.columns = columns_index.split() + columns_year_sort
            wind.value = [
                [
                    data_pd_ocenka[column][id]
                    for column in wind.columns
                    if year_sort_from.get() <= column <= year_sort_to.get()
                    or column == "Индекс"
                ]
                for id in data_pd_ocenka.index
            ]
            wind.treeview()

    btn_sort = ttk.Button(wind, text="Сортировка", command=sort)
    btn_sort.grid(column=4, row=0, sticky="ew")


def ochenca_stab(value, treb_znac):
    ochenca_stab = ["Ок:"]
    for i in value[0][1:]:
        if i != "-":
            i = str(i).split(",")
            ochenca_stab_promez = []
            for j in i:
                if treb_znac[0]["min"] == "-":
                    if float(j) <= float(treb_znac[0]["max"]):
                        ochenca_stab_promez.append("Ок")
                    else:
                        ochenca_stab_promez.append("НеОк")
                elif treb_znac[0]["max"] == "-":
                    if float(j) >= float(treb_znac[0]["min"]):
                        ochenca_stab_promez.append("Ок")
                    else:
                        ochenca_stab_promez.append("НеОк")
                else:
                    if (
                        float(treb_znac[0]["min"])
                        <= float(j)
                        <= float(treb_znac[0]["max"])
                    ):
                        ochenca_stab_promez.append("Ок")
                    else:
                        ochenca_stab_promez.append("НеОк")

            ochenca_stab.append(ochenca_stab_promez)
        else:
            ochenca_stab.append("Нет оценки")
    return ochenca_stab


def grafik(valueX, valueY1, valueY2):
    try:
        l1 = tuple(int(i) for i in valueX[1:])
        ##        d = {i: j for i, j in zip(l1, l2)}
        x = []
        y1 = []
        for i, j in enumerate(l1):
            if valueY1[0][1:][i] != "-":
                if len(str(valueY1[0][1:][i]).split(",")) > 1:
                    for k in str(valueY1[0][1:][i]).split(","):
                        x.append(j)
                        y1.append(float(k))
                else:
                    x.append(j)
                    y1.append(float("".join(str(valueY1[0][1:][i]).split(","))))
            else:
                pass

        x2 = [x[i] for i in range(len(x)) if i == 0 or i == len(x) - 1]
        y_sr = [round(np.mean(y1), 2)] * 2
        y_sko = round(np.std(y1, ddof=1), 2)

        plt.figure(figsize=(20, 10), facecolor="w")

        if valueY2[0][1] != "-":
            y2_minKD = [float(valueY2[0][1])] * 2
            y2_minStab = [float(valueY2[0][3])] * 2
            plt.plot(x2, y2_minKD, linewidth=3, label="minKD")
            plt.plot(x2, y2_minStab, linewidth=3, label="min")
        if valueY2[0][2] != "-":
            y2_maxKD = [float(valueY2[0][2])] * 2
            y2_maxStab = [float(valueY2[0][4])] * 2
            plt.plot(x2, y2_maxKD, linewidth=3, label="maxKD")
            plt.plot(x2, y2_maxStab, linewidth=3, label="max")

        plt.scatter(x, y1, c="k", marker="D", linewidths=3, label="value")
        plt.plot(x2, y_sr, "--b", linewidth=3, label=f"Среднее={y_sr[0]}\СКО={y_sko}")
        plt.xticks(x, x)
        plt.minorticks_on()
        plt.grid(which="major", linestyle="-")
        plt.grid(which="minor")
        plt.xlabel("god")
        plt.ylabel(valueY1[0][0].split(",")[-1])
        plt.legend(loc="upper left")
        plt.title(valueY1[0][0].split(",")[0])
        plt.tight_layout()
        plt.show()
    except Exception as e:
        ##        print(e)
        with open("errors.txt", "a", encoding="utf-8") as f:
            f.write(str(e) + "\n")


def wind_menu():
    main_menu = tk.Menu(wind)
    main_menu_Btn3 = tk.Menu(wind, tearoff=0)

    file_menu = tk.Menu(wind, tearoff=0)
    edit_menu = tk.Menu(wind, tearoff=0)

    file_menu.add_command(label="Таблица", command=main)
    file_menu.add_command(label="Сортировать по индексу", command=sort_by_index)
    file_menu.add_command(label="Сортировать по году", command=sort_by_year)
    file_menu.add_command(
        label="Таблица с заданными значениями", command=table_treb_znach
    )

    edit_menu.add_command(label="Новая колонка", command=wind.new_column)
    edit_menu.add_command(label="Новая стока", command=wind.new_row)
    edit_menu.add_command(label="Удалить колонку", command=wind.delete_column)
    edit_menu.add_command(label="Удалить выделенную строку", command=wind.delete_row)

    main_menu.add_cascade(label="Меню", menu=file_menu)
    main_menu.add_cascade(label="Редактирование", menu=edit_menu)

    wind.config(menu=main_menu)


def main():
    wind.clian_all()
    wind.load()
    ##    wind.columns = ['index', 2011, 2012, 2013, 2014, 2015]
    wind.treeview()
    wind_menu()
    wind.buttons()
    wind.mainloop()


if __name__ == "__main__":

    main()
