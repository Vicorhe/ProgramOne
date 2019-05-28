import shelve
import os
from sys import platform
import cv2 as cv
import tkinter as tk
from shutil import rmtree
from pathlib import Path
from FeatureExtraction.feature_set_a import get_statistics
from DataFrameOps import get_roi
if platform != "darwin":
    from Camera.CameraThread import CameraThread


PROMPT_GEOMETRY = '%dx%d%+d%+d' % (700, 400, 250, 125)
TITLE_FONT = ("Courier", 35)
MAIN_MENU_FONT = ("Courier", 35)
NAV_FONT = ("Courier", 25)
USER_ACTION_FONT = ("Courier", 20)
PROMPT_FONT = ("Courier", 25)
PROMPT_OPTION_FONT = ("Courier", 25)
LIST_FONT = ("Courier", 25)
INDICATOR_FONT = ("Courier", 30)
FORM_FONT = ("Courier", 35)


MAC_PICTURES_PATH = '/Users/victorhe/Pictures'
WINDOWS_PICTURES_PATH = 'C:\\Users\\van32\\Pictures'


class MainApplication(tk.Tk):
    DB_NAME = 'tiles'

    def __init__(self):
        super().__init__(className='颜色分拣系统')
        self.geometry('%dx%d%+d%+d' % (1100, 650, 150, 50))
        self._frame = None
        self.selected_series = None
        self.is_updating = False
        self.switch_frame(MainMenu)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.build_title()
        self.build_main_menu_option('运作区', OperatingMenu)
        self.build_main_menu_option('训练区', TrainingMenu)

    def build_title(self):
        tk.Label(self, text='主页', font=TITLE_FONT, height=2).grid(pady=10)

    def build_main_menu_option(self, text, destination):
        option = tk.Button(self, text=text, font=MAIN_MENU_FONT, width=6, height=2, borderwidth=10,
                           command=lambda: self.master.switch_frame(destination))
        option.grid(pady=5)


class BaseFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.prompt = None

    def build_title(self, title_text):
        title_label = tk.Label(self, text=title_text, font=TITLE_FONT, height=2)
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

    def build_prompt(self):
        self.bell()
        self.prompt = tk.Toplevel(self)
        self.prompt.geometry(PROMPT_GEOMETRY)

    def add_prompt_text(self, text):
        prompt_text = tk.Label(self.prompt, text=text, font=PROMPT_FONT)
        prompt_text.pack(pady=15)

    def add_prompt_action(self, text, hook):
        action = tk.Button(self.prompt, text=text, font=PROMPT_OPTION_FONT,
                           height=2, width=6, borderwidth=5, command=hook)
        action.pack(pady=10)


class SeriesList(BaseFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.my_list = None
        self.actions_frame = None
        self.prompt = None

    def build_list(self):
        list_container = tk.Frame(self)
        list_container.grid(row=1, column=0)

        self.my_list = tk.Listbox(list_container, selectmode=tk.SINGLE, font=LIST_FONT)
        self.my_list.bind('<<ListboxSelect>>', self.selection_callback)
        self.my_list.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(list_container, orient='vertical')
        scrollbar.config(command=self.my_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.my_list.config(yscrollcommand=scrollbar.set)

        self.populate_list()
        self.select_first_series()

    def selection_callback(self, _event):
        if self.my_list.curselection():
            series = self.my_list.get(self.my_list.curselection())
            self.master.selected_series = series

    def populate_list(self):
        with shelve.open(self.master.DB_NAME) as db:
            series_list = sorted(list(db.keys()))
            for series in series_list:
                self.my_list.insert(tk.END, series)

    def select_first_series(self):
        if self.my_list.size() > 0:
            self.my_list.selection_set(0)
            series = self.my_list.get(self.my_list.curselection())
            self.master.selected_series = series

    def selection_check_wrapper(self, hook):
        if self.master.selected_series:
            hook()
        else:
            self.prompt_no_series_selected()

    def prompt_no_series_selected(self):
        self.build_prompt()
        self.add_prompt_text('没有选到瓷砖系列')
        self.add_prompt_action('确定', self.prompt.destroy)

    def build_bottom_navigation(self):
        nav_button = tk.Button(self, text='主页', font=NAV_FONT, width=6, height=2, borderwidth=5,
                               command=lambda: self.master.switch_frame(MainMenu))
        nav_button.grid(row=2, column=0, columnspan=3, pady=10)

    def add_action(self, text, hook):
        action = tk.Button(self.actions_frame, text=text, font=USER_ACTION_FONT,
                           width=6, height=2, borderwidth=5, command=hook)
        action.pack(pady=5)

    def add_selection_based_action(self, text, hook):
        self.add_action(text, lambda: self.selection_check_wrapper(hook))


class SeriesInstance(BaseFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.top_preview_frame = None
        self.bottom_preview_frame = None
        self.actions_frame = None
        self.shades = list()
        self.prompt = None
        self.num_shades = tk.IntVar()
        self.model = None
        self.num_images_taken = tk.IntVar()
        self.batch_number = 0

        if self.master.selected_series:
            with shelve.open(self.master.DB_NAME) as db:
                selected_series = self.master.selected_series
                self.num_shades.set(db[selected_series]['num_shades'])
                self.batch_number = db[selected_series]['batch_number']
                self.model = db[selected_series]['model']

        base_path = MAC_PICTURES_PATH if platform == "darwin" else WINDOWS_PICTURES_PATH
        self.batch_path = Path(base_path)
        batch_extension = 'TrainingBatches/%s/batch_%d' % (self.master.selected_series, self.batch_number)
        self.batch_path = self.batch_path / batch_extension

    def build_preview(self):
        self.top_preview_frame = tk.Frame(self)
        self.top_preview_frame.grid(pady=15)

        self.bottom_preview_frame = tk.Frame(self)
        self.bottom_preview_frame.grid(pady=(0, 15))

        self.build_shades()

    def build_shades(self):
        # destroy previous shades
        self.shades = list()
        for child in self.top_preview_frame.winfo_children():
            child.destroy()
        for child in self.bottom_preview_frame.winfo_children():
            child.destroy()

        # build new shades
        for i in range(1, 1 + self.num_shades.get()):
            self.build_shade_option(i)

    def build_shade_option(self, option):
        parent = self.top_preview_frame if len(self.shades) < 3 else self.bottom_preview_frame
        option_frame = tk.Frame(parent)
        option_frame.pack(side=tk.LEFT, padx=6)
        label = tk.Label(option_frame, text=str(option), fg='white', bg='dark slate gray',
                         width=4, height=2, font=("Courier", 40), borderwidth=20)
        label.pack()
        self.shades.append(label)

    def build_user_actions_frame(self):
        self.actions_frame = tk.Frame(self)
        self.actions_frame.grid()

    def add_user_action(self, text, hook):
        user_action = tk.Button(self.actions_frame, text=text, font=("Courier", 30),
                                height=2, width=7, borderwidth=5, command=hook)
        user_action.pack(side=tk.LEFT, padx=10)

    def predict(self, image):
        if self.model is None:
            raise Exception('No model to run!')
        roi = get_roi(image)
        roi_hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        feature_vector = get_statistics(roi_hsv).reshape(1, -1)
        prediction = self.model.predict(feature_vector)
        return int(prediction[0])

    def highlight_shade(self, shade_id):
        for i, shade_option in enumerate(self.shades):
            if i == shade_id - 1:
                shade_option.configure(relief=tk.RIDGE)
            else:
                shade_option.configure(relief=tk.FLAT)


class OperatingMenu(SeriesList):
    def __init__(self, master):
        super().__init__(master)
        self.build_title('运作区')
        self.build_list()
        self.build_user_actions()
        self.build_bottom_navigation()

    def build_user_actions(self):
        self.actions_frame = tk.Frame(self)
        self.actions_frame.grid(row=1, column=1, padx=20)
        self.add_selection_based_action('确认', self.operate_hook)

    def operate_hook(self):
        self.master.switch_frame(OperatingSession)


class TrainingMenu(SeriesList):
    def __init__(self, master):
        super().__init__(master)
        self.build_title('训练区')
        self.build_list()
        self.build_user_actions()
        self.build_bottom_navigation()

    def build_user_actions(self):
        self.actions_frame = tk.Frame(self)
        self.actions_frame.grid(row=1, column=1, padx=20)
        self.add_action('新建', self.create_hook)
        self.add_selection_based_action('更改', self.update_hook)
        self.add_selection_based_action('删除', self.delete_hook)
        self.add_selection_based_action('训练', self.train_hook)

    def create_hook(self):
        self.master.selected_series = None
        self.master.switch_frame(FormPage)

    def update_hook(self):
        self.master.is_updating = True
        self.master.switch_frame(FormPage)

    def delete_hook(self):
        self.build_prompt()
        text = '您确定要把以下瓷砖系列删除码: ' + self.master.selected_series
        self.add_prompt_text(text)
        self.add_prompt_action('确定', self.delete_series)
        self.add_prompt_action('取消', self.prompt.destroy)

    def delete_series(self):
        with shelve.open(self.master.DB_NAME) as db:
            del db[self.master.selected_series]
            self.master.selected_series = None
        self.prompt.destroy()
        self.master.switch_frame(TrainingMenu)

    def train_hook(self):
        self.master.switch_frame(TrainingSession)


class FormPage(SeriesInstance):
    def __init__(self, master):
        super().__init__(master)
        self.series_name = tk.StringVar()
        self.build_title('瓷砖资料表格')
        self.build_form()
        self.fill_out_form()
        self.build_preview()
        self.build_user_actions()

    def build_form(self):
        form_frame = tk.Frame(self)
        form_frame.grid()
        tk.Label(form_frame, text='系列名称', font=FORM_FONT).grid(row=0, column=0)
        tk.Entry(form_frame, textvariable=self.series_name, font=FORM_FONT).grid(row=0, column=1, padx=15)
        tk.Label(form_frame, text='偏色数量', font=FORM_FONT).grid(row=1, column=0)
        radio_frame = tk.Frame(form_frame)
        radio_frame.grid(row=1, column=1, padx=10)
        self.populate_radio_frame(radio_frame)

    def populate_radio_frame(self, radio_frame):
        for i in range(5):
            value = 2 + i
            radio_option = tk.Radiobutton(radio_frame, text=str(value), value=value,
                                          variable=self.num_shades, font=FORM_FONT, width=3,
                                          command=self.build_shades)
            radio_option.pack(side=tk.LEFT, padx=10)

    def fill_out_form(self):
        if self.master.is_updating:
            with shelve.open(self.master.DB_NAME) as db:
                selected_series = self.master.selected_series
                self.series_name.set(selected_series)
                self.num_shades.set(db[selected_series]['num_shades'])

    def build_user_actions(self):
        self.build_user_actions_frame()
        save_button_text = '保存' if self.master.is_updating else '创建'
        self.add_user_action(save_button_text, self.save_series)
        self.add_user_action('取消', self.route_to_training_menu)

    def save_series(self):
        series_name = self.series_name.get()
        num_shades = self.num_shades.get()
        if not self.valid_form_entry():
            self.prompt_failed_save()
        else:
            with shelve.open(self.master.DB_NAME) as db:
                db[series_name] = {
                    'num_shades': num_shades,
                    'batch_number': self.batch_number,
                    'model': self.model
                }
            next_page = TrainingMenu if self.master.is_updating else TrainingSession
            self.master.is_updating = False
            self.master.selected_series = series_name
            self.master.switch_frame(next_page)

    def valid_form_entry(self):
        name = self.series_name.get()
        num_shades = self.num_shades.get()
        with shelve.open(self.master.DB_NAME) as db:
            if len(name) == 0 or num_shades == 0:
                return False
            # allows name to remain the same during update
            # doesn't allow new series to take an existing name
            elif name in db.keys() and name != self.master.selected_series:
                return False
            else:
                return True

    def prompt_failed_save(self):
        self.build_prompt()
        self.add_prompt_text('未能保存瓷砖系列，原因是以下其中之一:\na.系列名称已存在\nb.没有填写系列名称\nc.没有选到系列数量')
        self.add_prompt_action('确定', self.prompt.destroy)

    def route_to_training_menu(self):
        self.master.is_updating = False
        self.master.switch_frame(TrainingMenu)


class OperatingSession(SeriesInstance):
    def __init__(self, master):
        super().__init__(master)
        title_text = '系列名称: ' + self.master.selected_series
        self.build_title(title_text)
        self.build_preview()
        self.build_user_actions_frame()
        self.add_user_action('结束', self.leave_session)
        self.terminate_session = False
        if platform != 'darwin':
            self.appInstance = CameraThread(session=self, is_training_session=False)
        else:
            print('CameraThread NOT INITIATED')

    def leave_session(self):
        self.terminate_session = True
        if platform != 'darwin':
            self.appInstance.join()
        self.master.switch_frame(OperatingMenu)


class TrainingSession(SeriesInstance):
    def __init__(self, master):
        super().__init__(master)
        self.num_images_labeled = tk.IntVar()
        self.indicator_frame = None
        self.labels = list()
        title_text = self.master.selected_series + ' 训练进行中'
        self.build_title(title_text)
        self.build_preview()
        self.make_shades_into_choices()
        self.build_indicator_frame()
        self.build_user_actions_frame()
        self.add_user_action('结束训练', self.prompt_save_model)
        self.create_batch_directory()
        self.terminate_session = False
        if platform != "darwin":
            self.appInstance = CameraThread(session=self, is_training_session=True)
        else:
            print('CameraThread NOT INITIATED')

    def make_shades_into_choices(self):
        for shade in self.shades:
            shade.bind('<Enter>', self.on_enter)
            shade.bind('<Leave>', self.on_leave)
            shade.bind('<Button>', self.on_click)

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
        self.indicator_frame.grid(pady=10)

        tk.Label(self.indicator_frame, text='相片采集数量: ',
                 font=INDICATOR_FONT).grid(row=0, column=0)

        tk.Label(self.indicator_frame, textvariable=self.num_images_taken,
                 font=INDICATOR_FONT).grid(row=0, column=1)

        tk.Label(self.indicator_frame, text='已打标签数量: ',
                 font=INDICATOR_FONT).grid(row=1, column=0)

        tk.Label(self.indicator_frame, textvariable=self.num_images_labeled,
                 font=INDICATOR_FONT).grid(row=1, column=1)

    def prompt_save_model(self):
        self.terminate_session = True
        if platform != 'darwin':
            self.appInstance.join()
        self.build_prompt()
        text = '是否保存刚刚操作的 ' + self.master.selected_series + ' 系列版本?'
        self.add_prompt_text(text)
        self.add_prompt_action('确定', self.write_to_db)
        self.add_prompt_action('取消', self.clear_session_data)

    def write_to_db(self):
        self.delete_unlabeled_images()
        self.write_labels_file()
        # todo add training mechanism here
        with shelve.open(self.master.DB_NAME) as db:
            db[self.master.selected_series] = {
                'num_shades': self.num_shades.get(),
                'batch_number': self.batch_number + 1,
                'model': self.model
            }
        self.prompt.destroy()
        self.master.switch_frame(TrainingMenu)

    def delete_unlabeled_images(self):
        start = self.num_images_labeled.get()
        end = self.num_images_taken.get()
        print(start, end)
        for i in range(start, end):
            image_name = 'image_%d.BMP' % i
            image_path = str(self.batch_path / image_name)
            print('deleting image file at', image_path)
            os.remove(image_path)

    def write_labels_file(self):
        labels_path = self.batch_path / 'labels.txt'
        print('writing the following labels file at', labels_path)
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


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
