import handClockProcessor as hCP
from tkinter import Tk, Button, Scale, Label, HORIZONTAL, messagebox, ttk
from tkinter.filedialog import askopenfilename
import displayImages
import numpy as np

img_file_path = ''
kernel_size_combo = ...
dilation_iterations_scale = ...
thresh_value_scale = ...
thresh_max_scale = ...
approx_epsilon_scale_1 = ...
approx_epsilon_scale_2 = ...
min_hand_length_scale = ...


def select_file():
    global img_file_path
    img_file_path = askopenfilename()


def show_error_message(error_message):
    # Tạo cửa sổ thông báo lỗi
    window = Tk()
    window.withdraw()  # Ẩn cửa sổ chính

    # Hiển thị hộp thoại thông báo lỗi
    messagebox.showerror("Lỗi", error_message)


def detect_time():
    color_type = displayImages.ColorType
    display = displayImages.ImageDisplay(fig_size=(10, 8))

    color_img, gray_img, thresh_img, dilation_img = hCP.preprocessing_img(color_img_path=img_file_path,
                                                                          blur_ksize=(5, 5),
                                                                          dilation_kernel=kernel_size_combo.get(),
                                                                          dilation_iterations=dilation_iterations_scale.get(),
                                                                          thresh_value=thresh_value_scale.get(),
                                                                          thresh_max_value=thresh_max_scale.get())
    display.add_img(color_type.GRAY, thresh_img, 231, 'Thresh IMG')
    display.add_img(color_type.GRAY, dilation_img, 232, 'Dilation IMG')

    color_img, thresh_contours = hCP.find_contours(color_img=color_img, binary_img=thresh_img)
    color_img, dilation_contours = hCP.find_contours(color_img=color_img, binary_img=dilation_img)

    clock_centre, max_rad = hCP.find_max_circle(color_img=color_img, contours=thresh_contours)
    display.add_img(color_type.BGR, color_img, 233, 'Img with Max Circle')

    min_sec_hand_contour = hCP.find_hand_contour(color_img=color_img,
                                                 contours=thresh_contours,
                                                 clock_centre=clock_centre)
    hour_min_hand_contour = hCP.find_hand_contour(color_img=color_img,
                                                  contours=dilation_contours,
                                                  clock_centre=clock_centre)
    display.add_img(color_type.BGR, color_img, 234, 'Img with Hand Contour')

    possible_hour_min_hand_vertices = None
    try:
        possible_hour_min_hand_vertices = hCP.find_possible_hand_vertices(color_img=color_img,
                                                                          hand_contour=hour_min_hand_contour,
                                                                          approx_epsilon=approx_epsilon_scale_1.get(),
                                                                          clock_centre=clock_centre,
                                                                          min_hand_length=min_hand_length_scale.get())
        display.add_img(color_type.BGR, color_img, 235, 'Hour-Min Handled IMG')
    except Exception as e:
        print('Error:', e)
        show_error_message(str(e))

    possible_min_sec_hand_vertices = None
    try:
        possible_min_sec_hand_vertices = hCP.find_possible_hand_vertices(color_img=color_img,
                                                                         hand_contour=min_sec_hand_contour,
                                                                         approx_epsilon=approx_epsilon_scale_1.get(),
                                                                         clock_centre=clock_centre,
                                                                         min_hand_length=min_hand_length_scale.get())
    except Exception as e:
        print('Error:', e)
        show_error_message(str(e))

    print(f'possible min and sec vertices = {possible_min_sec_hand_vertices}')
    print(f'possible hour and min vertices = {possible_hour_min_hand_vertices}')

    second_hand_vertex = None
    minute_hand_vertex = None
    hour_hand_vertex = None

    try:
        minute_hand_vertex = possible_hour_min_hand_vertices[0][0]

        # Exception1: 3 hands overlapped each other
        if len(possible_min_sec_hand_vertices) > 1:
            second_hand_vertex = possible_min_sec_hand_vertices[1][0]
            hour_hand_vertex = possible_hour_min_hand_vertices[1][0]
        elif len(possible_min_sec_hand_vertices) == 1:
            second_hand_vertex = minute_hand_vertex
            hour_hand_vertex = minute_hand_vertex

        # Exception2: second hand overlaps minute hand
        sec_hand_length = np.sqrt(
            (clock_centre[0] - second_hand_vertex[0]) ** 2 + (clock_centre[1] - second_hand_vertex[1]) ** 2)
        hour_hand_length = np.sqrt(
            (clock_centre[0] - hour_hand_vertex[0]) ** 2 + (clock_centre[1] - hour_hand_vertex[1]) ** 2)
        if abs(sec_hand_length - hour_hand_length) < 10:
            second_hand_vertex = minute_hand_vertex
    except Exception as e:
        print('Error:', e)
        show_error_message(str(e))

    time_hand_vertices = [hour_hand_vertex, minute_hand_vertex, second_hand_vertex]
    print(f'time_hand_vertices = {time_hand_vertices}')

    time_value = None
    try:
        time_value = hCP.get_time(color_img=color_img,
                                  time_hand_vertices=time_hand_vertices,
                                  clock_centre=clock_centre)
    except Exception as e:
        print('Error:', e)
        show_error_message(str(e))

    print(time_value)
    display.add_img(color_type.BGR, color_img, 236, 'Handled IMG')
    display.show()


def create_tkinter_slider(tkinter_root, label_name, start_val, end_val, default_val, orient_val):
    label = Label(tkinter_root, text=label_name)
    label.pack()
    scale = Scale(tkinter_root, from_=start_val, to=end_val, orient=orient_val)
    scale.set(default_val)
    scale.pack()
    return scale


def create_tkinter_combobox(tkinter_root, label_name, state, values, default_value):
    label = Label(tkinter_root, text=label_name)
    label.pack()
    combo = ttk.Combobox(state=state, values=values)
    combo.set(default_value)
    combo.pack()
    return combo


def main():
    # Create tkinter root window
    root = Tk()
    root.title('Tuning parameters')

    # Create "Select file" button
    select_button = Button(root, text="Select file", command=select_file)
    select_button.pack()

    # Create Dilation kernel size combo
    global kernel_size_combo
    kernel_value = ['3x3', '5x5', '7x7']
    kernel_size_combo = create_tkinter_combobox(root, 'Dilation kernel size', 'readonly', kernel_value, '5x5')

    # Create Dilation iteration scale
    global dilation_iterations_scale
    dilation_iterations_scale = create_tkinter_slider(root, 'Dilation iterations', 1, 5, 1, HORIZONTAL)

    # Create slider for Canny threshold1
    global thresh_value_scale
    thresh_value_scale = create_tkinter_slider(root, 'Thresh value', 0, 255, 150, HORIZONTAL)

    # Create slider for Canny threshold2
    global thresh_max_scale
    thresh_max_scale = create_tkinter_slider(root, 'Thresh max value', 0, 255, 255, HORIZONTAL)

    # Create slider for approxPolyDP epsilon
    global approx_epsilon_scale_1
    approx_epsilon_scale_1 = create_tkinter_slider(root, 'approxPolyDP epsilon 1', 0, 100, 8, HORIZONTAL)

    # Create slider for approxPolyDP epsilon
    global approx_epsilon_scale_2
    approx_epsilon_scale_2 = create_tkinter_slider(root, 'approxPolyDP epsilon 2', 0, 100, 8, HORIZONTAL)

    global min_hand_length_scale
    min_hand_length_scale = create_tkinter_slider(root, 'Min hand length', 0, 200, 50, HORIZONTAL)

    detect_button = Button(root, text="Start detect", command=detect_time)
    detect_button.pack()
    # Run tkinter
    root.mainloop()


if __name__ == '__main__':
    main()
