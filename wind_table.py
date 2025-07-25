from tkinter import Tk, Menu, Text, Misc, TclError
from tkinter.font import Font
import tkinter.ttk as ttk
import pandas as pd


class WindTreeview(Tk):

    def __init__(self, title=None, geometry=None):
        super().__init__()
        self.title(title)
        self.razmer_okna()
        self.geometry(self.razmer)
        self.load()

    def load(self):
        self.data_pd = pd.read_csv("data.csv", encoding="utf-8")
        self.value = [list(self.data_pd.loc[id]) for id in self.data_pd.index]
        self.columns = list(self.data_pd.columns)

        return self.columns, self.value

    def razmer_okna(self):
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.razmer = "{}x{}-50-50".format(w - 100, h - 150)

        return self.razmer

    def buttons(self):
        self.btn_save = ttk.Button(text="Сохранить", command=self.save_file)
        self.btn_save.grid(column=0, row=0, sticky="ew")

    def treeview(self):

        height_table = self.winfo_screenmmheight() // 10 + 2
        ##        print(height_table)
        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            height=height_table,
            show="headings",
            selectmode="browse",
            padding=20,
        )
        self.tree.grid(columnspan=100, row=1, sticky="nsew")

        self.style = ttk.Style(self)
        self.style.configure("Treeview", rowheight=30)
        self.style.map(
            "Treeview",
            background=[("selected", "black")],
            foreground=[("selected", "white")],
        )
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        width_table = str(int(self.razmer.split("x")[0]) // len(self.columns))
        for i in self.columns:
            self.tree.column(i, width=width_table)
        self.update()

        for i in self.columns:
            if i == "Индекс":
                self.tree.heading(i, text=i)
                self.tree.column(i, width="150", stretch=True, anchor="w")
            else:
                self.tree.heading(i, text=i)
                self.tree.column(i, width="100", stretch=True, anchor="c")

        self.auto_format()  # zapolnenie tablici s avto viravnivaniem

        ##        for k in self.value:
        ##                self.tree.insert('','end', values=k)

        self.main_menu_Btn_3 = Menu(self, tearoff=0)
        self.main_menu_Btn_3.add_command(
            label="Удалить выделенную строку", command=self.delete_row
        )
        self.main_menu_Btn_3.add_command(
            label="Добавить новую строку", command=self.new_row
        )
        self.main_menu_Btn_3.add_command(
            label="Ввести значение", command=self.set_value_1
        )

        self.tree.bind("<Double-1>", func=self.set_value_1)
        self.tree.bind("<Button-1>", func=self.select_row)
        self.tree.bind("<Button-3>", func=self.button_3)
        self.tree.bind("<B1-Motion>", func=self.motion_hendler)

        self.scrolbarY = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrolbarY.set)
        self.scrolbarY.grid(column=101, row=1, sticky="ns")

        self.scrolbarX = ttk.Scrollbar(
            self, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(xscroll=self.scrolbarX.set)
        self.scrolbarX.grid(columnspan=100, row=2, sticky="ew")

    def set_value_1(self, event=None):
        ##        self.win = WindTreeview('Vvod', '200x70+300+250')
        if self.column == "#1":
            self.win = WindTreeview("Vvod")
            self.win.geometry("220x110+300+250")
            self.edit = Text(self.win, height=5, width=25, wrap="word")
            self.edit.insert(1.0, self.tree.set(self.row, self.column))
            self.edit.pack()
        else:
            self.win = WindTreeview("Vvod")
            self.win.geometry("220x80+300+250")
            self.edit = ttk.Entry(self.win, width=50)
            self.edit.insert(0, self.tree.set(self.row, self.column))
            self.edit.pack()

        def save_edit():
            if self.column == "#1":
                self.tree.set(
                    self.row, column=self.column, value=self.edit.get(1.0, "end")
                )
            else:
                self.tree.set(self.row, column=self.column, value=self.edit.get())
            self.win.destroy()

        self.btn_ok = ttk.Button(self.win, text="OK", width=18, command=save_edit)
        self.btn_ok.pack()

    def save_file(self):
        _save = [list(self.tree.item(i, "values")) for i in self.tree.get_children("")]
        self.data_save = [
            [i[j].replace("\n", "").replace("\r", "") for j in range(len(i))]
            for i in _save
        ]
        self.data_frame = pd.DataFrame(self.data_save, columns=self.columns)
        ##        print(self.data_frame, type(self.data_frame))
        return self.data_frame.to_csv("data.csv", index=False, encoding="utf-8")

    def new_column(self):
        self.data_pd = pd.read_csv("data.csv", encoding="utf-8")
        ##        print(self.columns)
        self.columns.append(int(self.data_pd.columns[-1]) + 1)
        ##        print(self.columns)
        self.value = [
            list(self.tree.item(i, "values")) for i in self.tree.get_children("")
        ]
        for i in range(len(self.value)):
            self.value[i].append("-")
        self.treeview()
        self.tree.update()
        self.save_file()

    def button_3(self, event):
        self.main_menu_Btn_3.post(event.x_root, event.y_root)
        self.row = self.tree.identify_row(event.y)
        self.column = self.tree.identify_column(event.x)
        ##        print(self.row, self.column)
        return self.row, self.column

    def delete_column(self):
        self.data_pd = pd.read_csv("data.csv", encoding="utf-8")
        _ = self.data_pd.pop(self.data_pd.columns[-1])
        self.data_pd.to_csv("data.csv", index=False, encoding="utf-8")
        self.value = [list(self.data_pd.loc[id]) for id in self.data_pd.index]
        self.columns = list(self.data_pd.columns)
        self.treeview()
        self.tree.update()

    def new_row(self):
        self.data_pd = pd.read_csv("data.csv", encoding="utf-8")
        self.value = [self.tree.item(i, "values") for i in self.tree.get_children("")]
        add_element_value = tuple(("-" for i in range(len(self.value[0]))))
        self.value.append(add_element_value)
        self.treeview()
        self.tree.update()

    def select_row(self, event):
        self.row = self.tree.identify_row(event.y)
        self.column = self.tree.identify_column(event.x)
        ##        print(self.row, self.column)
        return self.row, self.column

    def format_column(self, stroka, widh_column):
        stroka = str(stroka)
        font = Font(font="TkDefaultFont")
        if (
            font.measure(stroka) < widh_column
        ):  # sravnenie razmera stroki s shirinoy stolbca
            return stroka
        else:
            elements = stroka.split(",")
            lines = [""]
            for (
                element
            ) in elements:  # formirovanie spiska s elemetami dlinoq < shiriny stolbca
                line = lines[-1] + "," + element
                if font.measure(line) < widh_column - 5:
                    lines[-1] = line.strip(",").strip().strip(",")
                else:
                    lines.append(element)
            return ",\n".join(lines)  # formirivanie stroki s perenosom

    def auto_format(self):
        col_widh = [
            self.tree.column(i)["width"] for i in self.tree["columns"]
        ]  # spisok s shirinoq columns
        n = 0
        for iid in self.value:
            n += 1
            new_line = []
            for v, w in zip(iid, col_widh):
                new_line.append(self.format_column(v, w))
            if n % 2 != 0:
                self.tree.insert("", "end", values=new_line, tag="lightblue")
                self.tree.tag_configure("lightblue", background="lightblue")
            else:
                self.tree.insert("", "end", values=new_line)

    def motion_hendler(self, event):
        if (
            self.tree.identify_region(event.x, event.y) == "separator"
        ):  # opredelyem mesto gde dvigaem mausom
            col = self.tree.identify_column(event.x)
            widh = self.tree.column(self.tree.identify_column(event.x))[
                "width"
            ]  # opredelyem column i ego shirinu
            for iid in self.tree.get_children():
                stroka = self.tree.item(iid)["values"][int(col.replace("#", "")) - 1]

                new_line = self.format_column(str(stroka).replace("\n", ""), widh)
                self.tree.set(iid, col, new_line)
        else:
            pass

    def delete_row(self):
        try:
            self.tree.delete(self.row)
        except TclError as e:
            print(e)

    def clian_all(self):
        for i in Misc.winfo_children(self):
            i.destroy()


if __name__ == "__main__":

    root = WindTreeview("test", "1050x900+150+50")
    root.treeview()
    root.buttons()

    root.mainloop()
