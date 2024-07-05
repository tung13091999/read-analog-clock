import handClockProcessor as hCP
from tkinter import Tk, Button, Scale, Label, HORIZONTAL
from tkinter.filedialog import askopenfilename
import displayImages

img_file_path = ''
canny_threshold1_scale = ...
canny_threshold2_scale = ...
hcc_dp_scale = ...
hcc_min_dist_scale = ...
hcc_param1_scale = ...
hcc_param2_scale = ...
approx_epsilon_scale = ...


def select_file():
    global img_file_path
    img_file_path = askopenfilename()


def detect_time():
    color_type = displayImages.ColorType
    display = displayImages.ImageDisplay(fig_size=(10, 8))

    color_img, gray_img, canny_edges = hCP.preprocessing_img(color_img_path=img_file_path,
                                                             blur_ksize=(5, 5),
                                                             canny_threshold1=canny_threshold1_scale.get(),
                                                             canny_threshold2=canny_threshold2_scale.get())
    display.add_img(color_type.GRAY, canny_edges, 221, 'Canny edges IMG')

    clock_centre, max_rad = hCP.find_max_clock_circle(color_img=color_img,
                                                      gray_img=gray_img,
                                                      dp=hcc_dp_scale.get(),
                                                      min_dist=hcc_min_dist_scale.get(),
                                                      param1=hcc_param1_scale.get(),
                                                      param2=hcc_param2_scale.get())
    # display.add_img(color_type.BGR, color_img, 222, 'Img with Max Circle')
    #
    # hand_contour = hCP.find_hand_contour(color_img=color_img,
    #                                      canny_edges=canny_edges,
    #                                      clock_centre=clock_centre)
    # display.add_img(color_type.BGR, color_img, 223, 'Img with Hand Contour')
    #
    # time_hand_vertices = hCP.find_hand_vertices(color_img=color_img,
    #                                             hand_contour=hand_contour,
    #                                             approx_epsilon=approx_epsilon_scale.get(),
    #                                             clock_centre=clock_centre)
    # time_value = hCP.get_time(color_img=color_img,
    #                           time_hand_vertices=time_hand_vertices,
    #                           clock_centre=clock_centre)
    # print(time_value)
    display.add_img(color_type.BGR, color_img, 224, 'Handled IMG')
    display.show()


def create_tkinter_slider(tkinter_root, label_name, start_val, end_val, default_val, orient_val):
    label = Label(tkinter_root, text=label_name)
    label.pack()
    scale = Scale(tkinter_root, from_=start_val, to=end_val, orient=orient_val)
    scale.set(default_val)
    scale.pack()
    return scale


def main():
    # Create tkinter root window
    root = Tk()
    root.title('Tuning parameters')

    # Create "Select file" button
    select_button = Button(root, text="Select file", command=select_file)
    select_button.pack()

    # Create slider for Canny threshold1
    global canny_threshold1_scale
    canny_threshold1_scale = create_tkinter_slider(root, 'Canny Threshold1', 0, 255, 100, HORIZONTAL)

    # Create slider for Canny threshold2
    global canny_threshold2_scale
    canny_threshold2_scale = create_tkinter_slider(root, 'Canny Threshold2', 0, 255, 150, HORIZONTAL)

    # Create slider for Hough Circle dp
    global hcc_dp_scale
    hcc_dp_scale = create_tkinter_slider(root, 'Hough CC dp', 1, 15, 1, HORIZONTAL)

    # Create slider for Hough Circle minDist
    global hcc_min_dist_scale
    hcc_min_dist_scale = create_tkinter_slider(root, 'Hough CC min dist', 10, 100, 10, HORIZONTAL)

    # Create slider for Hough Circle param1
    global hcc_param1_scale
    hcc_param1_scale = create_tkinter_slider(root, 'Hough CC param1', 0, 255, 50, HORIZONTAL)

    # Create slider for Hough Circle param2
    global hcc_param2_scale
    hcc_param2_scale = create_tkinter_slider(root, 'Hough CC param2', 0, 300, 100, HORIZONTAL)

    # Create slider for approxPolyDP epsilon
    global approx_epsilon_scale
    approx_epsilon_scale = create_tkinter_slider(root, 'approxPolyDP epsilon', 0, 100, 10, HORIZONTAL)

    detect_button = Button(root, text="Start detect", command=detect_time)
    detect_button.pack()
    # Run tkinter
    root.mainloop()


if __name__ == '__main__':
    main()
