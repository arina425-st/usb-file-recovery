import os.path

import gui


def save_recovered_file_at_given_path(recovered_file, recovered_file_name, output_folder):
    """
    Saves the given recorded file with the specified name
    at the given location.
    :param recovered_file: (bytes) the recovered file from the USB disk
    :param recovered_file_name: (string) the name of the recovered file from the USB disk
    :param output_folder: (string) an existing path where the recovered file will be saved
    :return: None
    """
    output_path = os.path.join(output_folder, recovered_file_name)
    with open(output_path, "wb") as file:
        file.write(recovered_file)
        # print(f"[SAVED FILE]: {recovered_file_name}")
        gui.display_text_in_output_box_of_gui(f"[SAVED FILE]: {recovered_file_name}")
