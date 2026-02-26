# Photo Cropper Tool

A small desktop application for batch-processing images for print workflows (e.g. Etsy listings).

The app allows you to:
- Select an **input folder** containing images
- Select an **output folder**
- Choose multiple **print sizes** via checkboxes (defined in a YAML config)
- Automatically:
  - Create a structured output folder per image
  - Copy original images into their own folders
  - Generate cropped/resized versions for each selected size

Built with **Python**, **Tkinter**, **Pillow**, and **YAML**.

---

## Features

- 📂 Folder-based batch processing
- 🖼 One output folder per image
- 📐 Print sizes driven by YAML config
- 🧼 Clean separation of UI and logic
- ⚙ Uses standard libraries (`os`, `errno`, `shutil`, `sys`)

---

## Project Structure
```
photo_cropper/
│
├─ main.py # Application entry point
│
├─ ui/
│ └─ app.py # Tkinter UI
│
├─ core/
│ ├─ crop_task.py # Image processing logic
│ └─ make_folders.py # Output folder + file copying logic
│
├─ config/
│ ├─ loader.py # YAML config loader
│ └─ sizes.yaml # Print size definitions
│
└─ requirements.txt
```

---

## Output Folder Structure

For an input image:
```
input/
└─ example.jpg
```

The output will be:
```
output/
└─ example/
├─ example.jpg
└─ MockUps/
├─ Pictures/
| ├─ example_5x7.jpg
| └─ example_8x10.jpg
└─ ...
```

Each image gets:
- Its own folder
- A copy of the original image
- A `Pixtures/` folder containing cropped versions
- A `Mockups/` folder containing a 5x7 cropped version of the image and the mockup images

---

## Configuration (`sizes.yaml`)

All available print sizes are defined in YAML:

```yaml
dpi: 300

sizes:
  - id: 5x7
    label: "5 × 7 inches"
    width_in: 5
    height_in: 7

  - id: 8x10
    label: "8 × 10 inches"
    width_in: 8
    height_in: 10

extensions:
  jpg:
    quality: 95
    subsampling: 95
  jpeg:
    quality: 95
    subsampling: 95
  png:
    compress_level: 0
  gif:
    save_all: True
  tiff:
    save_all: True
    quality: 95
```

## Installation Requirements
```
Python 3.9+

Pip
```
## Install dependencies
```
pip install -r requirements.txt

Running the App

From the project root:

python main.py
```
