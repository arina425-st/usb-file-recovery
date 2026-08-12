# USB File Recovery
_for educational purposes only_

This project is supposed to recover any deleted file from a USB stick, 
as long as no other file was written over it. The goal of the project is to prove 
that nothing can always be deleted. In other words, by not being careful enough, 
potentially sensitive data may be recovered by unauthorized parties, accessing the USB stick after file deletion.

## Preparation:
- Install Python
- Buy a USB stick of min 4 GB with at least one deleted file to recover
- Connect the USB stick to your device before running the software.

## Features (current)
- Dictionary of magic bytes for common file types (DOC, DOCX/ZIP, EXE, JPEG/JPG, PDF, PNG)
- Reading the USB on octet level
- Sequential scanning for magic bytes
- Extracting and saving the found files
- GUI for scanning, progress tracking, and downloading recovered files


## How it works
Introduce the USB stick in the device you are running the app from. 
Then, provide the hardcoded path of the USB stick,
and press the start button from the GUI. All the found file names will be printed in the terminal, 
and if the recover files button is pressed, the corresponding files will be saved in the output folder.


## Requirements
- Python 3.x
- USB stick of min 4 GB
- Python standard library, no external dependencies

## Usage
```bash
python main.py
```
1. Run `main.py`.
2. Enter the path of the USB drive in the corresponding field.
3. Press the **Start File Recovery** button.
4. If any files are found, they will be displayed in the output box.
Press the **Recover File** button if you wish to recover them.
5. The progress will be shown in the progress bar and the name of the successfully recovered files will be displayed in the output box.
6. The recovered files will be saved on the local machine within the project folder in a subfolder named 'recovered_files'.


## Testing environment
USB stick of minimum 4 GB and maximum of 8 GB.

## What I learned
- Reading files on byte level.
- Matching magic bytes (i.e. file signatures) to file types.
- Extracting a recovered file's content using either a trailer (end marker) or a maximum estimated file size, depending on the file type.
- Searching for the closest known header at any byte position, instead of only checking the start of fixed-size chunks, so files aren't missed just because they don't align to a chunk boundary.
- Saving the recovered file types on the local device.

## What I would improve
- Recovered files are not automatically scanned for malware. In a real-world 
scenario, recovered files should be opened only in an isolated environment 
and scanned with antivirus software before being trusted.
- This project works well for USB drives of 4 or 8 GB,
but for very large ones, reading the entire USB content via `file.read()`
could exceed the available RAM memory. In a  future, more advanced version of the project, 
I will use the `mmap` library. `mmap` objects are aware of all memory locations,
letting the OS load the accessed parts of the bytes only at any given moment.
Hence, there will be no need to save all the USB content into the RAM memory at once,
but only the needed part of it.

## License
Copyright (c) 2026 Arina Ralea

All rights reserved.

This code is provided for portfolio and educational demonstration 
purposes only. No permission is granted to use, copy, modify, 
distribute, or sell this code, in whole or in part, without 
explicit written permission from the author.
