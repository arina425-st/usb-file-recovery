import byte_reading

if __name__ == '__main__':
    # Provide values for testing:
    # (later let the user enter them from GUI)
    max_bytes_read_at_once = 4096
    # raw file access (byte wise)
    usb_path = r"\\.\E:"
    byte_reading.read_bytes_from_usb(max_bytes_read_at_once, usb_path)
