import tkinter as tk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # <create rest of your GUI here>
        # initialize, bind call backs, and place GUI widgets
        self.title = tk.Label(self, text='Hello World')
        self.title.pack(side='top', fill='x')


if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root).pack(side='top', fill='both', expand=True)
    root.mainloop()
