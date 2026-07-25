# Magic Bytes taken from:
# https://asecuritysite.com/forensics/magic
# https://www.ease.ws/forensics/fileCarving/fileSignatures.html
# For PNG trailer: https://www.w3.org/TR/png/#11IEND

# For file types where no trailer was available,
# I used a maximum estimated file size.

# Sources for maximum estimated file size:
#   DOC - 32 MB (for text documents): https://learn.microsoft.com/en-us/answers/questions/5065369/max-size-of-word-file
#   DOCX/ZIP - 4 GiB (DOCX is subtype of ZIP): https://en.wikipedia.org/wiki/ZIP_(file_format)
#   EXE - 4 GB:
#       https://superuser.com/questions/667593/is-it-possible-to-run-a-larger-than-4gb-exe#:~:text=Having%20a%20self%20extracting%20executable,and%2064%2Dbit%20versions).

# Notes on file types:
#   JPEG/JPG: (JPG is the abbreviation of JPEG)
#   Remove 0A from PDF trailer as it represents newline.

# Dictionary structure:
#       key: file type
#       value: dictionary {key: header - value, key: trailer / maximum estimated file size - value}
MAGIC_BYTES = {
    # Byte conversion (for reading function in bytes): GB > MB > KB > B
    #                  1 GB = 1 * 1000 MB = 1 * 1000 * 1000 KB = 1 * 1000 * 1000 * 1000 B
    #                                                  GiB > MiB > KiB > B
    #                  1 GiB = 1 * 1024 MiB = 1 * 1024 * 1024 KiB = 1 * 1024 * 1024 * 1024 B
    # Convert from hex to byte
    # for later comparison;
    # white spaces are ignored anyway:
    "doc": {
        "header": bytes.fromhex("D0 CF 11 E0 A1 B1 1A E1"),
        "max_estimated_file_size": 32 * 1000 * 1000
    },
    "zip": {
        "header": bytes.fromhex("50 4B 03 04"),
        "max_estimated_file_size": 4 * 1024 * 1024 * 1024
    },
    "exe": {
        "header": bytes.fromhex("4D 5A"),
        "max_estimated_file_size": 4 * 1000 * 1000 * 1000
    },
    "jpg": {
        "header": bytes.fromhex("FF D8 FF"),
        "trailer": bytes.fromhex("FF D9")
    },
    "pdf": {
        "header": bytes.fromhex("25 50 44 46"),
        "trailer": bytes.fromhex("25 25 45 4F 46")
    },
    "png": {
        "header": bytes.fromhex("89 50 4E 47"),
        "trailer": bytes.fromhex("49 45 4E 44")
    }
}

# Save current number of recovered files for file numbering:
current_recovered_file_nr = 1


def recover_if_match_with_magic_bytes(bytes_data):
    """
    Compares the given bytes_data against all the
    magic types within the dictionary. If a match is found,
    it returns the corresponding file type, otherwise it
    returns None.
    :param bytes_data: (bytes) raw bytes of the data from the USB
    :return recovered_file_name: (string) the name of the recovered file with its file type as a file extension
                                    or None if no match is found
    :return recovered_file: (bytes) the recovered file or None if no match is found
    :return recovered_file_length: (int) the length of the recovered file or 0 is no match is found
    """
    global current_recovered_file_nr
    recovered_file_name = None
    recovered_file = None
    recovered_file_length = 0

    for file_type, magic_bytes in MAGIC_BYTES.items():
        # CAREFUL: avoid "==" because magic bytes are only at the start,
        # not the whole byte stream (i.e. perfect match).
        if bytes_data.startswith(magic_bytes.get("header")):
            is_match_found = False
            # Check if file type has trailer:
            if "trailer" in magic_bytes:
                trailer = magic_bytes.get("trailer")
                # Returns -1 if no trailer is found:
                trailer_index = bytes_data.find(trailer)
                if trailer_index != -1:
                    is_match_found = True
                    # Get file until the last byte of the trailer:
                    recovered_file = bytes_data[:trailer_index + len(trailer)]

            # Or check if file type has max estimated file size:
            elif "max_estimated_file_size" in magic_bytes:
                max_estimated_file_size = magic_bytes.get("max_estimated_file_size")
                recovered_file = bytes_data[:max_estimated_file_size]
                is_match_found = True

            if is_match_found:
                recovered_file_name = f"recovered_file_{current_recovered_file_nr}.{file_type}"
                recovered_file_length = len(recovered_file)
                current_recovered_file_nr = current_recovered_file_nr + 1

    return recovered_file_name, recovered_file, recovered_file_length
