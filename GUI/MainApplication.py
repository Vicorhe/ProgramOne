import shelve
import os
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
        self.prompt = None
        self.num_shades = tk.IntVar()
        self.batch_number = 0

        if self.master.selected_series:
            with shelve.open(self.master.DB_NAME) as db:
                self.num_shades.set(db[self.master.selected_series]['num_shades'])
                self.batch_number = db[self.master.selected_series]['batch_number']

        self.batch_path = '%s/TrainingBatches/%s/batch_%d' % \
                          (os.getcwd(), self.master.selected_series, self.batch_number)

    def build_preview(self):
        self.preview_frame = tk.Frame(self)
        self.preview_frame.pack(pady=15)
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
        option_frame.pack(side=tk.LEFT, padx=6)

        label = tk.Label(option_frame, text=str(option), fg='white', bg='dark slate gray', width=4, height=3,
                         borderwidth=10)
        label.pack()

    def prompt_save_model(self):
        self.bell()
        self.prompt = tk.Toplevel(self)
        text = '是否保存刚刚操作的 ' + self.master.selected_series + ' 系列版本?'
        tk.Label(self.prompt, text=text).pack()
        tk.Button(self.prompt, text='确定', command=self.alter_db_state).pack()
        tk.Button(self.prompt, text='取消', command=self.clear_session_data).pack()

    # todo implement backend logic
    def alter_db_state(self):
        with shelve.open(self.master.DB_NAME) as db:
            db[self.master.selected_series] = {
                'num_shades': self.num_shades.get(),
                'batch_number': self.batch_number + 1
            }
        self.prompt.destroy()
        self.master.switch_frame(TrainingMenu)

    # todo implement backend logic
    def clear_session_data(self):
        self.remove_batch()

        if self.batch_number == 0:
            with shelve.open(self.master.DB_NAME) as db:
                del db[self.master.selected_series]
        
        self.prompt.destroy()
        self.master.switch_frame(TrainingMenu)

    def remove_batch(self):
        try:
            os.rmdir(self.batch_path)
        except OSError:
            print("Deletion of the directory %s failed" % self.batch_path)
        else:
            print("Successfully deleted the directory %s" % self.batch_path)


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

        tk.Label(self, text='系列名称: ' + self.master.selected_series).pack(pady=10)

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

        tk.Button(self, text='主页', command=lambda: self.master.switch_frame(StartMenu)).grid(row=2, column=0,
                                                                                             columnspan=3, pady=10)

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
            del db[self.master.selected_series]
            self.master.selected_series = None
        self.prompt.destroy()
        self.master.switch_frame(TrainingMenu)

    def train_hook(self):
        self.master.switch_frame(TrainingSession)


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
                db[series_name] = {
                    'num_shades': num_shades,
                    'batch_number': self.batch_number
                }
            self.master.selected_series = series_name
            self.master.is_updating = False
            self.master.switch_frame(TrainingSession)

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
        tk.Label(prompt, text='未能保存瓷砖系列，原因是以下其中之一:'
                              '\na.  系列名称已存在    '
                              '\nb.  没有填写系列名称'
                              '\nc.  没有选到系列数量').pack()
        tk.Button(prompt, text='确定', command=lambda: prompt.destroy()).pack()

    def route_to_training_menu(self):
        self.master.is_updating = False
        self.master.switch_frame(TrainingMenu)


class TrainingSession(Instance):
    def __init__(self, master):
        super().__init__(master)

        self.num_images_taken = tk.IntVar()
        self.num_images_labeled = tk.IntVar()
        self.indicator_frame = None

        tk.Label(self, text=self.master.selected_series + ' 训练进行中').pack(pady=10)

        self.build_preview()
        self.build_dynamic_shades()
        self.build_indicator_frame()

        tk.Button(self, text='结束训练', command=self.prompt_save_model).pack()

        self.create_batch_directory()

        # todo remove this functionality when external trigger API incorporated
        self.master.bind('t', self.key)

    def build_indicator_frame(self):
        self.indicator_frame = tk.Frame(self)
        self.indicator_frame.pack()

        tk.Label(self.indicator_frame, text='相片采集数量: ').grid(row=0, column=0)
        tk.Label(self.indicator_frame, textvariable=self.num_images_taken).grid(row=0, column=1)

        tk.Label(self.indicator_frame, text='已打标签数量: ').grid(row=1, column=0)
        tk.Label(self.indicator_frame, textvariable=self.num_images_labeled).grid(row=1, column=1)

    # todo remove this key binding
    def key(self, _event=None):
        print('模拟外触取图')
        self.num_images_taken.set(self.num_images_taken.get() + 1)

    def build_dynamic_shades(self):
        # destroy previous shades
        for child in self.preview_frame.winfo_children():
            child.destroy()
        # build new shades
        for i in range(1, 1 + self.num_shades.get()):
            self.build_dynamic_shade_option(i)

    def build_dynamic_shade_option(self, option):
        option_frame = tk.Frame(self.preview_frame)
        option_frame.pack(side=tk.LEFT, padx=6)

        label = tk.Label(option_frame, text=str(option), fg='white', bg='dark slate gray', width=4, height=3,
                         borderwidth=10)
        label.pack()
        label.bind('<Enter>', self.on_enter)
        label.bind('<Leave>', self.on_leave)

        label.bind('<Button>', self.on_click)

    def on_enter(self, event):
        if self.num_images_labeled.get() < self.num_images_taken.get():
            event.widget.configure(relief=tk.RIDGE)

    @staticmethod
    def on_leave(event):
        event.widget.configure(relief=tk.FLAT)

    def on_click(self, event):
        if self.num_images_labeled.get() < self.num_images_taken.get():
            print('选中了色号' + event.widget['text'])
            self.num_images_labeled.set(self.num_images_labeled.get() + 1)

    def create_batch_directory(self):
        if not os.path.isdir(self.batch_path):
            try:
                os.makedirs(self.batch_path)
            except OSError:
                print("Creation of the directory %s failed" % self.batch_path)
            else:
                print("Successfully created the directory %s" % self.batch_path)


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
