import tkinter as tk
from tkinter import LEFT, RIGHT


class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self, className='颜色分拣系统')
        self._frame = None
        self.switch_frame(StartPage)
        self.geometry('300x200')

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text='主页').grid(pady=10)

        tk.Button(self, text='训练',
                  command=lambda: master.switch_frame(TrainingPage)).grid()

        tk.Button(self, text='运作',
                  command=lambda: master.switch_frame(OperatingPage)).grid()


class TrainingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text='训练区').grid(pady=10, row=0, column=0, columnspan=3)

        self.build_list()

        tk.Button(self, text='主页', command=lambda: master.switch_frame(StartPage)).grid(row=4, column=0, columnspan=3, pady=10)

    def build_list(self):

        list_frame = tk.Frame(self)
        list_frame.grid(row=1)

        my_list = tk.Listbox(list_frame, width=20, height=7, font=("Helvetica", 12))
        my_list.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        scrollbar.config(command=my_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        my_list.config(yscrollcommand=scrollbar.set)

        for series in ['象牙白', '象牙黑', '象牙蓝']:
            my_list.insert(tk.END, series)


class OperatingPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text='运作区').pack(side='top', fill='x', pady=10)

        tk.Button(self, text='主页', command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
