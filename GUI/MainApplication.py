import shelve
import tkinter as tk


class MainApplication(tk.Tk):
    DB_NAME = 'tiles'

    def __init__(self):
        super().__init__(className='颜色分拣系统')

        self._frame = None
        self.selected_series = None
        self.is_updating = False

        self.geometry('400x260')
        self.switch_frame(StartMenu)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='主页').grid(pady=10)
        tk.Button(self, text='运作区', command=lambda: master.switch_frame(OperatingMenu)).grid()
        tk.Button(self, text='训练区', command=lambda: master.switch_frame(TrainingMenu)).grid()


class Listing(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.my_list = None
        self.prompt = None

    def build_list(self):
        list_frame = tk.Frame(self)
        list_frame.grid(row=1, column=0)

        self.my_list = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.my_list.bind('<<ListboxSelect>>', self.selection_callback)
        self.my_list.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        scrollbar.config(command=self.my_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.my_list.config(yscrollcommand=scrollbar.set)

        self.populate_list()
        self.select_default_series()

    def selection_callback(self, event):
        if self.my_list.curselection():
            series = self.my_list.get(self.my_list.curselection())
            self.master.selected_series = series

    def populate_list(self):
        with shelve.open(self.master.DB_NAME) as db:
            series_list = sorted(list(db.keys()))

            for series in series_list:
                self.my_list.insert(tk.END, series)

    def select_default_series(self):
        if self.my_list.size() > 0:
            self.my_list.selection_set(0)
            series = self.my_list.get(self.my_list.curselection())
            self.master.selected_series = series

    def selection_based_prompt(self, hook):
        if self.master.selected_series:
            hook()
        else:
            self.bell()
            self.prompt = tk.Toplevel(self)
            tk.Label(self.prompt, text='没有选到瓷砖系列').pack()
            tk.Button(self.prompt, text='确定', command=self.prompt.destroy).pack()


class Instance(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.preview_frame = None
        self.num_shades = tk.IntVar()

        if self.master.selected_series:
            with shelve.open(self.master.DB_NAME) as db:
                self.num_shades.set(db[self.master.selected_series]['num_shades'])

    def build_preview(self):
        self.preview_frame = tk.Frame(self)
        self.preview_frame.pack()
        self.build_shades()

    def build_shades(self):
        # destroy previous shades
        for child in self.preview_frame.winfo_children():
            child.destroy()
        # build new shades
        for i in range(1, 1 + self.num_shades.get()):
            self.build_shade_option(i)

    def build_shade_option(self, option):
        option_frame = tk.Frame(self.preview_frame)
        option_frame.pack(side=tk.LEFT)
        tk.Label(option_frame, text=str(option), fg='white', bg='yellow', bd=1, width=6, height=6).pack(padx=6)


class OperatingMenu(Listing):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='运作区').grid(row=0, column=0, columnspan=3, pady=10)

        self.build_list()
        self.build_user_actions()

        tk.Button(self, text='主页', command=lambda: master.switch_frame(StartMenu)).grid(row=2, column=0, columnspan=3)

    def build_user_actions(self):
        actions_frame = tk.Frame(self)
        actions_frame.grid(row=1, column=1)
        tk.Button(actions_frame, text='确认', command=lambda: self.selection_based_prompt(self.operate_hook)).pack()

    def operate_hook(self):
        self.master.switch_frame(OperatingPage)


class OperatingPage(Instance):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='运行页面').pack(pady=10)
        tk.Label(self, text=self.master.selected_series).pack(pady=10)

        self.build_preview()
        self.build_shades()

        tk.Button(self, text='开始').pack()
        tk.Button(self, text='结束', command=lambda: self.master.switch_frame(OperatingMenu)).pack()


class TrainingMenu(Listing):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='训练区').grid(row=0, column=0, columnspan=3, pady=10)

        self.build_list()
        self.build_user_actions()

        tk.Button(self, text='主页', command=lambda: self.master.switch_frame(StartMenu)).grid(row=2, column=0, columnspan=3, pady=10)

    def build_user_actions(self):
        actions_frame = tk.Frame(self)
        actions_frame.grid(row=1, column=1)
        tk.Button(actions_frame, text='新建', command=self.create_hook).pack()
        tk.Button(actions_frame, text='更改', command=lambda: self.selection_based_prompt(self.update_hook)).pack()
        tk.Button(actions_frame, text='删除', command=lambda: self.selection_based_prompt(self.delete_hook)).pack()
        tk.Button(actions_frame, text='训练', command=lambda: self.selection_based_prompt(self.train_hook)).pack()

    def create_hook(self):
        self.master.selected_series = None
        self.master.switch_frame(FormPage)

    def update_hook(self):
        self.master.is_updating = True
        self.master.switch_frame(FormPage)

    def delete_hook(self):
        self.bell()
        self.prompt = tk.Toplevel(self)
        tk.Label(self.prompt, text='您确定要把以下瓷砖系列删除码: ' + self.master.selected_series).pack()
        tk.Button(self.prompt, text='确定', command=self.delete_series).pack()
        tk.Button(self.prompt, text='取消', command=self.prompt.destroy).pack()

    def delete_series(self):
        with shelve.open(self.master.DB_NAME) as db:
            print('正在删除', self.master.selected_series)
            del db[self.master.selected_series]
            self.master.selected_series = None
        self.prompt.destroy()
        self.master.switch_frame(TrainingMenu)

    def train_hook(self):
        self.master.switch_frame(TrainingPage)


class FormPage(Instance):
    def __init__(self, master):
        super().__init__(master)

        self.series_name = tk.StringVar()

        tk.Label(self, text='瓷砖资料表格').pack(pady=10)

        self.build_form()
        self.build_preview()
        self.build_user_actions()

    def build_form(self):
        form_frame = tk.Frame(self)
        form_frame.pack()

        tk.Label(form_frame, text='系列名称').grid(row=0)
        e1 = tk.Entry(form_frame, textvariable=self.series_name)
        e1.grid(row=0, column=1)

        tk.Label(form_frame, text='偏色数量').grid(row=1, column=0)
        radio_frame = tk.Frame(form_frame)
        radio_frame.grid(row=1, column=1)

        self.populate_radio_frame(radio_frame)
        self.fill_out_form()

    def populate_radio_frame(self, radio_frame):
        for i in range(5):
            value = 2 + i
            tk.Radiobutton(radio_frame, text=str(value), variable=self.num_shades, value=value,
                           command=self.build_shades).pack(side=tk.LEFT, padx=10)

    def fill_out_form(self):
        if self.master.is_updating:
            with shelve.open(self.master.DB_NAME) as db:
                selected_series = self.master.selected_series
                self.series_name.set(selected_series)
                self.num_shades.set(db[selected_series]['num_shades'])

    def build_user_actions(self):
        actions_frame = tk.Frame(self)
        actions_frame.pack()
        save_button_text = '保存' if self.master.is_updating else '创建'
        tk.Button(actions_frame, text=save_button_text, command=self.save_series).pack(side=tk.LEFT)
        tk.Button(actions_frame, text='取消', command=self.route_to_training_menu).pack(side=tk.LEFT)

    def save_series(self):
        series_name = self.series_name.get()
        num_shades = self.num_shades.get()
        if not self.valid_form_entry():
            self.prompt_failed_save()
        else:
            with shelve.open(self.master.DB_NAME) as db:
                db[series_name] = {'num_shades': num_shades}
            self.master.selected_series = series_name
            self.master.is_updating = False
            self.master.switch_frame(TrainingPage)

    def valid_form_entry(self):
        name = self.series_name.get()
        num_shades = self.num_shades.get()
        with shelve.open(self.master.DB_NAME) as db:
            if len(name) == 0 or num_shades == 0:
                return False
            # allows name to remain the same during update, doesn't allow new series to take an existing name
            elif name in db.keys() and name != self.master.selected_series:
                return False
            else:
                return True

    def prompt_failed_save(self):
        self.bell()
        prompt = tk.Toplevel(self)
        tk.Label(prompt, text='we were not able to create a tile series due to one of the following reasons: '
                              '\na) series name was taken; '
                              '\nb) series name was left empty; '
                              '\nc) no valid number of shades was selected').pack()
        tk.Button(prompt, text='确定', command=lambda: prompt.destroy()).pack()

    def route_to_training_menu(self):
        self.master.is_updating = False
        self.master.switch_frame(TrainingMenu)


class TrainingPage(Instance):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='训练页面').pack(pady=10)
        tk.Label(self, text=self.master.selected_series).pack(pady=10)

        self.build_preview()
        self.build_shades()

        tk.Button(self, text='开始').pack()
        tk.Button(self, text='结束', command=lambda: self.master.switch_frame(TrainingMenu)).pack()


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
