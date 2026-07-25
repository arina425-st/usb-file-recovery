# 1 octet = 8 bits = 1 byte
import magic_bytes_matching
import file_saving


def read_bytes_from_usb(max_bytes_read_at_once, usb_path, output_folder):
    """
    Reads from the specified file path,
    maximum specified number of bytes at a time.
    :param max_bytes_read_at_once: (int) nr. of bytes read at once
    :param usb_path: (string) path of the file where the USB is
    :param output_folder: (string) path of the output folder
                          where the recovered files will be saved
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
    with open(usb_path, "rb") as file:
        print("[START FILE RECOVERY]")
        while True:
            bytes_data = file.read(max_bytes_read_at_once)

            if not bytes_data:
                break

            # Match magic bytes:
            recovered_file_name, recovered_file, recovered_file_length = (
                magic_bytes_matching.recover_if_match_with_magic_bytes(bytes_data)
            )

            # Avoid unnecessary saving of files of type None:
            if recovered_file is None:
                continue

            print(f"[FOUND FILE]: {recovered_file_name}")
            file_saving.save_recovered_file_at_given_path(recovered_file, recovered_file_name, output_folder)
            # match = magic_bytes_matching.recover_if_match_with_magic_bytes(bytes_data)

            # if match is not None:
            #     print(match)

        print("[END FILE RECOVERY]")
