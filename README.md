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

## Features (planned)
- GUI for scanning, progress tracking, and downloading recovered files

## How it works
Introduce the USB stick in the device you are running the app from. 
Then, provide the hardcoded path of the USB stick, 
(eventually) provide the hardcoded path of the output file (existent or not) 
and press run. All the found and saved file names will be printed in the terminal, 
and saved in the specified output folder.


## Requirements
- Python 3.x
- USB stick of min 4 GB
- Python standard library, no external dependencies

## Usage
```bash
python main.py
```
1. Open `main.py`.
2. Set `usb_path` to the path of the USB stick within your device.
3. (Optional) Specify the location where the recovered files should be saved by
setting `output_folder` to an already existent (or about to be created) path.
4. Run the above command.

The found file types will be printed in the terminal.

## Testing environment
USB stick of minimum 4 GB.

## What I learned
- Reading files on byte level.
- Matching magic bytes (i.e. file signatures) to file types.

## What I would improve
Recovered files are not automatically scanned for malware. In a real-world 
scenario, recovered files should be opened only in an isolated environment 
and scanned with antivirus software before being trusted.

## License
Copyright (c) 2026 Arina Ralea

All rights reserved.

This code is provided for portfolio and educational demonstration 
purposes only. No permission is granted to use, copy, modify, 
distribute, or sell this code, in whole or in part, without 
explicit written permission from the author.
