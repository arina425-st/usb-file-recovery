import os

import byte_reading

if __name__ == '__main__':
    # Provide values for testing:
    # (later let the user enter them from GUI)
    max_bytes_read_at_once = 4096
    # raw file access (byte wise)
    usb_path = r"\\.\E:"

    # DRAFT: Use a temporary output put for saving the recovered file.
    # TODO: Save the recovered file on the USB disk.
    output_folder = "recovered_files"
    # exist_ok=True - do not throw error if file already exists
    os.makedirs(output_folder, exist_ok=True)
    
    byte_reading.read_bytes_from_usb(max_bytes_read_at_once, usb_path, output_folder)
