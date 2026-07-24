# 1 octet = 8 bits = 1 byte
import magic_bytes_matching


def read_bytes_from_usb(max_bytes_read_at_once, usb_path):
    """
    Reads from the specified file path,
    maximum specified number of bytes at a time.
    :param max_bytes_read_at_once: (int) nr. of bytes read at once
    :param usb_path: (string) path of the file where the USB is
    :return: None
    """
    # Use "with ..." to close the file regardless
    # of errors occurred in the loop
    # Open the file for rb (= reading bytes):
    # In order not to overwhelm the RAM,
    # and hence, stop the program,
    # read the file a few bytes at a time:
    with open(usb_path, "rb") as file:
        print("[START FILE RECOVERY]")
        while True:
            bytes_data = file.read(max_bytes_read_at_once)

            if not bytes_data:
                break

            # Match magic bytes:
            match = magic_bytes_matching.match_with_magic_bytes(bytes_data)

            if match is not None:
                print(match)

        print("[END FILE RECOVERY]")
