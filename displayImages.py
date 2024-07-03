import matplotlib.pyplot as plt
import cv2


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
