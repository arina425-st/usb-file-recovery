# User manually introduces bytes read at a time
# recommended: 4096
# User manually introduces file path
# GUI
import os
import threading
import tkinter
from tkinter import ttk

import byte_reading
import file_saving

tkinter_object = None
output_box = None
progress_bar = None
output_folder = None
start_button = None


def start_recovery_thread(usb_path):
    """
    Starts a separate thread for the GUI in order to prevent
    the program from freezing. Also disables the start recovery button
    in order to prevent a second press during the scan and mess up the
    already read / recovered files.
    :param usb_path: (string) the path of the USB drive
    :return: None
    """
    start_button.config(state=tkinter.DISABLED)
    thread = threading.Thread(target=byte_reading.read_bytes_from_usb, args=(usb_path, ))
    thread.start()


def enable_start_recovery_button():
    """
    Gets called at the end of the scan,
    and enables the start recovery button.
    :return:
    """
    start_button.config(state=tkinter.NORMAL)


def display_gui():
    """
    Displays the GUI window.
    :return: None
    """

    global tkinter_object, output_box, progress_bar, output_folder, start_button

    tkinter_object = tkinter.Tk()
    # Elements start on column 0,
    # but move by weight=1 as the window is resized.
    tkinter_object.columnconfigure(0, weight=1)

    # Add GUI title
    tkinter_object.title("USB File Recovery")

    # Add frame for aligning labels + text entry / progress bar
    input_frame = tkinter.Frame(tkinter_object)
    input_frame.grid(row=1, column=0, pady=(10, 0))

    # Add text
    # sticky="w" -> w - West -> text on the left instead of centered
    enter_usb_file_path_text = tkinter.Label(input_frame,
                                             text=r'Enter the USB file path here (Format example: "\\.\E:"):',
                                             font=("calibre", 10, "normal"))
    enter_usb_file_path_text.grid(row=1, column=0, pady=(10, 5), sticky="w")

    # Add field for entering host IP
    usb_file_path_entry = tkinter.Entry(input_frame, font=("calibre", 10, "normal"), width=30, justify="left")
    # pady=(0, 15): add 0 pixels above and 15 pixels below the field
    usb_file_path_entry.grid(row=2, column=0, pady=(0, 15))

    # Add label for the progress bar:
    progress_bar_label = tkinter.Label(input_frame, text="Progress:",
                                       font=("calibre", 10, "normal"))
    progress_bar_label.grid(row=4, column=0, pady=(10, 0), sticky="w")

    # Add progress bar
    progress_bar = ttk.Progressbar(input_frame, orient="horizontal", length=210, mode="determinate")
    # Add the progress bar in the GUI window:
    # pady=20: add 20 pixels above and below the progress bar,
    # such that it won't be glued to other elements.
    progress_bar.grid(row=5, column=0, pady=(0, 20))

    # DRAFT: Use a temporary output put for saving the recovered file.
    # TODO: Save the recovered file on the USB disk.
    output_folder = "recovered_files"
    # exist_ok=True - do not throw error if file already exists
    os.makedirs(output_folder, exist_ok=True)

    # Add button to start the vulnerability scanner (+ progress bar),
    # reading the input entered by the user in the entry field.
    # CAREFUL: Read user input when the function is called (i.e. within the start button),
    # otherwise the input field remains empty.

    # CAREFUL: Start a separate thread for the GUI, otherwise,
    # the program will freeze for heavy tasks like downloading files.
    start_button = tkinter.Button(tkinter_object, text="Start File Recovery",
                                  command=lambda: start_recovery_thread(usb_file_path_entry.get()))
    start_button.grid(row=6, column=0, pady=10)

    # Add frame to hold the output box + scrollbar together:
    output_frame = tkinter.Frame(tkinter_object)
    output_frame.grid(row=7, column=0, padx=20, pady=(10, 20))

    # Add scrollbar as child of output_frame not of main GUI window
    scrollbar = tkinter.Scrollbar(output_frame)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    # Text box for showing results:
    # yscrollcommand=scrollbar.set = keeps the scrollbar's position in sync with the text being scrolled/displayed
    output_box = tkinter.Text(output_frame, width=60, height=15, yscrollcommand=scrollbar.set, font=("calibre", 10))
    # side=tkinter.LEFT  = positions the text widget against the left edge of the frame
    # fill=tkinter.BOTH  = text widget expands to fill available space on both axes (horizontal + vertical)
    # expand=True = widget claims extra space in the frame if the window is resized;
    # without it, the text stays at its fixed width/height despite more space being available.
    output_box.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
    # output_box.yview when scrollbar is dragged manually, scroll the text accordingly
    scrollbar.config(command=output_box.yview)

    # Center GUI when displayed on the screen:
    # Force Tkinter to calculate the actual needed size based on added elements / widgets:
    tkinter_object.update_idletasks()

    # Get the natural size Tkinter calculated for the GUI window:
    width = tkinter_object.winfo_width()
    height = tkinter_object.winfo_height()

    # Get screen dimensions:
    screen_width = tkinter_object.winfo_screenwidth()
    screen_height = tkinter_object.winfo_screenheight()

    # Calculate top-left position for centering:
    x = (screen_width // 2) - (width // 2)
    # CAREFUL: Use addition for height as well, because here,
    # the higher you go on the y-axis, the lower the coordinates are.
    y = (screen_height // 2) - (height // 2)

    # Apply size + position together, with some extra padding around the content
    # GUI width * GUI size + GUI top left corner x coordinate + GUI top left corner y coordinate
    tkinter_object.geometry(f"{width + 40}x{height + 20}+{x}+{y}")

    # Only close the GUI window when user presses on exit button:
    tkinter_object.mainloop()


def display_text_in_output_box_of_gui(text):
    """
    Displays the given text at the end of the output box
    of the GUI, and a blank line afterward.
    :param text: (string) text to be displayed
    :return: None
    """
    output_box.insert(tkinter.END, text + "\n")
    # Automatically scroll till the last line:
    output_box.see(tkinter.END)


def display_recovered_file_name_in_output_box_of_gui(recovered_file_name, recovered_file):
    """
    Displays the given name of the recovered file at the end of the output box
    of the GUI, a button to recover that file, and a blank line afterward.
    :param recovered_file_name: (string) file name to be displayed
    :param recovered_file: (bytes) recovered file with the possibility of being saved on the device
    :return: None
    """
    recover_file_button = tkinter.Button(tkinter_object, text="Recover File",
                                         command=lambda: file_saving.save_recovered_file_at_given_path(
                                                    recovered_file, recovered_file_name, output_folder))

    output_box.insert(tkinter.END, f"[FOUND FILE]: {recovered_file_name} ")
    # Insert widget (i.e. button):
    output_box.window_create(tkinter.END, window=recover_file_button)
    output_box.insert(tkinter.END, "\n")
    # Automatically scroll till the last line:
    output_box.see(tkinter.END)


def setup_progress_bar(usb_size):
    """
    For the setup, it sets the maximum value of the progress bar
    to the USB size, and sets the current value of the progress bar to 0.
    :param usb_size: (int) total bytes of the USB disk
    :return: None
    """

    def configure_progress_bar():
        progress_bar["maximum"] = usb_size
        progress_bar["value"] = 0

    tkinter_object.after(0, configure_progress_bar)


def update_progress_bar(current_position):
    """
    Updates the progress bar, increasing its value to the current position
    of the scanned bytes within the USB disk.
    :param current_position: (int) the current byte position within the USB disk
    :return: None
    """

    def set_value_of_progress_bar():
        progress_bar["value"] = current_position

    tkinter_object.after(0, set_value_of_progress_bar)
