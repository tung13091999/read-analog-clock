import cv2
import displayImages
import numpy as np
import handClockProcessor as hCP
from tkinter import Tk, Button, Scale, Label, HORIZONTAL, messagebox, ttk
from tkinter.filedialog import askopenfilename
import GUI
from tkinter.filedialog import askopenfilename

import handClockDetector as hCD

img_file_path = None
def select_file():
    global img_file_path
    img_file_path = askopenfilename()


def main():
    # Create tkinter root window
    control_panel = GUI.ControlPanel(window_name='Tuning params', window_size="400x600")

    # Create "Select file" button
    control_panel.add_button(text="Select file", command=select_file)
    control_panel.start_window()


if __name__ == '__main__':
    main()
