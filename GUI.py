import matplotlib.pyplot as plt
import cv2
from tkinter import Tk, Label, ttk, Scale, Button


class ColorType:
    BINARY = 0
    GRAY = 1
    BGR = 2


class ImageDisplay:

    def __init__(self, fig_size):
        self.fig = plt.figure(figsize=fig_size)
        self.subplots = []
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)

    def add_img(self, img_type, img, subplot_pos, axis_title):
        if img_type == ColorType.GRAY:
            ax = self.fig.add_subplot(subplot_pos)
            ax.imshow(img, cmap='gray')
            ax.set_title(axis_title)
            self.subplots.append(ax)
        elif img_type == ColorType.BINARY:
            ax = self.fig.add_subplot(subplot_pos)
            ax.imshow(img, cmap='binary')
            ax.set_title(axis_title)
            self.subplots.append(ax)
        elif img_type == ColorType.BGR:
            color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            ax = self.fig.add_subplot(subplot_pos)
            ax.imshow(color_img)
            ax.set_title(axis_title)
            self.subplots.append(ax)

    def on_click(self, event):
        if event.inaxes in self.subplots and event.dblclick:
            ax = event.inaxes
            img = ax.get_images()[0].get_array()

            # Hiển thị ảnh lớn
            plt.figure()
            plt.imshow(img, cmap='gray')
            plt.show()

    @staticmethod
    def show():
        plt.show()

    def close(self):
        plt.close(self.fig)


class ControlPanel:
    def __init__(self, window_name, window_size):
        self.root = Tk()
        self.root.title(window_name)
        self.root.geometry(window_size)
        self.root.resizable(False, False)

    def add_combobox(self, label_name, state, values, default_value):
        label = Label(self.root, text=label_name)
        label.pack()
        combo = ttk.Combobox(state=state, values=values)
        combo.set(default_value)
        combo.pack()
        return combo

    def add_slider(self, label_name, start_val, end_val, default_val, orient_val):
        label = Label(self.root, text=label_name)
        label.pack()
        scale = Scale(self.root, from_=start_val, to=end_val, orient=orient_val)
        scale.set(default_val)
        scale.pack()
        return scale

    def add_button(self, text, command):
        button = Button(self.root, text=text, command=command)
        button.pack()
        self.root.mainloop()
        return button

    def start_window(self):
        self.root.mainloop()

    def close_window(self):
        self.root.destroy()

