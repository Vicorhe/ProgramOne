import shelve
import tkinter as tk


DB_NAME = 'tiles'


class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self, className='颜色分拣系统')

        self._frame = None
        self.selected_series = None
        self.is_updating = False

        self.switch_frame(StartMenu)
        self.geometry('400x260')

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text='主页').grid(pady=10)

        tk.Button(self, text='运作区',
                  command=lambda: master.switch_frame(OperatingMenu)).grid()

        tk.Button(self, text='训练区',
                  command=lambda: master.switch_frame(TrainingMenu)).grid()


class OperatingMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        self.my_list = None
        self.prompt = None

        tk.Label(self, text='运作区').grid(row=0, column=0, columnspan=3, pady=10)

        self.build_list()
        self.build_user_actions()

        tk.Button(self, text='主页', command=lambda: master.switch_frame(StartMenu)).grid(row=2, column=0, columnspan=3)

    def build_list(self):
        list_frame = tk.Frame(self)
        list_frame.grid(row=1, column=0)

        self.my_list = tk.Listbox(list_frame, font=('Helvetica', 12), selectmode=tk.SINGLE)
        self.my_list.bind('<<ListboxSelect>>', self.selection_callback)
        self.my_list.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        scrollbar.config(command=self.my_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.my_list.config(yscrollcommand=scrollbar.set)

        with shelve.open(DB_NAME) as db:
            series_list = list(db.keys())

            for series in series_list:
                self.my_list.insert(tk.END, series)

            if len(series_list) > 0:
                self.my_list.selection_set(0)
                series = self.my_list.get(self.my_list.curselection())
                print(series, 'selected')
                self.master.selected_series = series

    def selection_callback(self, event):
        if self.my_list.curselection():
            series = self.my_list.get(self.my_list.curselection())
            print(series, 'selected')
            self.master.selected_series = series

    def build_user_actions(self):
        actions_frame = tk.Frame(self)
        actions_frame.grid(row=1, column=1)

        tk.Button(actions_frame, text='确认', command=self.prompt_operate).pack()

    def prompt_operate(self):
        if self.master.selected_series:
            self.master.switch_frame(OperatingPage)
        else:
            self.bell()
            self.prompt = tk.Toplevel(self)
            tk.Label(self.prompt, text='no series was selected').pack()
            tk.Button(self.prompt, text='确定', command=self.prompt.destroy).pack()


class OperatingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        self.preview_frame = None
        self.num_shades = None

        with shelve.open(DB_NAME) as db:
            self.num_shades = db[self.master.selected_series]['num_shades']

        tk.Label(self, text='运行页面').pack(pady=10)
        tk.Label(self, text=self.master.selected_series).pack(pady=10)

        self.build_preview()
        self.build_shades()

        tk.Button(self, text='开始').pack()
        tk.Button(self, text='结束', command=lambda: self.master.switch_frame(OperatingMenu)).pack()

    def build_preview(self):
        self.preview_frame = tk.Frame(self)
        self.preview_frame.pack()

    def build_shades(self):
        # destroy previous shades
        for child in self.preview_frame.winfo_children():
            child.destroy()
        # build new shades
        for i in range(1, 1 + self.num_shades):
            self.build_shade_option(i)

    def build_shade_option(self, option):
        option_frame = tk.Frame(self.preview_frame)
        option_frame.pack(side=tk.LEFT)
        tk.Label(option_frame, text=str(option), fg='white', bg='green', bd=1, width=6, height=6).pack(padx=6)


class TrainingMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        self.my_list = None
        self.prompt = None

        tk.Label(self, text='训练区').grid(row=0, column=0, columnspan=3, pady=10)

        self.build_list()
        self.build_user_actions()

        tk.Button(self, text='主页', command=lambda: self.master.switch_frame(StartMenu)).grid(row=2, column=0, columnspan=3, pady=10)

    def build_list(self):

        list_frame = tk.Frame(self)
        list_frame.grid(row=1, column=0)

        self.my_list = tk.Listbox(list_frame, font=('Helvetica', 12), selectmode=tk.SINGLE)
        self.my_list.bind('<<ListboxSelect>>', self.selection_callback)
        self.my_list.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        scrollbar.config(command=self.my_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.my_list.config(yscrollcommand=scrollbar.set)

        with shelve.open(DB_NAME) as db:
            series_list = list(db.keys())

            for series in series_list:
                self.my_list.insert(tk.END, series)

            if len(series_list) > 0:
                self.my_list.selection_set(0)
                series = self.my_list.get(self.my_list.curselection())
                print(series, 'selected')
                self.master.selected_series = series

    def selection_callback(self, event):
        if self.my_list.curselection():
            series = self.my_list.get(self.my_list.curselection())
            print(series, 'selected')
            self.master.selected_series = series

    def build_user_actions(self):
        actions_frame = tk.Frame(self)
        actions_frame.grid(row=1, column=1)
        tk.Button(actions_frame, text='新建', command=self.route_to_creation_form).pack()
        tk.Button(actions_frame, text='更改', command=self.prompt_update).pack()
        tk.Button(actions_frame, text='删除', command=self.prompt_delete).pack()
        tk.Button(actions_frame, text='训练', command=self.prompt_train).pack()

    def route_to_creation_form(self):
        self.master.selected_series = None
        self.master.switch_frame(FormPage)

    def prompt_update(self):
        if self.master.selected_series:
            self.master.is_updating = True
            self.master.switch_frame(FormPage)
        else:
            self.bell()
            self.prompt = tk.Toplevel(self)
            tk.Label(self.prompt, text='no series was selected').pack()
            tk.Button(self.prompt, text='确定', command=self.prompt.destroy).pack()

    def prompt_delete(self):
        self.bell()
        self.prompt = tk.Toplevel(self)
        if self.master.selected_series:
            tk.Label(self.prompt, text='are you sure you want to delete tile series ' + self.master.selected_series).pack()
            tk.Button(self.prompt, text='确定', command=self.delete_series).pack()
            tk.Button(self.prompt, text='取消', command=self.prompt.destroy).pack()
        else:
            tk.Label(self.prompt, text='no series was selected').pack()
            tk.Button(self.prompt, text='确定', command=self.prompt.destroy).pack()

    def delete_series(self):
        self.prompt.destroy()
        with shelve.open(DB_NAME) as db:
            print('deleting', self.master.selected_series)
            del db[self.master.selected_series]
            self.master.selected_series = None
        self.master.switch_frame(TrainingMenu)

    def prompt_train(self):
        if self.master.selected_series:
            self.master.switch_frame(TrainingPage)
        else:
            self.bell()
            self.prompt = tk.Toplevel(self)
            tk.Label(self.prompt, text='no series was selected').pack()
            tk.Button(self.prompt, text='确定', command=self.prompt.destroy).pack()


class FormPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        self.preview_frame = None
        self.series_name = tk.StringVar()
        self.num_shades = tk.IntVar()

        self.build_form()
        self.build_preview()
        self.build_user_actions()

    def build_form(self):
        tk.Label(self, text='瓷砖资料表格').pack(pady=10)
        form_frame = tk.Frame(self)
        form_frame.pack()
        tk.Label(form_frame, text='系列名称').grid(row=0)
        e1 = tk.Entry(form_frame, textvariable=self.series_name)
        e1.grid(row=0, column=1)
        tk.Label(form_frame, text='偏色数量').grid(row=1, column=0)
        radio_frame = tk.Frame(form_frame)
        radio_frame.grid(row=1, column=1)
        for i in range(5):
            value = 2 + i
            tk.Radiobutton(radio_frame, text=str(value), variable=self.num_shades, value=value,
                           command=self.build_shades).pack(side=tk.LEFT, padx=10)
        if self.master.is_updating:
            with shelve.open(DB_NAME) as db:
                selected_series = self.master.selected_series
                self.series_name.set(selected_series)
                self.num_shades.set(db[selected_series]['num_shades'])

    def build_preview(self):
        self.preview_frame = tk.Frame(self)
        self.preview_frame.pack()

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
        tk.Label(option_frame, text=str(option), fg='white', bg='green', bd=1, width=6, height=6).pack(padx=6)

    def build_user_actions(self):
        options_frame = tk.Frame(self)
        options_frame.pack()
        if self.master.is_updating:
            tk.Button(options_frame, text='保存', command=self.save_changes).pack(side=tk.LEFT)
        else:
            tk.Button(options_frame, text='创建', command=self.create_new_series).pack(side=tk.LEFT)
        tk.Button(options_frame, text='取消', command=self.route_to_training_menu).pack(side=tk.LEFT)

    def save_changes(self):
        series_name = self.series_name.get()
        num_shades = self.num_shades.get()
        if not self.valid_name() or num_shades < 2:
            self.prompt_unsuccessful()
        else:
            with shelve.open(DB_NAME) as db:
                db[series_name] = {
                    'num_shades': num_shades
                }

            self.master.selected_series = series_name
            self.master.is_updating = False
            self.master.switch_frame(TrainingPage)

    def create_new_series(self):
        series_name = self.series_name.get()
        num_shades = self.num_shades.get()
        if not self.valid_name() or num_shades < 2:
            self.prompt_unsuccessful()
        else:
            with shelve.open(DB_NAME) as db:
                db[series_name] = {
                    'num_shades': num_shades
                }

            self.master.selected_series = series_name
            self.master.switch_frame(TrainingPage)

    def prompt_unsuccessful(self):
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

    def valid_name(self):
        name = self.series_name.get()
        with shelve.open(DB_NAME) as db:
            if len(name) == 0:
                return False
            elif name in db.keys() and name != self.master.selected_series:
                return False
            else:
                return True


class TrainingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        self.preview_frame = None
        self.num_shades = None

        with shelve.open(DB_NAME) as db:
            self.num_shades = db[self.master.selected_series]['num_shades']

        tk.Label(self, text='训练页面').pack(pady=10)
        tk.Label(self, text=self.master.selected_series).pack(pady=10)

        self.build_preview()
        self.build_shades()

        tk.Button(self, text='开始').pack()
        tk.Button(self, text='结束', command=lambda: self.master.switch_frame(TrainingMenu)).pack()

    def build_preview(self):
        self.preview_frame = tk.Frame(self)
        self.preview_frame.pack()

    def build_shades(self):
        # destroy previous shades
        for child in self.preview_frame.winfo_children():
            child.destroy()
        # build new shades
        for i in range(1, 1 + self.num_shades):
            self.build_shade_option(i)

    def build_shade_option(self, option):
        option_frame = tk.Frame(self.preview_frame)
        option_frame.pack(side=tk.LEFT)
        tk.Label(option_frame, text=str(option), fg='white', bg='green', bd=1, width=6, height=6).pack(padx=6)



if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
