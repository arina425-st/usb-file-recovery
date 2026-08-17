# 1 octet = 8 bits = 1 byte
import gui
import magic_bytes_matching


def read_bytes_from_usb(usb_path):
    """
    Reads from the specified file path,
    all the bytes at a once.
    :param usb_path: (string) path of the file where the USB is
    :return: None
    """
    # Use "with ..." to close the file regardless
    # of errors occurred in the loop
    # Open the file for rb (= reading bytes):
    # In order not to overwhelm the RAM,
    # and hence, stop the program,
    # read the file a few bytes at a time:
    # CAREFUL: (while developing the software, at least)
    # Only read from the USB disk,
    # DO NOT write on the USB disk,
    # otherwise deleted files may be overwritten,
    # and, hence, never recovered.
    # Get USB size:
    # 4 MB per read
    chunk_size = 4 * 1000 * 1000
    # limit of project: 8 GB
    max_total_size = 8 * 1000 * 1000 * 1000

    chunks = []
    total_read = 0

    # Setup progress bar for the reading:
    gui.setup_progress_bar(max_total_size)

    try:
        with open(usb_path, "rb") as file:

            gui.display_text_in_output_box_of_gui("[START USB READING]")

            while total_read < max_total_size:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                chunks.append(chunk)
                print("DEBUG: Still reading chunk")
                total_read += len(chunk)
                print(f"DEBUG: Current length: {total_read}")

                # Update progress bar for the reading:
                gui.update_progress_bar(total_read)

            gui.display_text_in_output_box_of_gui("[END USB READING]")
    except FileNotFoundError:
        gui.display_text_in_output_box_of_gui("[ERROR]: Path not found!")
        gui.enable_start_recovery_button()
        return
    except PermissionError:
        gui.display_text_in_output_box_of_gui("[ERROR]: Permission of accessing the path denied! Try running admin / "
                                              "root mode.")
        gui.enable_start_recovery_button()
        return

    bytes_data = b"".join(chunks)
    usb_size = len(bytes_data)

    # Setup progress bar with respect to the actual USB size:
    gui.setup_progress_bar(usb_size)

    # Uncomment for debug / testing purposes:
    # print("[START FILE RECOVERY]")
    gui.display_text_in_output_box_of_gui("[START FILE RECOVERY]")

    current_position = 0
    while current_position < usb_size:
        # Match magic bytes:
        recovered_file_name, recovered_file, recovered_file_length = (
            magic_bytes_matching.recover_if_match_with_magic_bytes(bytes_data[current_position:])
        )

        # Avoid unnecessary saving of files of type None:
        if recovered_file is None:
            # Move to the next closest header:
            next_position = magic_bytes_matching.find_next_magic_bytes_header(bytes_data, current_position + 1)
            # If there are no other headers, stop the algorithm:
            if next_position is None:
                break

            current_position = next_position
            gui.update_progress_bar(current_position)
            continue

        gui.display_recovered_file_name_in_output_box_of_gui(recovered_file_name, recovered_file)

        current_position += recovered_file_length
        # Update progress bar depending on how much of the usb_size has been scanned:
        gui.update_progress_bar(current_position)

    gui.update_progress_bar(usb_size)
    # print("[END FILE RECOVERY]")
    gui.display_text_in_output_box_of_gui("[END FILE RECOVERY]")
    gui.enable_start_recovery_button()
