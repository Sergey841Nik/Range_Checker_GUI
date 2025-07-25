from tkinter import Menu
import tkinter.ttk as ttk
import pandas as pd
from wind_table import WindTreeview

class WindTreeview_required_range(WindTreeview):

    def __init__(self, title=None, geometry=None):
        super().__init__()
##        self.title(title)
        self.geometry(geometry)
##        self.load()

    def load(self):
        self.data_pd = pd.read_csv('required_range.csv', encoding='utf-8')
        self.data_pd_value = pd.read_csv('data.csv', encoding='utf-8')

        self.value = [list(self.data_pd.loc[id])[1:] for id in self.data_pd.index]
        self.columns = list(self.data_pd.columns)

        try:
            for i in range(len(list(self.data_pd_value['Индекс']))):
                self.value[i].insert(0, list(self.data_pd_value['Индекс'])[i])

        except Exception as e:
            print(e)
            with open('errors.txt', 'a', encoding='utf-8') as f:
                f.write(str(e) + '\n')
            def destroy_oshibki():
                self.lable_oshobka.destroy()
                self.btk_oshibka.destroy()

            self.lable_oshobka = ttk.Label(self, text = '''
                Какая-то ошибка
            ''')
            self.lable_oshobka.grid(column=0, row=0)
            self.btk_oshibka = ttk.Button(self, text = 'что-то', command = destroy_oshibki)
            self.btk_oshibka.grid(column=1, row=0)
            self.value = [list(self.data_pd.loc[id]) for id in self.data_pd.index]

        return self.value, self.columns



    def treeview(self):
        self.tree = ttk.Treeview(self, columns=self.columns, height=20, show='headings', selectmode='browse')
        self.tree.grid(columnspan=100, row=1, sticky='nsew')
        self.style = ttk.Style(self)
        self.style.configure('Treeview', rowheight=28)

        for i in self.columns:
            if i == 'index':
                self.tree.heading(i, text=i)
                self.tree.column(i, width='180', stretch=True, anchor='w')
            else:
                self.tree.heading(i, text=i)
                self.tree.column(i, width='100', stretch=True, anchor='c')

        self.auto_format()
##
##        for k in self.value:
##                self.tree.insert('','end', values=k)

        self.main_menu = Menu(self, tearoff=0)
        self.main_menu.add_command(label='Сохраниь', command=self.save_file)
        self.config(menu=self.main_menu)

        self.main_menu_Btn_3 = Menu(self, tearoff=0)
        self.main_menu_Btn_3.add_command(label='Удалить выделеную строку', command=self.delete_row)
        self.main_menu_Btn_3.add_command(label='Добавить строку', command=self.new_row)
        self.main_menu_Btn_3.add_command(label='Изменить значение', command=self.set_value_1)


        self.tree.bind('<Double-1>', func=self.set_value_1)
        self.tree.bind('<Button-1>', func=self.select_row)
        self.tree.bind('<Button-3>', func=self.button_3)
        self.tree.bind('<B1-Motion>', func=self.motion_hendler)

        self.scrolbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=self.scrolbar.set)
        self.scrolbar.grid(column=101,row=1, sticky='ns')


    def save_file(self):
        self.data_save = [self.tree.item(i, 'values') for i in self.tree.get_children('')]
        self.data_frame = pd.DataFrame(self.data_save, columns=self.columns)
##        print(self.data_frame)
        return self.data_frame.to_csv('required_range.csv', index=False, encoding='utf-8')

    def new_row(self):
        self.data_pd = pd.read_csv('required_range.csv', encoding='utf-8')
        self.value = [self.tree.item(i, 'values') for i in self.tree.get_children('')]
        add_element_value = tuple(('-' for i in range(len(self.value[0]))))
        self.value.append(add_element_value)
        self.treeview()
        self.tree.update()

if __name__ == '__main__':
    data = {}

    root = WindTreeview_required_range('test', '750x600+350+150')
    root.treeview()

    root.mainloop()
