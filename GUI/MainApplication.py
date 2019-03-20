import tkinter as tk


class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self, className='颜色分拣系统')
        self._frame = None
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

        tk.Label(self, text='运作区').grid(row=0, column=0, columnspan=3, pady=10)

        self.build_list()
        self.build_options()

        tk.Button(self, text='主页', command=lambda: master.switch_frame(StartMenu)).grid(row=2, column=0, columnspan=3)

    def build_list(self):
        list_frame = tk.Frame(self)
        list_frame.grid(row=1, column=0, columnspan=2)

        my_list = tk.Listbox(list_frame, font=('Helvetica', 12))
        my_list.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        scrollbar.config(command=my_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        my_list.config(yscrollcommand=scrollbar.set)

        for series in ['象牙白', '象牙黑', '象牙蓝']:
            my_list.insert(tk.END, series)

    def build_options(self):
        options_frame = tk.Frame(self)
        options_frame.grid(row=1, column=2)

        tk.Button(options_frame, text='确认', command=lambda: self.master.switch_frame(OperatingPage)).pack()


class OperatingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        tk.Label(self, text='运行页面').grid(pady=10)

        self.build_color_instances(3)

        tk.Button(self, text='开始').grid()
        tk.Button(self, text='结束', command=lambda: self.master.switch_frame(OperatingMenu)).grid()

    def build_color_instances(self, n):
        color_instances_frame = tk.Frame(self)
        color_instances_frame.grid()

        for i in range(n):
            self.build_color_option(color_instances_frame, i)

    def build_color_option(self, parent, option):
        option_frame = tk.Frame(parent)
        option_frame.pack(side=tk.LEFT)

        tk.Label(option_frame, text=str(option), fg='white', bg='blue', bd=1, width=6, height=6).pack(padx=6)


class TrainingMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        tk.Label(self, text='训练区').grid(row=0, column=0, columnspan=3, pady=10)

        self.build_list()
        self.build_options()

        tk.Button(self, text='主页', command=lambda: self.master.switch_frame(StartMenu)).grid(row=2, column=0, columnspan=3, pady=10)

    def build_list(self):

        list_frame = tk.Frame(self)
        list_frame.grid(row=1, column=0)

        my_list = tk.Listbox(list_frame, font=('Helvetica', 12))
        my_list.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        scrollbar.config(command=my_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        my_list.config(yscrollcommand=scrollbar.set)

        for series in ['象牙白', '象牙黑', '象牙蓝'] * 7:
            my_list.insert(tk.END, series)

    def build_options(self):

        options_frame = tk.Frame(self)
        options_frame.grid(row=1, column=1)

        tk.Button(options_frame, text='新建', command=lambda: self.master.switch_frame(FormPage)).pack()
        tk.Button(options_frame, text='更改', command=lambda: self.master.switch_frame(FormPage)).pack()
        tk.Button(options_frame, text='删除').pack()
        tk.Button(options_frame, text='训练', command=lambda: self.master.switch_frame(TrainingPage)).pack()


class FormPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        tk.Label(self, text='瓷砖资料表格').pack(pady=10)
        self.build_color_instances(3)
        self.build_form()
        self.build_options()
        tk.Button(self, text='主页', command=lambda: self.master.switch_frame(StartMenu)).pack(pady=10)

    def build_form(self):
        form_frame = tk.Frame(self)
        form_frame.pack()

        tk.Label(form_frame, text='系列名称').grid(row=0)
        e1 = tk.Entry(form_frame)
        e1.grid(row=0, column=1)

        radio_frame = tk.Frame(form_frame)
        radio_frame.grid(row=1, column=0, columnspan=2)
        v = tk.IntVar()
        for i in range(5):
            val = 2 + i
            tk.Radiobutton(radio_frame, text=str(val), variable=v, value=val).pack(side=tk.LEFT, padx=10)

    def build_options(self):
        options_frame = tk.Frame(self)
        options_frame.pack()
        tk.Button(options_frame, text='确认', command=lambda: self.master.switch_frame(TrainingPage)).pack(side=tk.LEFT)
        tk.Button(options_frame, text='取消', command=lambda: self.master.switch_frame(TrainingMenu)).pack(side=tk.LEFT)

    def build_color_instances(self, n):
        color_instances_frame = tk.Frame(self)
        color_instances_frame.pack()

        for i in range(n):
            self.build_color_option(color_instances_frame, i)

    def build_color_option(self, parent, option):
        option_frame = tk.Frame(parent)
        option_frame.pack(side=tk.LEFT)

        tk.Label(option_frame, text=str(option), fg='white', bg='blue', bd=1, width=6, height=6).pack(padx=6)


class TrainingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master

        tk.Label(self, text='训练页面').grid(pady=10)

        self.build_color_instances(3)

        tk.Button(self, text='开始').grid()
        tk.Button(self, text='结束', command=lambda: self.master.switch_frame(TrainingMenu)).grid()

    def build_color_instances(self, n):
        color_instances_frame = tk.Frame(self)
        color_instances_frame.grid()

        for i in range(n):
            self.build_color_option(color_instances_frame, i)

    def build_color_option(self, parent, option):
        option_frame = tk.Frame(parent)
        option_frame.pack(side=tk.LEFT)

        tk.Label(option_frame, text=str(option), fg='white', bg='blue', bd=1, width=6, height=6).pack(padx=6)


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
