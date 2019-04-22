import shelve
import os
import random
import numpy as np
import tkinter as tk
from shutil import rmtree
from threading import Thread
import mvsdk


class MainApplication(tk.Tk):
    DB_NAME = 'tiles'

    def __init__(self):
        super().__init__(className='颜色分拣系统')

        self._frame = None
        self.selected_series = None
        self.is_updating = False

        self.geometry('%dx%d%+d%+d' % (1100, 650, 150, 50))
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

        tk.Label(self, text='主页', font=("Courier", 35), height=2).grid(pady=10)
        tk.Button(self, text='运作区', font=("Courier", 35), width=6, height=2, borderwidth=10,
                  command=lambda: master.switch_frame(OperatingMenu)).grid(pady=10)
        tk.Button(self, text='训练区', font=("Courier", 35), width=6, height=2, borderwidth=10,
                  command=lambda: master.switch_frame(TrainingMenu)).grid()


class Listing(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.my_list = None
        self.prompt = None

    def build_list(self):
        list_frame = tk.Frame(self)
        list_frame.grid(row=1, column=0)

        self.my_list = tk.Listbox(list_frame, selectmode=tk.SINGLE, font=("Courier", 22))
        self.my_list.bind('<<ListboxSelect>>', self.selection_callback)
        self.my_list.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        scrollbar.config(command=self.my_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.my_list.config(yscrollcommand=scrollbar.set)

        self.populate_list()
        self.select_default_series()

    def selection_callback(self, _event):
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
            self.prompt.geometry('%dx%d%+d%+d' % (700, 400, 250, 125))
            tk.Label(self.prompt, text='没有选到瓷砖系列',
                     font=("Courier", 25)).pack(pady=15)
            tk.Button(self.prompt, text='确定', font=("Courier", 25), height=2, width=6, borderwidth=5,
                      command=self.prompt.destroy).pack(pady=10)


class Instance(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.preview_frame = None
        self.shades = list()
        self.prompt = None
        self.num_shades = tk.IntVar()
        self.num_images_taken = tk.IntVar()
        self.batch_number = 0

        if self.master.selected_series:
            with shelve.open(self.master.DB_NAME) as db:
                self.num_shades.set(db[self.master.selected_series]['num_shades'])
                self.batch_number = db[self.master.selected_series]['batch_number']

        self.batch_path = '%s\\TrainingBatches\\%s\\batch_%d' % \
                          (os.getcwd(), self.master.selected_series, self.batch_number)

    def build_preview(self):
        self.preview_frame = tk.Frame(self)
        self.preview_frame.pack(pady=15)
        self.build_shades()

    def build_shades(self):
        # destroy previous shades
        self.shades = list()
        for child in self.preview_frame.winfo_children():
            child.destroy()
        # build new shades
        for i in range(1, 1 + self.num_shades.get()):
            self.build_shade_option(i)

    def build_shade_option(self, option):
        option_frame = tk.Frame(self.preview_frame)
        option_frame.pack(side=tk.LEFT, padx=6)

        label = tk.Label(option_frame, text=str(option), fg='white', bg='dark slate gray',
                         width=4, height=2, font=("Courier", 40), borderwidth=20)
        label.pack()
        self.shades.append(label)

    def predict(self):
        return random.randint(1, self.num_shades.get())

    def highlight_shade(self, shade_id):
        for i, shade_option in enumerate(self.shades):
            if i == shade_id - 1:
                shade_option.configure(relief=tk.RIDGE)
            else:
                shade_option.configure(relief=tk.FLAT)


class OperatingMenu(Listing):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='运作区', font=("Courier", 35), height=2
                 ).grid(row=0, column=0, columnspan=3, pady=10)

        self.build_list()
        self.build_user_actions()

        tk.Button(self, text='主页', font=("Courier", 20), width=6, height=2, borderwidth=5,
                  command=lambda: master.switch_frame(StartMenu)).grid(row=2, column=0, columnspan=3, pady=10)

    def build_user_actions(self):
        actions_frame = tk.Frame(self)
        actions_frame.grid(row=1, column=1, padx=20)
        tk.Button(actions_frame, text='确认', font=("Courier", 15), width=6, height=2, borderwidth=5,
                  command=lambda: self.selection_based_prompt(self.operate_hook)).pack()

    def operate_hook(self):
        self.master.switch_frame(OperatingSession)


class OperatingSession(Instance):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='系列名称: ' + self.master.selected_series,
                 font=("Courier", 35), height=2).pack(pady=10)

        self.build_preview()
        self.build_shades()

        tk.Button(self, text='结束', font=("Courier", 30), height=2, width=7, borderwidth=5,
                  command=self.leave_session).pack()

        self.terminate_session = False
        self.appInstance = CameraApp(self, False)

    def leave_session(self):
        self.terminate_session = True
        self.appInstance.join()
        self.master.switch_frame(OperatingMenu)


class TrainingMenu(Listing):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text='训练区', font=("Courier", 35), height=2
                 ).grid(row=0, column=0, columnspan=3, pady=10)

        self.build_list()
        self.build_user_actions()

        tk.Button(self, text='主页', font=("Courier", 20), width=6, height=2, borderwidth=5,
                  command=lambda: self.master.switch_frame(StartMenu)).grid(row=2, column=0, columnspan=3, pady=10)

    def build_user_actions(self):
        actions_frame = tk.Frame(self)
        actions_frame.grid(row=1, column=1, padx=20)
        tk.Button(actions_frame, text='新建', font=("Courier", 15), width=6, height=2, borderwidth=5,
                  command=self.create_hook).pack(pady=5)
        tk.Button(actions_frame, text='更改', font=("Courier", 15), width=6, height=2, borderwidth=5,
                  command=lambda: self.selection_based_prompt(self.update_hook)).pack(pady=5)
        tk.Button(actions_frame, text='删除', font=("Courier", 15), width=6, height=2, borderwidth=5,
                  command=lambda: self.selection_based_prompt(self.delete_hook)).pack(pady=5)
        tk.Button(actions_frame, text='训练', font=("Courier", 15), width=6, height=2, borderwidth=5,
                  command=lambda: self.selection_based_prompt(self.train_hook)).pack(pady=5)

    def create_hook(self):
        self.master.selected_series = None
        self.master.switch_frame(FormPage)

    def update_hook(self):
        self.master.is_updating = True
        self.master.switch_frame(FormPage)

    def delete_hook(self):
        self.bell()
        self.prompt = tk.Toplevel(self)
        self.prompt.geometry('%dx%d%+d%+d' % (700, 400, 250, 125))
        tk.Label(self.prompt, text='您确定要把以下瓷砖系列删除码: ' + self.master.selected_series,
                 font=("Courier", 25)).pack(pady=15)
        tk.Button(self.prompt, text='确定', font=("Courier", 25), height=2, width=6, borderwidth=5,
                  command=self.delete_series).pack(pady=10)
        tk.Button(self.prompt, text='取消', font=("Courier", 25), height=2, width=6, borderwidth=5,
                  command=self.prompt.destroy).pack()

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

        tk.Label(self, text='瓷砖资料表格', font=("Courier", 35), height=2
                 ).pack(pady=10)

        self.build_form()
        self.build_preview()
        self.build_user_actions()

    def build_form(self):
        form_frame = tk.Frame(self)
        form_frame.pack()

        tk.Label(form_frame, text='系列名称', font=("Courier", 35), height=1
                 ).grid(row=0)
        e1 = tk.Entry(form_frame, textvariable=self.series_name, font=("Courier", 35))
        e1.grid(row=0, column=1, padx=15)

        tk.Label(form_frame, text='偏色数量', font=("Courier", 35), height=1
                 ).grid(row=1, column=0)
        radio_frame = tk.Frame(form_frame)
        radio_frame.grid(row=1, column=1, padx=10)

        self.populate_radio_frame(radio_frame)
        self.fill_out_form()

    def populate_radio_frame(self, radio_frame):
        for i in range(5):
            value = 2 + i
            tk.Radiobutton(radio_frame, text=str(value), variable=self.num_shades, value=value,
                           font=("Courier", 35), width=3,
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
        tk.Button(actions_frame, text=save_button_text, font=("Courier", 25), height=2, width=7, borderwidth=5,
                  command=self.save_series).pack(side=tk.LEFT, padx=10)
        tk.Button(actions_frame, text='取消', font=("Courier", 25), height=2, width=7, borderwidth=5,
                  command=self.route_to_training_menu).pack(side=tk.LEFT, padx=10)

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
            next_page = TrainingMenu if self.master.is_updating else TrainingSession
            self.master.is_updating = False
            self.master.switch_frame(next_page)

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
        prompt.geometry('%dx%d%+d%+d' % (700, 400, 250, 125))
        tk.Label(prompt, text='未能保存瓷砖系列，原因是以下其中之一:\na.系列名称已存在\nb.没有填写系列名称\nc.没有选到系列数量',
                 font=("Courier", 25)).pack(pady=15)
        tk.Button(prompt, text='确定', font=("Courier", 25), height=2, width=6, borderwidth=5,
                  command=lambda: prompt.destroy()).pack(pady=10)

    def route_to_training_menu(self):
        self.master.is_updating = False
        self.master.switch_frame(TrainingMenu)


class TrainingSession(Instance):
    def __init__(self, master):
        super().__init__(master)

        self.num_images_labeled = tk.IntVar()
        self.indicator_frame = None
        self.labels = list()

        tk.Label(self, text=self.master.selected_series + ' 训练进行中',
                 font=("Courier", 35), height=2).pack(pady=10)

        self.build_preview()
        self.build_dynamic_shades()
        self.build_indicator_frame()

        tk.Button(self, text='结束训练', font=("Courier", 25), height=2, width=7, borderwidth=5,
                  command=self.prompt_save_model).pack()

        self.create_batch_directory()

        self.terminate_session = False
        self.appInstance = CameraApp(self, True)

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

        label = tk.Label(option_frame, text=str(option), fg='white', bg='dark slate gray',
                         width=4, height=2, font=("Courier", 40), borderwidth=20)
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
            label = event.widget['text']
            print('labeled', label)
            self.labels.append(label)
            self.num_images_labeled.set(self.num_images_labeled.get() + 1)

    def build_indicator_frame(self):
        self.indicator_frame = tk.Frame(self)
        self.indicator_frame.pack(pady=10)

        tk.Label(self.indicator_frame, text='相片采集数量: ',
                 font=("Courier", 30), height=1).grid(row=0, column=0)
        tk.Label(self.indicator_frame, textvariable=self.num_images_taken,
                 font=("Courier", 30), height=1).grid(row=0, column=1)

        tk.Label(self.indicator_frame, text='已打标签数量: ',
                 font=("Courier", 30), height=1).grid(row=1, column=0)
        tk.Label(self.indicator_frame, textvariable=self.num_images_labeled,
                 font=("Courier", 30), height=1).grid(row=1, column=1)

    def prompt_save_model(self):
        self.terminate_session = True
        self.appInstance.join()
        self.bell()
        self.prompt = tk.Toplevel(self)
        self.prompt.geometry('%dx%d%+d%+d' % (700, 400, 250, 125))
        text = '是否保存刚刚操作的 ' + self.master.selected_series + ' 系列版本?'
        tk.Label(self.prompt, text=text, font=("Courier", 25)).pack(pady=15)
        tk.Button(self.prompt, text='确定', font=("Courier", 25), height=2, width=6, borderwidth=5,
                  command=self.alter_db_state).pack(pady=10)
        tk.Button(self.prompt, text='取消', font=("Courier", 25), height=2, width=6, borderwidth=5,
                  command=self.clear_session_data).pack()

    def alter_db_state(self):
        self.write_labels_file()
        with shelve.open(self.master.DB_NAME) as db:
            db[self.master.selected_series] = {
                'num_shades': self.num_shades.get(),
                'batch_number': self.batch_number + 1
            }
        self.prompt.destroy()
        self.master.switch_frame(TrainingMenu)

    def write_labels_file(self):
        labels_path = '%s/labels.txt' % self.batch_path
        print('writing the following labels file at', labels_path)
        print(self.labels)
        with open(labels_path, 'w+') as file:
            file.write(' '.join(self.labels))

    def clear_session_data(self):
        self.remove_batch()

        if self.batch_number == 0:
            with shelve.open(self.master.DB_NAME) as db:
                del db[self.master.selected_series]

        self.prompt.destroy()
        self.master.selected_series = None
        self.master.switch_frame(TrainingMenu)

    def remove_batch(self):
        try:
            rmtree(self.batch_path)
        except OSError:
            print("Deletion of the directory %s failed" % self.batch_path)
        else:
            print("Successfully deleted the directory %s" % self.batch_path)

    def create_batch_directory(self):
        if not os.path.isdir(self.batch_path):
            try:
                os.makedirs(self.batch_path)
            except OSError:
                print("Creation of the directory %s failed" % self.batch_path)
            else:
                print("Successfully created the directory %s" % self.batch_path)


class CameraApp(Thread):
    def __init__(self, session, isTraining):
        Thread.__init__(self)
        self.session = session
        self.camera = None
        self.image_buffer = None
        if isTraining:
            self.camera_mainloop = self.training_mainloop
        else:
            self.camera_mainloop = self.operating_mainloop
        self.start()

    def run(self):
        try:
            self.camera_setup()
            self.allocate_image_buffer()
            while True:
                if self.session.terminate_session:
                    print('Session Terminated')
                    break
                self.camera_mainloop()
        finally:
            self.camera_breakdown()

    def camera_setup(self):
        device_list = mvsdk.CameraEnumerateDevice()
        num_devices = len(device_list)
        if num_devices < 1:
            raise Exception("No Camera Connected")

        device_info = device_list[0]
        try:
            self.camera = mvsdk.CameraInit(device_info, -1, -1)
        except mvsdk.CameraException as e:
            raise Exception("Camera Init Failed")

        # run camera API
        mvsdk.CameraPlay(self.camera)

    def allocate_image_buffer(self):
        camera_capability = mvsdk.CameraGetCapability(self.camera)
        frame_buffer_size = camera_capability.sResolutionRange.iWidthMax * camera_capability.sResolutionRange.iHeightMax * 3
        self.image_buffer = mvsdk.CameraAlignMalloc(frame_buffer_size, 16)

    def training_mainloop(self):
        try:
            p_raw_data, frame_head = mvsdk.CameraGetImageBuffer(self.camera, 500)
            mvsdk.CameraImageProcess(self.camera, p_raw_data, self.image_buffer, frame_head)
            mvsdk.CameraReleaseImageBuffer(self.camera, p_raw_data)

            # save the image to disk
            n = self.session.num_images_taken.get()
            image_path = '%s\\image_%d.BMP' % (self.session.batch_path, n)
            status = mvsdk.CameraSaveImage(self.camera, image_path, self.image_buffer, frame_head, mvsdk.FILE_BMP, 100)
            if status == mvsdk.CAMERA_STATUS_SUCCESS:
                print("Image Save Success at", image_path)
            else:
                print("Image Save Fail")
            self.session.num_images_taken.set(n + 1)

        except mvsdk.CameraException as e:
            pass

    def operating_mainloop(self):
        try:
            p_raw_data, frame_head = mvsdk.CameraGetImageBuffer(self.camera, 500)
            mvsdk.CameraImageProcess(self.camera, p_raw_data, self.image_buffer, frame_head)
            mvsdk.CameraReleaseImageBuffer(self.camera, p_raw_data)

            # convert image to model friendly formats
            n = self.session.num_images_taken.get()

            frame_data = (mvsdk.c_ubyte * frame_head.uBytes).from_address(self.image_buffer)
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = frame.reshape((frame_head.iHeight, frame_head.iWidth, 3))

            p = self.session.predict()
            print(p)
            self.session.highlight_shade(p)

            self.session.num_images_taken.set(n + 1)

        except mvsdk.CameraException as e:
            pass

    def camera_breakdown(self):
        print('cleanup ing')
        mvsdk.CameraUnInit(self.camera)
        mvsdk.CameraAlignFree(self.image_buffer)


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
